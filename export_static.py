#!/usr/bin/env python3
"""
Seysa Medya — GitHub Pages Statik Site İhracı (Static Site Exporter)

Bu betik, dinamik Python sunucusundaki tüm sayfaları ve veritabanı kayıtlarını
GitHub Pages ile %100 uyumlu, bağımsız statik HTML dosyalarına (`docs/`) dönüştürür.
Tüm dosya yolları ve bağlantılar göreceli (relative) hale getirilir, böylece
hem GitHub Pages alt klasöründe hem de yerel tarayıcıda doğrudan çalışır.
"""
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from seysa import storage, views
from seysa.content import SERVICES
from seysa.journal import ARTICLES

DOCS_DIR = ROOT / 'docs'


def rewrite_html(html, depth, root_prefix=None):
    """
    HTML içindeki mutlak yolları (örn. /style.css, /hizmetler, /assets/...)
    bulunulan sayfanın derinliğine göre göreceli (relative) yollara çevirir.
    """
    def repl(m):
        attr = m.group(1)
        quote = m.group(2)
        url = m.group(3)

        # Harici linkler, e-posta, çapa ve protokolleri olduğu gibi bırak
        if not url or url.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', 'javascript:', '#', '//')):
            return m.group(0)
        
        # Sadece kökten başlayan yolları dönüştür
        if not url.startswith('/'):
            return m.group(0)

        match = re.match(r'^([^?#]*)(\?[^#]*)?(#.*)?$', url)
        path_part = match.group(1) if match else url
        query = match.group(2) or ''
        fragment = match.group(3) or ''

        prefix = root_prefix if root_prefix is not None else '../' * depth
        if path_part == '/':
            new_url = (prefix + 'index.html' if prefix else 'index.html') + query + fragment
        else:
            clean = path_part.lstrip('/')
            # Dosya uzantısı varsa (.css, .js, .svg, .png, .jpg, .webp, .txt vb.)
            if re.search(r'\.[a-zA-Z0-9]+$', clean):
                new_url = prefix + clean + query + fragment
            else:
                # Sayfa rotası ise /index.html'e yönlendir
                new_url = prefix + clean.rstrip('/') + '/index.html' + query + fragment

        return f'{attr}={quote}{new_url}{quote}'

    return re.sub(r'(\b(?:href|src|action|data-full-image))=([\"\'])([^\"\']+)\2', repl, html)


def build_admin_preview_page():
    """GitHub Pages üzerinde /admin tıklandığında gösterilecek bilgilendirme sayfası."""
    card = '''
    <section class="container section-after-intro" style="max-width: 640px; margin: 40px auto; padding: 32px; background: #ffffff; border: 1px solid #e5e7eb; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
        <h2 style="margin-top:0; font-size: 24px; color: #111827;">Yönetim Paneli Bilgisi</h2>
        <p style="color: #4b5563; line-height: 1.6;">
            Bu site şu anda <strong>GitHub Pages</strong> üzerinde statik önizleme olarak yayınlanmaktadır.
        </p>
        <p style="color: #4b5563; line-height: 1.6;">
            İçerik ekleme, düzenleme ve silme işlemlerini gerçekleştirebileceğiniz yönetim paneli,
            güvenlik gereği yerel Python ortamında (<code>python3 -B server.py</code>) ve SQLite veritabanı ile çalışır.
        </p>
        <div style="margin-top: 24px;">
            <a class="button" href="/">Ana Sayfaya Dön <svg class="ui-icon" aria-hidden="true" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a>
        </div>
    </section>
    '''
    return views.page('Yönetim Paneli', card, path='/admin')


def export():
    print('📦 Statik site derlemesi başlatılıyor...')
    storage.initialize()
    projects, refs = storage.public_data()
    print(f'   - {len(projects)} yayınlanan proje ve {len(refs)} referans veritabanından alındı.')

    # 1. docs/ klasörünü temizle/oluştur
    if DOCS_DIR.exists():
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Statik dosyaları kopyala
    print('📂 Varlıklar kopyalanıyor (style.css, main.js, assets, uploads)...')
    shutil.copy2(ROOT / 'style.css', DOCS_DIR / 'style.css')
    shutil.copy2(ROOT / 'main.js', DOCS_DIR / 'main.js')

    if (ROOT / 'assets').exists():
        shutil.copytree(ROOT / 'assets', DOCS_DIR / 'assets')

    # Yüklenen görselleri kopyala (.data/uploads -> docs/uploads)
    uploads_target = DOCS_DIR / 'uploads'
    uploads_target.mkdir(parents=True, exist_ok=True)
    published_media = {p['image'] for p in projects} | {r['logo'] for r in refs} | {m['url'] for p in projects for m in p.get('gallery',[]) if m['kind']=='image'}
    for url in published_media:
        if not url.startswith('/uploads/'): continue
        item=storage.UPLOADS / Path(url).name
        if item.is_file(): shutil.copy2(item, uploads_target / item.name)

    # GitHub Pages için .nojekyll ve robots.txt oluştur
    (DOCS_DIR / '.nojekyll').write_text('', encoding='utf-8')
    (DOCS_DIR / 'robots.txt').write_text('User-agent: *\nDisallow: /admin/\n', encoding='utf-8')

    # 3. Sayfa rotalarını oluştur
    pages = {
        '/': (views.home(projects, refs), 0),
        '/hizmetler': (views.services_page('/hizmetler'), 1),
        '/projeler': (views.projects_page(projects), 1),
        '/referanslar': (views.references_page(refs), 1),
        '/paketler': (views.packages_page(), 1),
        '/hakkimizda': (views.about_page(), 1),
        '/iletisim': (views.contact_page(), 1),
        '/admin': (build_admin_preview_page(), 1),
    }

    # Hizmet alt sayfaları (31 adet)
    for path in SERVICES:
        depth = len([p for p in path.strip('/').split('/') if p])
        pages[path] = (views.services_page(path), depth)

    # Proje detay sayfaları
    for suffix in ['', '/rehberler', '/sektor-haberleri'] + ['/'+a['slug'] for a in ARTICLES]:
        path = '/icerik-rehberi'+suffix
        pages[path] = (views.journal_page(path), len(path.strip('/').split('/')))

    for p in projects:
        path = f'/projeler/{p["id"]}'
        depth = 2
        pages[path] = (views.projects_page(projects, p['id']), depth)

    # 4. HTML dosyalarını dönüştür ve yaz
    print(f'📝 {len(pages)} sayfa HTML olarak derleniyor...')
    for path, (raw_html, depth) in pages.items():
        converted = rewrite_html(raw_html, depth)
        if path == '/':
            target_file = DOCS_DIR / 'index.html'
        else:
            rel_dir = DOCS_DIR / path.strip('/')
            rel_dir.mkdir(parents=True, exist_ok=True)
            target_file = rel_dir / 'index.html'
        target_file.write_text(converted, encoding='utf-8')

    # 5. 404.html sayfası oluştur (GitHub Pages standart)
    # Error pages can be served at arbitrary depths; assets must resolve from the site root.
    site_prefix = '/' + os.environ.get('SITE_BASE_PATH', 'seysam').strip('/') + '/'
    site_prefix = site_prefix.replace('//', '/')
    err_404 = rewrite_html(views.error_page(404, 'Aradığınız sayfa bulunamadı.'), 0, root_prefix=site_prefix)
    (DOCS_DIR / '404.html').write_text(err_404, encoding='utf-8')

    print('✅ Derleme başarıyla tamamlandı!')
    print(f'   Çıktı konumu: {DOCS_DIR}')


if __name__ == '__main__':
    export()
