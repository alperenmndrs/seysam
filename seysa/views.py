from html import escape
from urllib.parse import quote
from .content import GROUPS, SERVICES, NAV, PACKAGES


def e(value):
    return escape(str(value if value is not None else ''), quote=True)


def button(label, url, extra=''):
    return f'<a class="button {extra}" href="{e(url)}">{e(label)} <span aria-hidden="true">↗</span></a>'


def page(title, body, path='/', description='', csrf='', admin=False, authenticated=False):
    links = ''.join(f'<a href="{p}" {"aria-current=page" if (path==p or p!="/" and path.startswith(p+"/")) else ""}>{t}</a>' for p,t in NAV)
    logo = '<img src="/assets/seysa-logo.svg" width="171" height="65" alt="Seysa Medya">'
    if admin:
        header = f'<header class="admin-header"><a href="/">{logo}</a><span>Yönetim paneli</span><a href="/">Siteyi aç</a>'
        if authenticated:
            header += f'<form method="post" action="/admin/cikis"><input type="hidden" name="csrf" value="{e(csrf)}"><button class="plain-button">Çıkış yap</button></form>'
        header += '</header>'
        footer = ''
    else:
        header = f'''<a class="skip-link" href="#main">İçeriğe geç</a><header class="site-header"><div class="container header-inner"><a class="brand" href="/" aria-label="Seysa Medya ana sayfa">{logo}</a><button id="menu-toggle" class="menu-toggle" aria-controls="main-nav" aria-expanded="false" hidden>Menü</button><nav id="main-nav" aria-label="Ana menü">{links}</nav></div></header>'''
        footer = f'''<footer class="site-footer"><div class="container footer-inner"><a class="brand" href="/">{logo}</a><nav aria-label="Alt menü"><a href="/hizmetler">Hizmetler</a><a href="/projeler">Projeler</a><a href="/referanslar">Referanslar</a><a href="/iletisim">İletişim</a></nav><a href="mailto:info@seysamedya.com">info@seysamedya.com</a></div><div class="container footer-bottom"><span>© 2026 Seysa Medya</span><a href="/admin">Yönetim</a></div></footer>'''
    creative_style = '' if admin else '<link rel="stylesheet" href="/assets/creative.css">'
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="description" content="{e(description or title)}"><title>{e(title)} — Seysa Medya</title><link rel="icon" href="/assets/seysa-logo.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">{creative_style}<script defer src="/main.js"></script></head><body class="{'admin-body' if admin else ''}">{header}<main id="main">{body}</main>{footer}</body></html>'''


def intro(title, description='', parent=None):
    crumbs = '<a href="/">Ana Sayfa</a>'
    if parent:
        crumbs += f'<span aria-hidden="true">/</span><a href="{e(parent[0])}">{e(parent[1])}</a>'
    return f'<div class="page-intro container"><nav class="breadcrumbs" aria-label="Sayfa yolu">{crumbs}<span aria-hidden="true">/</span><span aria-current="page">{e(title)}</span></nav><h1>{e(title)}</h1>{f"<p>{e(description)}</p>" if description else ""}</div>'


def service_cards(items=None):
    items = items if items is not None else [SERVICES['/hizmetler/'+g[0]] for g in GROUPS]
    return '<div class="service-grid visual-grid">' + ''.join(f'''<a class="service-card visual-card" data-tilt="3" href="{s['path']}">{service_image(s['path'])}<span class="visual-card-top"><span class="service-number">{i+1:02d}</span>{service_icon(s['path'])}</span><div class="visual-card-copy"><h2>{e(s['title'])}</h2><p>{e(s['description'])}</p><span class="card-link">Hizmeti keşfet <span aria-hidden="true">↗</span></span></div></a>''' for i,s in enumerate(items)) + '</div>'


def service_image(path):
    media = {'sosyal-medya-yonetimi': 'social', 'produksiyon': 'production',
             'marka-tasarim': 'design', 'web-dijital': 'digital',
             'digital-marketing': 'marketing', 'brand-setup': 'brand'}
    name = 'drone' if path.endswith('/drone') else media.get(path.split('/')[2], 'production')
    return f'<img class="service-photo" src="/assets/media/{name}.jpg" alt="" width="1400" height="1000" loading="lazy" decoding="async">'


def service_icon(path):
    """Small, local SVG interface icons; no font or remote icon dependency."""
    group = path.split('/')[2]
    shapes = {
        'sosyal-medya-yonetimi': '<rect x="3" y="3" width="18" height="18" rx="6"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
        'produksiyon': '<rect x="2" y="5" width="14" height="14" rx="3"/><path d="m16 10 6-4v12l-6-4M8 9l4 3-4 3Z"/>',
        'marka-tasarim': '<path d="m12 3 9 9-9 9-9-9ZM12 3v18M3 12h18"/>',
        'web-dijital': '<rect x="2" y="4" width="20" height="16" rx="3"/><path d="M2 9h20M6 6.5h.01M9 6.5h.01m0 6-3 2 3 2m6-4 3 2-3 2"/>',
        'digital-marketing': '<path d="M4 20V10m6 10V6m6 14v-8m-9-4 6-6h7v7m0-7-8 8"/>',
        'brand-setup': '<path d="m12 2 2.6 6.8L22 12l-7.4 3.2L12 22l-2.6-6.8L2 12l7.4-3.2Z"/>',
    }
    return '<span class="service-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'+shapes.get(group, shapes['brand-setup'])+'</svg></span>'


def logo_strip(refs):
    logos = [r for r in refs if r['logo']]
    if not logos: return ''
    entries = ''
    for r in logos:
        img = f'<img src="{e(r["logo"])}" alt="{e(r["name"])}" width="170" height="85" loading="lazy">'
        entries += f'<a class="logo-item" href="{e(r["website"])}" aria-label="{e(r["name"])} resmi sitesi">{img}</a>' if r.get('website') else f'<div class="logo-item">{img}</div>'
    copies = ''.join(f'<div class="logo-item"><img src="{e(r["logo"])}" alt="" width="170" height="85" loading="lazy"></div>' for r in logos)
    return f'''<div class="logo-strip" data-logo-strip><div class="logo-track"><div class="logo-group">{entries}</div><div class="logo-group" aria-hidden="true">{copies}</div></div></div>'''


def project_cards(projects):
    if not projects: return '<p class="empty-state">Henüz yayınlanan proje yok.</p>'
    cards = ''
    for p in projects:
        image = f'<img src="{e(p["image"])}" alt="{e(p["title"])}" width="680" height="460" loading="lazy">' if p['image'] else '<div class="project-no-image" aria-hidden="true">Seysa Medya</div>'
        cards += f'<a class="project-card" href="/projeler/{p["id"]}">{image}<div><span class="meta">{e(p["company_name"] or p["service"])}</span><h2>{e(p["title"])}</h2><p>{e(p["summary"])}</p><span class="card-link">Projeyi incele ↗</span></div></a>'
    return '<div class="project-grid">'+cards+'</div>'


def home(projects, refs):
    featured = [SERVICES['/hizmetler/'+slug] for slug in ['produksiyon', 'sosyal-medya-yonetimi', 'marka-tasarim', 'web-dijital', 'digital-marketing', 'brand-setup']]
    services = '<section class="container section creative-services"><div class="section-heading"><div><span class="eyebrow">NELER YAPIYORUZ?</span><h2>Fikirden<br><em>son kareye.</em></h2></div><div class="section-summary"><p>Çekim, tasarım ve dijital iletişim.<br>Markanız için birlikte üretiyoruz.</p><a class="text-link" href="/hizmetler">Tüm hizmetler ↗</a></div></div>'+service_cards(featured)+'</section>'
    hero = '''<section class="creative-hero"><div class="container creative-hero-inner"><div class="hero-copy"><span class="eyebrow"><i aria-hidden="true"></i> SEYSA MEDYA / KREATİF &amp; PRODÜKSİYON</span><h1>İyi bir fikir.<br><span>Güçlü bir</span><br>iz<span class="orange-dot">.</span></h1><p>Markanızı görünür kılan filmler, tasarımlar ve dijital deneyimler üretiyoruz.</p><div class="hero-actions"><a class="button" href="/iletisim">Teklif al <span aria-hidden="true">↗</span></a><a class="text-link" href="/projeler">Projeleri incele ↗</a></div></div><div class="hero-stage" data-hero-motion><div class="mesh-aura" aria-hidden="true"></div><div class="lens-sculpture" aria-hidden="true"><div class="lens-ring"></div><div class="lens-core"></div></div><a class="hero-shot hero-shot-main" href="/hizmetler/produksiyon"><img src="/assets/media/production.jpg" alt="Profesyonel kamera ve çekim seti" width="1400" height="2100" fetchpriority="high"><span class="shot-label"><span>PRODÜKSİYON</span><span>↗</span></span></a><a class="hero-shot hero-shot-drone" href="/hizmetler/produksiyon/drone"><img src="/assets/media/drone.jpg" alt="Havadan kıyı görüntüsü" width="1400" height="1000"><span class="shot-label"><span>FARKLI BİR AÇI.</span><span>↗</span></span></a><span class="stage-cross" aria-hidden="true">+</span><span class="stage-caption">FİKİR. KAMERA. AKSİYON.</span></div></div><div class="container hero-bottom"><span>Stratejiyle başlar. Yaratıcılıkla görünür olur.</span><a href="#hizmetlerimiz">Keşfet <span aria-hidden="true">↓</span></a></div></section><div class="discipline-strip" aria-hidden="true"><span>FİKİR</span><b>✳</b><span>PRODÜKSİYON</span><b>✳</b><span>TASARIM</span><b>✳</b><span>DİJİTAL</span><b>✳</b><span>ETKİ</span></div>'''
    services = services.replace('class="container section creative-services"', 'id="hizmetlerimiz" class="container section creative-services"')
    reference_section = ''
    if refs:
        reference_title = 'Örnek logolar' if all(r.get('is_sample') for r in refs) else 'Referanslarımız'
        reference_section = '<section class="reference-band"><div class="container section-heading"><h2>'+reference_title+'</h2><div class="strip-actions"><a class="text-link" href="/referanslar">Tüm referanslar ↗</a><button class="plain-button motion-toggle" type="button" aria-pressed="false" hidden>Hareketi durdur</button></div></div>'+logo_strip(refs)+ ('<div class="container"><p class="sample-note">Örnek olarak eklenen logolar müşteri ilişkisi belirtmez.</p></div>' if any(r.get('is_sample') for r in refs) else '')+'</section>'
    work = '<section class="container section"><div class="section-heading"><h2>Projeler</h2><a class="text-link" href="/projeler">Tüm projeler ↗</a></div>'+project_cards(projects[:3])+'</section>' if projects else ''
    cta = '<section class="creative-cta"><div class="container"><span class="eyebrow">SIRADAKİ İYİ FİKİR SİZİN OLSUN.</span><a href="/iletisim"><h2>Birlikte<br>üretelim.</h2><span class="cta-arrow" aria-hidden="true">↗</span></a><p>Projenizi konuşalım. İlk adımı birlikte atalım.</p></div></section>'
    return page('Ana Sayfa', hero+services+reference_section+work+cta, description='Seysa Medya: sosyal medya yönetimi, prodüksiyon, marka tasarımı, web ve dijital pazarlama hizmetleri.')


def services_page(path):
    if path == '/hizmetler':
        body = intro('Hizmetler', 'Markanızın içerik, tasarım ve dijital iletişim ihtiyaçları için çalışıyoruz.')
        body += '<section class="container section-after-intro">'
        for g in GROUPS:
            s = SERVICES['/hizmetler/'+g[0]]
            links = ''.join(f'<a href="{c["path"]}">{e(c["title"])} <span aria-hidden="true">↗</span></a>' for c in s['children'])
            body += f'<article class="service-directory visual-directory"><div class="directory-cover">{service_image(s["path"])}<div>{service_icon(s["path"])}<h2><a href="{s["path"]}">{e(s["title"])}</a></h2><p>{e(s["description"])}</p><a class="text-link" href="{s["path"]}">Hizmeti inceleyin ↗</a></div></div><div class="subservice-links">{links or "<p>İçerik planlama, tasarım, yayın ve topluluk yönetimi.</p>"}</div></article>'
        body += '</section>'
        return page('Hizmetler', body, path)
    s = SERVICES[path]
    parent = ('/hizmetler','Hizmetler') if s['parent']=='/hizmetler' else (s['parent'], SERVICES[s['parent']]['title'])
    body = intro(s['title'],s['description'],parent)
    if s['children']:
        body += '<section class="container section-after-intro">'+service_cards(s['children'])+'</section>'
    else:
        steps = ''.join(f'<li><h2>{e(t)}</h2>{f"<p>{e(d)}</p>" if d else ""}</li>' for t,d in s['scope'])
        body += '<section class="container detail-layout section-after-intro"><div><h2 class="scope-title">Hizmet kapsamı</h2><ul class="scope-list">'+steps+'</ul></div><aside class="service-aside"><h2>Teklif alın</h2><p>İhtiyacınızı paylaşın; kapsamı ve teslim takvimini birlikte belirleyelim.</p>'+button('Bize yazın','/iletisim?hizmet='+quote(s['title']))+'</aside></section>'
    if s['children']:
        body += '<section class="container contact-callout"><h2>'+e(s['title'])+' için teklif alın.</h2>'+button('Bize yazın','/iletisim?hizmet='+quote(s['title']))+'</section>'
    return page(s['title'],body,path,s['description'])


def references_page(refs):
    body = intro('Referanslar')
    if any(r.get('is_sample') for r in refs):
        body += '<div class="container"><p class="sample-note">Örnek olarak eklenen logolar müşteri ilişkisi belirtmez.</p></div>'
    if any(r['logo'] for r in refs):
        body += '<div class="container strip-actions"><button class="plain-button motion-toggle" aria-pressed="false" hidden>Hareketi durdur</button></div>'+logo_strip(refs)
    cards = ''
    for r in refs:
        logo = f'<img src="{e(r["logo"])}" alt="{e(r["name"])} logosu" width="200" height="100" loading="lazy">' if r['logo'] else ''
        if logo and r.get('website'): logo = f'<a class="reference-logo-link" href="{e(r["website"])}" aria-label="{e(r["name"])} resmi sitesi">{logo}</a>'
        author = '<cite>'+e(r['author'])+'</cite>' if r['author'] else ''
        feedback = '<blockquote><p>'+e(r['quote'])+'</p>'+author+'</blockquote>' if r['quote'] else ''
        if r.get('is_sample'): feedback += '<span class="sample-label">Örnek yerleşim</span>'
        cards += f'<article class="reference-card">{logo}<h2>{e(r["name"])}</h2>{feedback}</article>'
    body += '<section class="container section-after-intro"><div class="reference-grid">'+cards+'</div></section>' if refs else '<div class="container section-after-intro"><p class="empty-state">Henüz yayınlanan referans yok.</p></div>'
    return page('Referanslar',body,'/referanslar')


def projects_page(projects, project_id=None):
    if project_id is None:
        return page('Projeler',intro('Projeler')+'<section class="container section-after-intro">'+project_cards(projects)+'</section>','/projeler')
    p = next((p for p in projects if p['id']==project_id),None)
    if not p: return None
    body = intro(p['title'],p['summary'],('/projeler','Projeler'))
    image = f'<img class="project-cover" src="{e(p["image"])}" alt="{e(p["title"])}" width="1240" height="800">' if p['image'] else ''
    meta = ''.join(f'<div><dt>{label}</dt><dd>{e(value)}</dd></div>' for label,value in [('Şirket',p['company_name']),('Hizmet',p['service'])] if value)
    body += f'<article class="container section-after-intro">{image}<div class="project-detail"><div class="prose">'+''.join('<p>'+e(part)+'</p>' for part in p['body'].split('\n') if part.strip())+f'</div><dl>{meta}</dl></div></article>'
    return page(p['title'],body,'/projeler/'+str(p['id']),p['summary'])


def packages_page():
    cards = ''
    for title, desc, scope in PACKAGES:
        cards += '<article class="package-card"><h2>'+e(title)+'</h2><p>'+e(desc)+'</p><ul>'+''.join('<li>'+e(s)+'</li>' for s in scope)+'</ul>'+button('Teklif alın','/iletisim?hizmet='+quote(title))+'</article>'
    return page('Paketler / Teklif Al',intro('Paketler / Teklif Al','Kapsam ve fiyat, ihtiyacınıza göre belirlenir.')+'<section class="container section-after-intro"><div class="packages-grid">'+cards+'</div></section>','/paketler')


def about_page():
    body = intro('Hakkımızda','Seysa Medya; içerik üretimi, tasarım ve dijital iletişim alanlarında hizmet verir.')
    body += '''<section class="container about-layout section-after-intro"><div class="about-logo"><img src="/assets/seysa-logo.svg" width="513" height="195" alt="Seysa Medya"></div><div class="prose"><h2>Nasıl çalışıyoruz?</h2><p>Önce markanızın ihtiyaçlarını ve hedeflerini belirliyoruz. İşin kapsamını, takvimini ve teslimlerini birlikte netleştiriyoruz.</p><p>Sosyal medya, fotoğraf ve video, marka tasarımı, web ve reklam çalışmalarını aynı plan içinde yürütüyoruz.</p><a class="text-link" href="/iletisim">Bizimle iletişime geçin ↗</a></div></section>'''
    return page('Hakkımızda',body,'/hakkimizda')


def contact_page(selected=''):
    options = list(dict.fromkeys([p[0] for p in PACKAGES]+[s['title'] for s in SERVICES.values()]))
    if selected not in options: selected=''
    select = '<option value="">Hizmet seçin</option>'+''.join(f'<option {"selected" if s==selected else ""}>{e(s)}</option>' for s in options)
    body = intro('İletişim','Projenizi ve ihtiyaçlarınızı bize yazın.')
    body += f'''<section class="container contact-layout section-after-intro"><div><h2>E-posta</h2><a class="contact-email" href="mailto:info@seysamedya.com">info@seysamedya.com</a></div><form id="contact-form"><fieldset id="contact-fields" disabled><div class="form-row"><label>Adınız soyadınız<input name="name" autocomplete="name" maxlength="100" required></label><label>E-posta adresiniz<input name="email" type="email" autocomplete="email" maxlength="150" required></label></div><label>Hizmet<select name="service">{select}</select></label><label>Projeniz<textarea name="message" rows="6" maxlength="2000" required></textarea></label><p class="form-note">Form bir e-posta taslağı hazırlar. Gönderimi kendi e-posta uygulamanızdan yaparsınız.</p><button class="button" type="submit">E-posta taslağı hazırla</button><p id="form-status" role="status"></p><div id="draft-panel" hidden><label>Hazırlanan mesaj<textarea id="draft-text" readonly rows="7"></textarea></label><a id="draft-link" class="button" href="mailto:info@seysamedya.com">E-posta uygulamasında aç</a><p class="form-note">Uygulama açılmazsa metni kopyalayıp yukarıdaki adrese gönderebilirsiniz.</p></div></fieldset><noscript><p>Doğrudan e-posta adresimize yazabilirsiniz.</p></noscript></form></section>'''
    return page('İletişim',body,'/iletisim')


ADMIN_TYPES = {'sirketler':('Şirketler','Şirket'), 'projeler':('Projeler','Proje'), 'referanslar':('Referanslar','Referans')}

def admin_shell(title,content,csrf,active='',notice=''):
    links = '<a href="/admin" '+('aria-current="page"' if not active else '')+'>Genel bakış</a>'
    links += ''.join(f'<a href="/admin/{key}" {"aria-current=page" if active==key else ""}>{name[0]}</a>' for key,name in ADMIN_TYPES.items())
    links += '<a href="/admin/hesap" '+('aria-current="page"' if active=='hesap' else '')+'>Hesap</a>'
    message = f'<div class="notice" role="status">{e(notice)}</div>' if notice else ''
    return page(title,f'<div class="admin-layout"><aside class="admin-sidebar"><nav aria-label="Yönetim menüsü">{links}</nav></aside><div class="admin-content">{message}{content}</div></div>',csrf=csrf,admin=True,authenticated=True)


def auth_page(csrf,setup=False,error='',username=''):
    title = 'Yönetici hesabı oluştur' if setup else 'Yönetici girişi'
    hint = '<p>Bu hesabı yalnızca ilk kullanımda oluşturmanız gerekir.</p>' if setup else ''
    return page(title,f'''<section class="auth-card"><h1>{title}</h1>{hint}{f'<p class="error" role="alert">{e(error)}</p>' if error else ''}<form method="post" action="{'/admin/kurulum' if setup else '/admin/giris'}"><input type="hidden" name="csrf" value="{e(csrf)}"><label>Kullanıcı adı<input name="username" value="{e(username)}" required minlength="3" maxlength="80" autocomplete="username"></label><label>Şifre<input name="password" type="password" required {'minlength="12"' if setup else ''} maxlength="256" autocomplete="{'new-password' if setup else 'current-password'}"></label>{'<p class="form-note">En az 12 karakter kullanın.</p><label>Şifre tekrar<input type="password" name="password_confirm" required minlength="12" maxlength="256" autocomplete="new-password"></label>' if setup else ''}<button class="button">{'Hesabı oluştur' if setup else 'Giriş yap'}</button></form></section>''',csrf=csrf,admin=True)


def dashboard(csrf,counts):
    cards=''.join(f'<a class="stat-card" href="/admin/{key}"><span>{title[0]}</span><strong>{counts[key]}</strong></a>' for key,title in ADMIN_TYPES.items())
    content='<h1>Genel bakış</h1><div class="stat-grid">'+cards+'</div><section class="admin-help"><h2>İçerik ekleme</h2><ol><li>Şirketi oluşturun ve logosunu yükleyin.</li><li>Projeyi veya referansı ilgili şirkete bağlayın.</li><li>Hazır olduğunda “Sitede yayınla” seçeneğini işaretleyin.</li></ol><p>Yayınladığınız referansların logoları ana sayfada ve referanslar sayfasında gösterilir.</p></section>'
    return admin_shell('Yönetim paneli',content,csrf)


def record_list(kind,rows,csrf,notice=''):
    title,singular=ADMIN_TYPES[kind]
    content=f'<div class="admin-title"><h1>{title}</h1>{button(singular+" ekle","/admin/"+kind+"/yeni")}</div>'
    if not rows:
        content+=f'<div class="empty-state">Henüz kayıt yok. <a href="/admin/{kind}/yeni">{singular} ekleyin.</a></div>'
    else:
        lines=''
        for r in rows:
            name=r.get('name') or r.get('title') or r.get('company_name')
            logo=r.get('logo') or r.get('image')
            image=f'<img src="{e(logo)}" alt="" width="60" height="42">' if logo else ''
            status=('Yayında' if r['published'] else 'Taslak') if kind!='sirketler' else (r.get('sector') or '—')
            if kind=='referanslar' and r.get('is_sample'): status = 'Örnek · '+status
            lines+=f'<tr><td><div class="record-name">{image}<span>{e(name)}</span></div></td><td>{e(status)}</td><td class="record-actions"><a href="/admin/{kind}/{r["id"]}/duzenle">Düzenle</a><a class="danger-link" href="/admin/{kind}/{r["id"]}/sil">Sil</a></td></tr>'
        content+=f'<div class="table-wrap"><table><thead><tr><th scope="col">{singular}</th><th scope="col">{"Sektör" if kind=="sirketler" else "Durum"}</th><th scope="col">İşlemler</th></tr></thead><tbody>{lines}</tbody></table></div>'
    return admin_shell(title,content,csrf,kind,notice)


def record_form(kind,csrf,companies,record=None,error=''):
    record=record or {}; title=ADMIN_TYPES[kind][1]+(' düzenle' if record.get('id') else ' ekle')
    def field(label,name,required=False,limit=200,textarea=False,typ='text'):
        attrs=f'name="{name}" maxlength="{limit}" '+('required' if required else '')
        control=f'<textarea {attrs} rows="5">{e(record.get(name,""))}</textarea>' if textarea else f'<input type="{typ}" {attrs} value="{e(record.get(name,""))}">'
        return f'<label>{label}{control}</label>'
    def company_select(required=False):
        options='<option value="">Şirket seçin</option>'+''.join(f'<option value="{c["id"]}" {"selected" if str(c["id"])==str(record.get("company_id")) else ""}>{e(c["name"])}</option>' for c in companies)
        return '<label>Şirket<select name="company_id" '+('required' if required else '')+'>'+options+'</select></label>'
    def upload(label,key):
        current=record.get(key,'')
        image=f'<div class="upload-current"><img src="{e(current)}" alt="Mevcut görsel" width="160" height="100"><label class="checkbox"><input name="remove_media" type="checkbox" value="1"> Görseli kaldır</label></div>' if current else ''
        return image+f'<label>{label}<input type="file" name="media" accept="image/png,image/jpeg,image/webp,image/svg+xml"></label><p class="form-note">PNG, JPG, WebP veya SVG. En fazla 5 MB.</p>'
    fields=''
    if kind=='sirketler':
        fields=field('Şirket / kurum adı','name',True)+field('Sektör','sector')+field('Web sitesi (isteğe bağlı)','website',typ='url')+upload('Logo','logo')
    elif kind=='projeler':
        options='<option value="">Hizmet seçin</option>'+''.join(f'<option {"selected" if s["title"]==record.get("service") else ""}>{e(s["title"])}</option>' for s in SERVICES.values())
        fields=field('Proje adı','title',True)+company_select()+f'<label>Hizmet<select name="service">{options}</select></label>'+field('Kısa açıklama','summary',limit=400,textarea=True)+field('Proje açıklaması','body',limit=12000,textarea=True)+upload('Proje görseli','image')
    else:
        fields=company_select(True)+'<p class="form-note">Logo, şirket kaydından alınır. Logoyu değiştirmek için şirketi düzenleyin.</p>'+field('Referans yorumu (isteğe bağlı)','quote',limit=2000,textarea=True)+field('Yorum sahibi / unvanı (isteğe bağlı)','author')
    if kind=='referanslar':
        fields += '<label class="checkbox"><input type="checkbox" name="is_sample" value="1" '+('checked' if record.get('is_sample') else '')+'> Örnek yerleşim (müşteri referansı değildir)</label>'
    if kind!='sirketler':
        fields+=f'<label>Gösterim sırası<input name="position" type="number" min="0" max="9999" value="{e(record.get("position",0))}" required></label><label class="checkbox"><input type="checkbox" name="published" value="1" {"checked" if record.get("published") else ""}> Sitede yayınla</label>'
    action='/admin/'+kind+'/'+(str(record['id'])+'/duzenle' if record.get('id') else 'yeni')
    content=f'<div class="admin-title"><h1>{title}</h1><a href="/admin/{kind}">Listeye dön</a></div>'
    if error: content+=f'<p class="error" role="alert">{e(error)}</p>'
    content+=f'<form class="editor-form" method="post" enctype="multipart/form-data" action="{action}"><input type="hidden" name="csrf" value="{e(csrf)}">{fields}<div class="form-actions"><button class="button">Kaydet</button><a href="/admin/{kind}">Vazgeç</a></div></form>'
    return admin_shell(title,content,csrf,kind)


def delete_page(kind,record,csrf,project_count=0,reference_count=0):
    name=record.get('name') or record.get('title') or record.get('company_name')
    details=f'<p>Bu şirkete bağlı {reference_count} referans da kaldırılır. {project_count} proje korunur; şirket bağlantısı kaldırılır.</p>' if kind=='sirketler' else ''
    content=f'<section class="delete-card"><h1>Kaydı sil</h1><p><strong>{e(name)}</strong> kaydını silmek istediğinizden emin misiniz?</p>{details}<form method="post" action="/admin/{kind}/{record["id"]}/sil"><input type="hidden" name="csrf" value="{e(csrf)}"><div class="form-actions"><button class="button danger-button">Evet, sil</button><a href="/admin/{kind}">Vazgeç</a></div></form></section>'
    return admin_shell('Kaydı sil',content,csrf,kind)


def account_page(csrf,error='',notice=''):
    error_html=f'<p class="error" role="alert">{e(error)}</p>' if error else ''
    content=f'''<h1>Şifre değiştir</h1>{error_html}<form class="editor-form" method="post" action="/admin/hesap"><input name="csrf" type="hidden" value="{e(csrf)}"><label>Mevcut şifre<input type="password" name="current_password" required maxlength="256" autocomplete="current-password"></label><label>Yeni şifre<input type="password" name="password" minlength="12" maxlength="256" required autocomplete="new-password"></label><label>Yeni şifre tekrar<input type="password" name="password_confirm" minlength="12" maxlength="256" required autocomplete="new-password"></label><p class="form-note">En az 12 karakter kullanın. Şifre değişince tüm oturumlar kapatılır.</p><button class="button">Şifreyi değiştir</button></form>'''
    return admin_shell('Hesap',content,csrf,'hesap',notice)


def error_page(status,message):
    return page(str(status),intro(str(status),message)+'<div class="container section-after-intro">'+button('Ana sayfaya dön','/')+'</div>')
