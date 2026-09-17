from html import escape
from urllib.parse import quote
from pathlib import Path
from . import storage
from .content import GROUPS, SERVICES, NAV, PACKAGES
from datetime import date


def e(value):
    return escape(str(value if value is not None else ''), quote=True)


def button(label, url, extra=''):
    return f'<a class="button {extra}" href="{e(url)}">{e(label)} <span aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></a>'


def social_icon(kind):
    paths = {
        'instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor" stroke="none"/>',
        'linkedin': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7.5 10v7M11 17v-7m0 3a3 3 0 0 1 6 0v4"/><circle cx="7.5" cy="7" r=".8" fill="currentColor" stroke="none"/>',
        'whatsapp': '<path d="M20.5 11.8a8.5 8.5 0 0 1-12.6 7.4L3 20.5l1.3-4.7a8.5 8.5 0 1 1 16.2-4Z"/><path d="M8.2 7.4c-.4 0-1.2.8-1.2 1.8 0 2.5 4.2 6.7 6.8 6.7 1 0 1.8-.8 1.9-1.3l-2.1-1.2-.9 1c-1.6-.6-2.8-1.8-3.4-3.3l1-.9-1.2-2.8Z" fill="currentColor" stroke="none"/>',
    }
    return '<svg class="social-icon" aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+paths[kind]+'</svg>'


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
        footer = f'''<footer class="site-footer"><div class="container footer-inner"><a class="brand" href="/">{logo}</a><nav aria-label="Alt menü"><a href="/hizmetler">Hizmetler</a><a href="/projeler">Projeler</a><a href="/referanslar">Referanslar</a><a href="/iletisim">İletişim</a></nav><a href="mailto:info@seysamedya.com">info@seysamedya.com</a></div><div class="container footer-bottom"><span>© 2026 Seysa Medya</span></div></footer>'''
    css_version = (Path(__file__).resolve().parent.parent / 'assets/creative.css').stat().st_mtime_ns
    creative_style = f'<link rel="stylesheet" href="/assets/admin.css?v={(Path(__file__).resolve().parent.parent / "assets/admin.css").stat().st_mtime_ns}">' if admin else f'<link rel="stylesheet" href="/assets/creative.css?v={css_version}">'
    if not admin:
        settings = storage.site_settings()
        socials = ''.join(f'<a href="{e(settings[k])}" target="_blank" rel="noopener noreferrer">{social_icon(k)}{label} <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a>' if settings.get(k) else f'<span class="social-pending">{social_icon(k)}{label}</span>' for k,label in [('instagram','Instagram'),('linkedin','LinkedIn')])
        footer = '<footer class="site-footer balanced-footer"><div class="container footer-grid"><div class="footer-brand"><a class="brand" href="/" aria-label="Seysa Medya">'+logo+'</a><p>Kreatif fikirler.<br>Güçlü görsel iletişim.</p><div class="footer-socials">'+socials+'</div></div><nav aria-label="Alt menü"><span class="eyebrow">KEŞFEDİN</span><a href="/hizmetler">Hizmetler</a><a href="/projeler">Projeler</a><a href="/referanslar">Referanslar</a><a href="/icerik-rehberi">İçerik Rehberi</a><a href="/hakkimizda">Hakkımızda</a></nav><div class="footer-reach"><span class="eyebrow">BİZE ULAŞIN</span><a href="mailto:info@seysamedya.com">info@seysamedya.com</a><address>'+e(settings.get('address',''))+'</address><a class="text-link" href="/iletisim">Projenizi konuşalım <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div></div><div class="container footer-bottom"><span>© 2026 Seysa Medya</span><span>İstanbul</span></div></footer>'
        footer=footer.replace('info@seysamedya.com',e(settings.get('email','info@seysamedya.com')))
        if settings.get('whatsapp'):
            footer += '<a class="whatsapp-link" href="https://wa.me/'+e(settings['whatsapp'])+'" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp ile yazın">'+social_icon('whatsapp')+'<span>WhatsApp</span></a>'
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><meta name="description" content="{e(description or title)}"><title>{e(title)} — Seysa Medya</title><link rel="icon" href="/assets/seysa-logo.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css?v={css_version}">{creative_style}<script defer src="/main.js?v={css_version}"></script></head><body class="{'admin-body' if admin else ''}">{header}<main id="main">{body}</main>{footer}</body></html>'''


def intro(title, description='', parent=None):
    crumbs = '<a href="/">Ana Sayfa</a>'
    if parent:
        crumbs += f'<span aria-hidden="true">/</span><a href="{e(parent[0])}">{e(parent[1])}</a>'
    return f'<div class="page-intro container"><nav class="breadcrumbs" aria-label="Sayfa yolu">{crumbs}<span aria-hidden="true">/</span><span aria-current="page">{e(title)}</span></nav><h1>{e(title)}</h1>{f"<p>{e(description)}</p>" if description else ""}</div>'


def service_cards(items=None):
    items = items if items is not None else [SERVICES['/hizmetler/'+g[0]] for g in GROUPS]
    return '<div class="service-grid visual-grid">' + ''.join(f'''<a class="service-card visual-card" data-tilt="3" href="{s['path']}">{service_image(s['path'])}<span class="visual-card-top"><span class="service-number">{i+1:02d}</span>{service_icon(s['path'])}</span><div class="visual-card-copy"><h2>{e(s['title'])}</h2><p>{e(s['description'])}</p><span class="card-link">Hizmeti keşfet <span aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></span></div></a>''' for i,s in enumerate(items)) + '</div>'


def service_image(path):
    media = {'sosyal-medya-yonetimi': 'social', 'produksiyon': 'production',
             'marka-tasarim': 'design', 'web-dijital': 'digital',
             'digital-marketing': 'marketing', 'brand-setup': 'brand'}
    variations = {'strateji-icerik-plani': 'brand', 'paylasim-hikaye-tasarimi': 'design', 'reels-kisa-video': 'production', 'hesap-topluluk-yonetimi': 'social', 'analiz-raporlama': 'marketing', 'drone': 'drone'}
    name = variations.get(path.rsplit('/', 1)[-1], media.get(path.split('/')[2], 'production'))
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
    for index,p in enumerate(projects):
        image = f'<img src="{e(p["image"])}" alt="{e(p["title"])}" width="680" height="460" loading="lazy">' if p['image'] else '<div class="project-no-image" aria-hidden="true">Seysa Medya</div>'
        cards += f'<a class="project-card portfolio-card" data-project-service="{e(p["service"])}" href="/projeler/{p["id"]}"><div class="portfolio-cover">{image}<span class="portfolio-index">{index+1:02d}</span><span class="portfolio-open" aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></div><div class="portfolio-caption"><span class="meta">{e(p["company_name"] or "Seysa Medya")} / {e(p["service"])}</span><h2>{e(p["title"])}</h2><p>{e(p["summary"])}</p><span class="card-link">Projeyi keşfet <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></div></a>'
    return '<div class="project-grid">'+cards+'</div>'


def home(projects, refs):
    featured = [SERVICES['/hizmetler/'+slug] for slug in ['produksiyon', 'sosyal-medya-yonetimi', 'marka-tasarim', 'web-dijital', 'digital-marketing', 'brand-setup']]
    services = '<section class="container section creative-services"><div class="section-heading"><div><span class="eyebrow">NELER YAPIYORUZ?</span><h2>Fikirden<br><em>son kareye.</em></h2></div><div class="section-summary"><p>Çekim, tasarım ve dijital iletişim.<br>Markanız için birlikte üretiyoruz.</p><a class="text-link" href="/hizmetler">Tüm hizmetler <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div></div>'+service_cards(featured)+'</section>'
    hero = '''<section class="creative-hero"><div class="container creative-hero-inner"><div class="hero-copy"><span class="eyebrow"><i aria-hidden="true"></i> SEYSA MEDYA / KREATİF &amp; PRODÜKSİYON</span><h1>İyi bir fikir.<br><span>Güçlü bir</span><br>iz<span class="orange-dot">.</span></h1><p>Markanızı görünür kılan filmler, tasarımlar ve dijital deneyimler üretiyoruz.</p><div class="hero-actions"><a class="button" href="/iletisim">Teklif al <span aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></a><a class="text-link" href="/projeler">Projeleri incele <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div></div><div class="hero-stage" data-hero-motion><div class="mesh-aura" aria-hidden="true"></div><div class="lens-sculpture" aria-hidden="true"><div class="lens-ring"></div><div class="lens-core"></div></div><a class="hero-shot hero-shot-main" href="/hizmetler/produksiyon"><img src="/assets/media/production.jpg" alt="Profesyonel kamera ve çekim seti" width="1400" height="2100" fetchpriority="high"><span class="shot-label"><span>PRODÜKSİYON</span><span><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></span></a><a class="hero-shot hero-shot-drone" href="/hizmetler/produksiyon/drone"><img src="/assets/media/drone.jpg" alt="Havadan kıyı görüntüsü" width="1400" height="1000"><span class="shot-label"><span>FARKLI BİR AÇI.</span><span><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></span></a><span class="stage-cross" aria-hidden="true"><svg class="ui-icon" viewBox="0 0 24 24"><use href="/assets/icons.svg#plus"/></svg></span></div></div></section><div class="discipline-strip" aria-hidden="true"><div class="discipline-track"><div class="discipline-group"><span>FİKİR</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>PRODÜKSİYON</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>TASARIM</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>DİJİTAL</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>ETKİ</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b></div><div class="discipline-group"><span>FİKİR</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>PRODÜKSİYON</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>TASARIM</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>DİJİTAL</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b><span>ETKİ</span><b><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></b></div></div></div>'''
    services = services.replace('class="container section creative-services"', 'id="hizmetlerimiz" class="container section creative-services"')
    reference_section = ''
    if refs:
        reference_title = 'Referanslar'
        reference_section = '<section class="home-references" aria-label="Referanslar"><div class="container"><h2>'+reference_title+'</h2></div><div class="reference-band compact-references">'+logo_strip(refs)+'</div></section>'
    work = '<section class="container section"><div class="section-heading"><h2>Projeler</h2></div>'+project_cards(projects[:3])+'</section>' if projects else ''
    cta = '<section class="creative-cta"><div class="container"><span class="eyebrow">SIRADAKİ İYİ FİKİR SİZİN OLSUN.</span><a href="/iletisim"><h2>Birlikte<br>üretelim.</h2><span class="creative-orbit" aria-hidden="true"><span class="orbit-ring"></span><span class="orbit-ring"></span><span class="orbit-ring"></span><span class="orbit-spark"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></span><span class="orbit-label">FİKRİNİ PAYLAŞ</span></span></a><p>Projenizi konuşalım. İlk adımı birlikte atalım.</p></div></section>'
    return page('Ana Sayfa', hero+services+reference_section+work+cta, description='Seysa Medya: sosyal medya yönetimi, prodüksiyon, marka tasarımı, web ve dijital pazarlama hizmetleri.')


def services_page(path):
    if path == '/hizmetler':
        body = intro('Hizmetler', 'Markanızın içerik, tasarım ve dijital iletişim ihtiyaçları için çalışıyoruz.')
        body += '<section class="container section-after-intro">'
        for g in GROUPS:
            s = SERVICES['/hizmetler/'+g[0]]
            links = ''.join(f'<a href="{c["path"]}">{e(c["title"])} <span aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></a>' for c in s['children'])
            body += f'<article class="service-directory visual-directory"><div class="directory-cover">{service_image(s["path"])}<div>{service_icon(s["path"])}<h2><a href="{s["path"]}">{e(s["title"])}</a></h2><p>{e(s["description"])}</p><a class="text-link" href="{s["path"]}">Hizmeti inceleyin <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div></div><div class="subservice-links">{links or "<p>İçerik planlama, tasarım, yayın ve topluluk yönetimi.</p>"}</div></article>'
        body += '</section>'
        return page('Hizmetler', '<div class="services-page">'+body+'</div>', path)
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
    return page(s['title'],'<div class="services-page">'+body+'</div>',path,s['description'])


def references_page(refs):
    body = '<section class="container editorial-intro reference-intro"><span class="eyebrow">SEYSA MEDYA</span><h1>REFERANSLAR<span>.</span></h1><p>Markalar, kurumlar ve birlikte üretilen işler.</p></section>'
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
        filters = ''.join('<button type="button" data-project-filter="'+e(service)+'" aria-pressed="false">'+e(service)+'</button>' for service in dict.fromkeys(p['service'] for p in projects if p['service']))
        body='<section class="container editorial-intro portfolio-intro"><span class="eyebrow">SEYSA MEDYA / PORTFÖY</span><h1>FİKİRLERİN<br><em>GÖRÜNÜR HALİ.</em></h1><div class="portfolio-intro-bottom"><p>Çekimden tasarıma, markadan dijitale.<br>Projelerin hikâyelerine ve detaylarına yakından bakın.</p><span>'+str(len(projects))+' proje</span></div></section>'
        if filters: body+='<div class="container portfolio-filters" aria-label="Proje kategorileri"><button type="button" data-project-filter="" aria-pressed="true">Tüm çalışmalar</button>'+filters+'</div>'
        body+='<section class="container section-after-intro portfolio-list">'+project_cards(projects)+'</section>'
        return page('Projeler',body,'/projeler')
    p = next((p for p in projects if p['id']==project_id),None)
    if not p: return None
    body = '<section class="container case-intro"><a class="text-link" href="/projeler"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-left"/></svg> Projelere dön</a><span class="eyebrow">'+e(p['service'] or 'PROJE DETAYI')+'</span><h1>'+e(p['title'])+'</h1><p>'+e(p['summary'])+'</p></section>'
    image = f'<img class="project-cover" src="{e(p["image"])}" alt="{e(p["title"])}" width="1240" height="800">' if p['image'] else ''
    meta = ''.join(f'<div><dt>{label}</dt><dd>{e(value)}</dd></div>' for label,value in [('Şirket',p['company_name']),('Hizmet',p['service'])] if value)
    body += f'<article class="container section-after-intro case-study">{image}<div class="project-detail"><div class="prose"><span class="eyebrow">PROJE HAKKINDA</span><h2>Çalışmaya<br>yakından bakış.</h2>'+''.join('<p>'+e(part)+'</p>' for part in p['body'].split('\n') if part.strip())+f'</div><dl>{meta}</dl></div>'
    for number,key,title in [('01','brief','İhtiyaç & hedef'),('02','process','Yaklaşım & üretim'),('03','result','Sonuç & teslimler')]:
        if p.get(key): body+='<section class="case-chapter"><span>'+number+'</span><h2>'+title+'</h2><div>'+''.join('<p>'+e(part)+'</p>' for part in p[key].split('\n') if part.strip())+'</div></section>'
    body+='</article>'
    if p.get('gallery'):
        entries = ''
        for item in p['gallery']:
            caption = item['caption'] or p['title']
            if item['kind']=='image':
                content = f'<button class="gallery-open" type="button" data-full-image="{e(item["url"])}" data-caption="{e(caption)}" aria-label="{e(caption)} — büyüt"><img src="{e(item["url"])}" alt="{e(caption)}" loading="lazy"><span aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></button>'
            else:
                content = f'<iframe src="{e(item["url"])}" title="{e(caption)}" loading="lazy" allow="fullscreen; picture-in-picture" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
            entries += '<figure class="gallery-'+item['kind']+'">'+content+'<figcaption>'+e(caption)+'</figcaption></figure>'
        body += '<section class="container project-gallery section-after-intro"><div class="section-heading"><h2>Projeden kareler</h2></div><div class="gallery-grid">'+entries+'</div></section><dialog id="image-viewer" aria-label="Proje görseli"><button type="button" class="viewer-close" aria-label="Görseli kapat">Kapat <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#close"/></svg></button><img alt=""><p></p></dialog>'
    other = next((item for item in projects[projects.index(p)+1:]+projects[:projects.index(p)] if item['id']!=p['id']),None)
    if other: body+='<section class="container next-project"><span class="eyebrow">SIRADAKİ PROJE</span><a href="/projeler/'+str(other['id'])+'"><h2>'+e(other['title'])+'</h2><span aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></a></section>'
    body+='<section class="container contact-callout"><h2>Sizin projenizi de konuşalım.</h2>'+button('Birlikte üretelim','/iletisim')+'</section>'
    return page(p['title'],body,'/projeler/'+str(p['id']),p['summary'])


def packages_page():
    cards = ''
    details = [
        ('social', 'DÜZENLİ İLETİŞİM', 'Sosyal kanallarında tutarlı bir görünüm ve düzenli yayın isteyen markalar için.', ['Aylık içerik ve yayın takvimi', 'Paylaşım ve hikâye tasarımları', 'İçerik metinleri ve yayın yönetimi', 'Hesap düzeni ve etkileşim takibi', 'Performans değerlendirmesi'], 'İçerik sayısı ve yönetilecek kanallar birlikte belirlenir.'),
        ('production', 'GÖRSEL ÜRETİM', 'Ürün, mekân veya etkinliğini güçlü görsellerle anlatmak isteyen markalar için.', ['Çekim fikri ve hazırlık planı', 'Fotoğraf ve video prodüksiyonu', 'Reels ve kısa reklam versiyonları', 'Kurgu, renk ve ses düzenlemesi', 'Yayın kanallarına uygun dosya teslimi'], 'Çekim günü, lokasyon, ekip ve teslim sayısı teklifte netleşir.'),
        ('design', 'MARKA BAŞLANGICI', 'Yeni bir marka kuran veya mevcut kimliğini yenileyen işletmeler için.', ['Marka yönü ve görsel kimlik', 'Logo, renk ve tipografi çalışması', 'Kurumsal web sitesi', 'Alan adı ve e-posta kurulum desteği', 'Lansman için temel içerikler'], 'Sayfa sayısı, entegrasyonlar ve dış hizmet ücretleri ayrıca belirlenir.')]
    for (title, desc, scope), (photo, tag, audience, features, note) in zip(PACKAGES, details):
        cards += '<article class="package-card rich-package"><div class="package-cover"><img src="/assets/media/'+photo+'.jpg" alt="" width="700" height="460" loading="lazy"><span>'+tag+'</span></div><div class="package-content"><h2>'+e(title)+'</h2><p>'+audience+'</p><h3>Neler dahil?</h3><ul>'+''.join('<li>'+e(s)+'</li>' for s in features)+'</ul><p class="package-note">'+note+'</p>'+button('Bu paket için teklif al','/iletisim?hizmet='+quote(title))+'</div></article>'
    body = intro('İhtiyacınıza göre,<br>birlikte planlayalım.'.replace('<br>',' '), 'Paketler / Teklif Al — Üretim ve iletişim ihtiyaçlarınıza göre şekillenen üç çalışma alanı.')
    body += '<section class="container section-after-intro"><div class="packages-grid">'+cards+'</div><div class="package-explainer"><h2>Teklif nasıl hazırlanır?</h2><div class="process-grid"><article><span>01</span><h3>İhtiyacı konuşuruz.</h3><p>Hedefinizi, kanallarınızı ve mevcut içeriklerinizi değerlendiririz.</p></article><article><span>02</span><h3>Kapsamı belirleriz.</h3><p>Teslimleri, revizyonları, takvimi ve bütçeyi teklif içinde netleştiririz.</p></article><article><span>03</span><h3>Üretime başlarız.</h3><p>Onaylanan planla ilerler, çalışmaları birlikte değerlendiririz.</p></article></div><p class="form-note">Reklam bütçesi, baskı, lisans ve barındırma gibi dış maliyetler gerektiğinde teklifte ayrıca belirtilir.</p></div></section>'
    return page('Paketler / Teklif Al',body,'/paketler')


def about_page():
    body = intro('Hakkımızda','Seysa Medya; içerik üretimi, tasarım ve dijital iletişim alanlarında hizmet verir.')
    body += '''<section class="container about-editorial section-after-intro"><div class="about-photo"><img src="/assets/media/production.jpg" alt="Prodüksiyon için kamera ve ışık düzeni" width="1400" height="2100"><span>Fikirden yayına.</span></div><div class="about-story"><span class="eyebrow">SEYSA MEDYA</span><h2>Bir markanın<br>anlatacak çok<br><em>şeyi vardır.</em></h2><p>Biz o hikâyenin nasıl görüneceği, nasıl duyulacağı ve insanlara nasıl ulaşacağı üzerine çalışıyoruz.</p><p>Fotoğraf ve filmden marka tasarımına, sosyal medyadan web sitelerine kadar her işi aynı soruyla ele alıyoruz: Bu çalışma markanız için neyi anlatmalı?</p><a class="text-link" href="/hizmetler">Çalışma alanlarımız <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div></section><section class="about-method"><div class="container method-layout"><div class="method-heading"><span class="eyebrow">ÇALIŞMA BİÇİMİMİZ</span><h2>Önce anlarız.<br><em>Sonra üretiriz.</em></h2><p>Her projede net bir hedef, güçlü bir fikir ve planlı bir üretim.</p><span class="method-mark" aria-hidden="true"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></span></div><ol class="method-steps"><li><span class="method-number" aria-hidden="true">01</span><div><span class="eyebrow">KEŞİF &amp; STRATEJİ</span><h3>Dinle.</h3><p>İhtiyaçlarınızı, hedef kitlenizi ve vermek istediğiniz mesajı birlikte netleştiririz.</p><span class="method-delivery">Hedef · Kapsam · Yol haritası</span></div></li><li><span class="method-number" aria-hidden="true">02</span><div><span class="eyebrow">FİKİR &amp; TASARIM</span><h3>Tasarla.</h3><p>Görsel dili, içerik yönünü ve üretim planını aynı hedef etrafında şekillendiririz.</p><span class="method-delivery">Konsept · Görsel dil · Üretim planı</span></div></li><li><span class="method-number" aria-hidden="true">03</span><div><span class="eyebrow">ÜRETİM &amp; TESLİM</span><h3>Hayata geçir.</h3><p>Çekim, tasarım ve dijital uygulamaları planlanan teslimlerle birlikte yürütürüz.</p><span class="method-delivery">Çekim · Tasarım · Yayın</span></div></li></ol></div></section><section class="container section about-values"><div><span class="eyebrow">BİZİM İÇİN ÖNEMLİ OLAN</span><h2>Açık iletişim.<br>Tutarlı üretim.</h2></div><div><article><h3>Net bir kapsam</h3><p>Ne üreteceğimizi, hangi formatlarda teslim edeceğimizi ve takvimi baştan konuşuruz.</p></article><article><h3>Markaya uygun bir dil</h3><p>Her mecrada aynı karakteri koruyan, ihtiyaca özel içerikler tasarlarız.</p></article><article><h3>Birlikte ilerlemek</h3><p>Geri bildirimlerinizi üretim sürecine dahil eder, kararları birlikte veririz.</p></article></div></section><section class="container contact-callout"><h2>Sizin hikâyenizle başlayalım.</h2><a class="button" href="/iletisim">Bize yazın <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></section>'''
    return page('Hakkımızda','<div class="about-page">'+body+'</div>','/hakkimizda')


def contact_page(selected=''):
    options = list(dict.fromkeys([p[0] for p in PACKAGES]+[s['title'] for s in SERVICES.values()]))
    if selected not in options: selected=''
    select = '<option value="">Hizmet seçin</option>'+''.join(f'<option {"selected" if s==selected else ""}>{e(s)}</option>' for s in options)
    body = '<section class="container contact-intro"><span class="eyebrow">İLETİŞİM / YENİ BİR BAŞLANGIÇ</span><h1>Bir fikriniz mi var?<br><em>Konuşalım.</em></h1><p>Bir çekim, yeni bir marka ya da dijitalde yeni bir adım.<br>Ne yapmak istediğinizi anlatın; birlikte şekillendirelim.</p></section>'
    body += f'''<section class="container contact-layout section-after-intro"><div><h2>E-posta</h2><a class="contact-email" href="mailto:info@seysamedya.com">info@seysamedya.com</a></div><form id="contact-form"><fieldset id="contact-fields" disabled><div class="form-row"><label>Adınız soyadınız<input name="name" autocomplete="name" maxlength="100" required></label><label>E-posta adresiniz<input name="email" type="email" autocomplete="email" maxlength="150" required></label></div><label>Hizmet<select name="service">{select}</select></label><label>Projeniz<textarea name="message" rows="6" maxlength="2000" required></textarea></label><p class="form-note">Form bir e-posta taslağı hazırlar. Gönderimi kendi e-posta uygulamanızdan yaparsınız.</p><button class="button" type="submit">E-posta taslağı hazırla</button><p id="form-status" role="status"></p><div id="draft-panel" hidden><label>Hazırlanan mesaj<textarea id="draft-text" readonly rows="7"></textarea></label><a id="draft-link" class="button" href="mailto:info@seysamedya.com">E-posta uygulamasında aç</a><p class="form-note">Uygulama açılmazsa metni kopyalayıp yukarıdaki adrese gönderebilirsiniz.</p></div></fieldset><noscript><p>Doğrudan e-posta adresimize yazabilirsiniz.</p></noscript></form></section>'''
    body = body.replace('class="container contact-layout section-after-intro"', 'class="container contact-layout contact-studio section-after-intro"')
    body = body.replace('<div><h2>E-posta</h2><a class="contact-email"', '<div class="contact-side"><div class="contact-photo"><img src="/assets/media/brand.jpg" alt="Tasarım masası ve renk çalışmaları" width="900" height="600"><span>Birlikte üretelim. <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></div><span class="eyebrow">DOĞRUDAN YAZIN</span><a class="contact-email"')
    body = body.replace('info@seysamedya.com</a></div><form', 'info@seysamedya.com</a><div class="contact-guide"><h3>Nereden başlayalım?</h3><p>Markanızı, ihtiyacınız olan hizmeti ve varsa hedeflediğiniz tarihi paylaşmanız yeterli.</p></div></div><form')
    body = body.replace('<fieldset id="contact-fields" disabled>', '<fieldset id="contact-fields" disabled><div class="form-heading"><span class="eyebrow">PROJENİZİ ANLATIN</span><h2>İlk adımı atalım.</h2><p>Kısa bir notla başlayabilirsiniz.</p></div>')
    address=storage.site_settings().get('address','')
    if address:
        body=body.replace('<div class="contact-guide">','<div class="contact-address"><span class="eyebrow">ADRES</span><p>'+e(address)+'</p><a class="text-link" href="https://www.google.com/maps/search/?api=1&amp;query='+quote(address)+'" target="_blank" rel="noopener noreferrer">Haritada aç <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div><div class="contact-guide">')
    body=body.replace('info@seysamedya.com',e(storage.site_settings().get('email','info@seysamedya.com')))
    return page('İletişim',body,'/iletisim')


ADMIN_TYPES = {'sirketler':('Şirketler','Şirket'), 'projeler':('Projeler','Proje'), 'referanslar':('Referanslar','Referans'), 'icerikler':('İçerik Rehberi','İçerik')}

def admin_shell(title,content,csrf,active='',notice=''):
    links = '<a href="/admin" '+('aria-current="page"' if not active else '')+'>Genel bakış</a>'
    links += ''.join(f'<a href="/admin/{key}" {"aria-current=page" if active==key else ""}>{name[0]}</a>' for key,name in ADMIN_TYPES.items())
    links += '<a href="/admin/hesap" '+('aria-current="page"' if active=='hesap' else '')+'>Hesap</a>'
    links += '<a href="/admin/site-bilgileri" '+('aria-current="page"' if active=='site-bilgileri' else '')+'>Site bilgileri</a>'
    message = f'<div class="notice" role="status">{e(notice)}</div>' if notice else ''
    content='<div class="admin-publish-note"><strong>Yayın bilgisi</strong><span>Kaydettiğiniz değişiklikler yerel siteye yansır. GitHub Pages paylaşım sitesi, yeniden yayınlandığında güncellenir.</span></div>'+content
    return page(title,f'<div class="admin-layout"><aside class="admin-sidebar"><nav aria-label="Yönetim menüsü">{links}</nav></aside><div class="admin-content">{message}{content}</div></div>',csrf=csrf,admin=True,authenticated=True)


def auth_page(csrf,setup=False,error='',username=''):
    title = 'Yönetici hesabı oluştur' if setup else 'Yönetici girişi'
    hint = '<p>Bu hesabı yalnızca ilk kullanımda oluşturmanız gerekir.</p>' if setup else ''
    return page(title,f'''<section class="auth-card"><h1>{title}</h1>{hint}{f'<p class="error" role="alert">{e(error)}</p>' if error else ''}<form method="post" action="{'/admin/kurulum' if setup else '/admin/giris'}"><input type="hidden" name="csrf" value="{e(csrf)}"><label>Kullanıcı adı<input name="username" value="{e(username)}" required minlength="3" maxlength="80" autocomplete="username"></label><label>Şifre<input name="password" type="password" required {'minlength="12"' if setup else ''} maxlength="256" autocomplete="{'new-password' if setup else 'current-password'}"></label>{'<p class="form-note">En az 12 karakter kullanın.</p><label>Şifre tekrar<input type="password" name="password_confirm" required minlength="12" maxlength="256" autocomplete="new-password"></label>' if setup else ''}<button class="button">{'Hesabı oluştur' if setup else 'Giriş yap'}</button></form></section>''',csrf=csrf,admin=True)


def dashboard(csrf,counts):
    cards=''.join(f'<a class="stat-card" href="/admin/{key}"><span>{title[0]}</span><strong>{counts[key]}</strong><small>Kayıtları yönet →</small></a>' for key,title in ADMIN_TYPES.items())
    content='<div class="admin-welcome"><span class="eyebrow">SEYSA MEDYA / YÖNETİM</span><h1>Bugün ne üretelim?</h1><p>İçerikleri hazırlayın, markaları düzenleyin, çalışmalarınızı yayına alın.</p><div class="form-actions">'+button('Yeni yazı','/admin/icerikler/yeni')+button('Referans ekle','/admin/referanslar/yeni')+'</div></div><div class="stat-grid">'+cards+'</div><div class="admin-guide-grid"><section class="admin-help"><h2>Şirket & referans</h2><p>Şirket, ortak marka ve logo kaydıdır. Referans ise bu markanın sitede nerede ve hangi sırada görüneceğini belirler.</p><p>Referans eklerken yeni şirketi ve logosunu aynı formda oluşturabilirsiniz. Şirket kaydı tek başına sitede görünmez.</p></section><section class="admin-help"><h2>İçerik Rehberi</h2><p>Rehberleri ve sektör haberlerini taslak olarak hazırlayın. Kapağı, başlıkları ve kaynakları ekleyin; önizlemede kontrol edip yayınlayın.</p><a class="text-link" href="/admin/icerikler">Yazılara git</a></section></div>'
    return admin_shell('Yönetim paneli',content,csrf)


def record_list(kind,rows,csrf,notice='',filters=None):
    filters=filters or {}; q=filters.get('q','').strip(); status=filters.get('status','')
    title,singular=ADMIN_TYPES[kind]
    total=len(rows)
    if q: rows=[r for r in rows if q.casefold() in ' '.join(str(r.get(k) or '') for k in ('name','title','company_name','sector','topic')).casefold()]
    if status in ('published','draft') and kind!='sirketler': rows=[r for r in rows if bool(r['published'])==(status=='published')]
    if kind=='sirketler' and status=='unlinked': rows=[r for r in rows if not r.get('reference_id')]
    descriptions={'sirketler':'Logo ve şirket bilgilerini tek yerde tutun. Bağlı projeleri ve referans durumunu buradan takip edin.','referanslar':'Ana sayfadaki logo şeridini ve referans sayfasını yönetin. Aynı şirket için tek kayıt yeterli.','projeler':'Projelerinizi, yayın durumlarını ve fotoğraf galerilerini yönetin.','icerikler':'Rehberler ve sektör haberleri: taslak hazırlayın, önizleyin, yayınlayın.'}
    content=f'<div class="admin-title"><div><span class="eyebrow">İÇERİK YÖNETİMİ</span><h1>{title}</h1></div>{button(singular+" ekle","/admin/"+kind+"/yeni")}</div><p class="admin-description">{descriptions[kind]}</p>'
    options=[('','Tüm kayıtlar')]+([('unlinked','Referansı olmayanlar')] if kind=='sirketler' else [('published','Yayında'),('draft','Taslak')])
    select=''.join(f'<option value="{key}" '+('selected' if status==key else '')+f'>{label}</option>' for key,label in options)
    content+=f'<form class="admin-filters" method="get" action="/admin/{kind}"><label>Kayıtlarda ara<input name="q" type="search" value="{e(q)}" placeholder="Ad veya başlık" maxlength="200"></label><label>Durum<select name="status">{select}</select></label><button class="button">Filtrele</button><a href="/admin/{kind}">Temizle</a></form><p class="record-count">{total} kayıttan {len(rows)} gösteriliyor</p>'
    if not rows:
        content+='<div class="empty-state">'+('Bu filtrelere uyan kayıt yok. Filtreleri temizleyip tekrar deneyin.' if total else 'Henüz kayıt yok. İlk kaydınızı yukarıdaki düğmeyle ekleyin.')+'</div>'
    else:
        lines=''
        for r in rows:
            name=r.get('name') or r.get('title') or r.get('company_name'); logo=r.get('logo') or r.get('image')
            image=f'<img src="{e(logo)}" alt="" width="72" height="54">' if logo else '<span class="record-placeholder" aria-hidden="true">'+e(name[:1])+'</span>'
            detail=''; extra=''
            if kind=='sirketler':
                ref_id=r.get('reference_id')
                status_label=('Referans yayında' if r.get('reference_published') else 'Referans taslak') if ref_id else 'Referans yok'
                state='published' if r.get('reference_published') else 'draft'
                detail=e(r.get('sector') or 'Sektör belirtilmedi')+' · '+str(r.get('project_count',0))+' proje'
                extra=f'<a href="/admin/referanslar/{ref_id}/duzenle">Referansı düzenle</a>' if ref_id else f'<a href="/admin/referanslar/yeni?sirket={r["id"]}">Referans ekle</a>'
            else:
                status_label='Yayında' if r['published'] else 'Taslak'; state='published' if r['published'] else 'draft'
                detail='Sıra: '+str(r.get('position',0))
                if kind=='referanslar':
                    if r.get('is_sample'): detail+=' · Örnek yerleşim'
                    if not logo: detail+=' · Logo eksik'
                    extra=f'<a href="/admin/sirketler/{r["company_id"]}/duzenle">Şirket bilgileri</a>'
                if kind=='icerikler':
                    detail=('Rehber' if r['category']=='rehberler' else 'Sektör haberi')+' · '+e(r['date'])
                    extra=f'<a href="/admin/icerikler/{r["id"]}/onizle" target="_blank" rel="noopener">Önizle</a>'
                if kind=='projeler': extra=f'<a href="/admin/projeler/{r["id"]}/galeri">Galeri</a>'
            lines+=f'<tr><td><div class="record-name">{image}<div><strong>{e(name)}</strong><small>{detail}</small></div></div></td><td><span class="status-badge {state}">{status_label}</span></td><td class="record-actions">{extra}<a href="/admin/{kind}/{r["id"]}/duzenle">Düzenle</a><a class="danger-link" href="/admin/{kind}/{r["id"]}/sil">Sil</a></td></tr>'
        content+=f'<div class="table-wrap"><table><thead><tr><th scope="col">{singular}</th><th scope="col">Durum</th><th scope="col">İşlemler</th></tr></thead><tbody>{lines}</tbody></table></div>'
    return admin_shell(title,content,csrf,kind,notice)


def record_form(kind,csrf,companies,record=None,error=''):
    if kind=='icerikler': return article_form(csrf,record,error)
    record=record or {}; title=ADMIN_TYPES[kind][1]+(' düzenle' if record.get('id') else ' ekle')
    def field(label,name,required=False,limit=200,textarea=False,typ='text'):
        attrs=f'name="{name}" maxlength="{limit}" '+('required' if required else '')
        control=f'<textarea {attrs} rows="5">{e(record.get(name,""))}</textarea>' if textarea else f'<input type="{typ}" {attrs} value="{e(record.get(name,""))}">'
        return f'<label>{label}{control}</label>'
    def company_select(required=False):
        options='<option value="">Yeni şirket oluştur / şirket seçin</option>'+''.join(f'<option value="{c["id"]}" {"selected" if str(c["id"])==str(record.get("company_id")) else ""}>{e(c["name"])}</option>' for c in companies if kind!='referanslar' or not c.get('reference_id') or str(c['id'])==str(record.get('company_id')))
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
        fields=field('Proje adı','title',True)+company_select()+f'<label>Hizmet<select name="service">{options}</select></label>'+field('Kısa açıklama','summary',limit=400,textarea=True)+field('Proje açıklaması','body',limit=12000,textarea=True)+upload('Proje görseli','image')+field('İhtiyaç ve hedef (isteğe bağlı)','brief',limit=8000,textarea=True)+field('Yaklaşım ve üretim süreci (isteğe bağlı)','process',limit=8000,textarea=True)+field('Sonuç ve teslimler (isteğe bağlı)','result',limit=8000,textarea=True)
    else:
        fields='<section class="form-section"><h2>1. Şirket ve logo</h2>'+company_select()+'<p class="form-note">Referansı olmayan bir şirket seçin veya aşağıdan yeni şirket oluşturun. Her şirketin tek referans kaydı vardır.</p><details'+(' open' if not record.get('company_id') else '')+'><summary>Yeni şirket oluştur</summary>'+field('Yeni şirket / kurum adı','new_company_name')+field('Sektör (isteğe bağlı)','new_company_sector')+'</details>'+upload('Logo yükle veya değiştir','logo')+'<p class="form-note">Seçili şirketin logosu kullanılır. Buradan yüklediğiniz logo şirket kaydını da günceller.</p></section><section class="form-section"><h2>2. Referans bilgileri</h2>'+field('Referans yorumu (isteğe bağlı)','quote',limit=2000,textarea=True)+field('Yorum sahibi / unvanı (isteğe bağlı)','author')
    if kind=='referanslar':
        fields += '</section><label class="checkbox"><input type="checkbox" name="is_sample" value="1" '+('checked' if record.get('is_sample') else '')+'> Örnek yerleşim (müşteri referansı değildir)</label>'
    if kind!='sirketler':
        fields+='<p class="form-note">Düşük sıra numarası önce gösterilir. Taslaklar ziyaretçilere görünmez.</p>'
        fields+=f'<label>Gösterim sırası<input name="position" type="number" min="0" max="9999" value="{e(record.get("position",0))}" required></label><label class="checkbox"><input type="checkbox" name="published" value="1" {"checked" if record.get("published") else ""}> Sitede yayınla</label>'
    action='/admin/'+kind+'/'+(str(record['id'])+'/duzenle' if record.get('id') else 'yeni')
    content=f'<div class="admin-title"><h1>{title}</h1><a href="/admin/{kind}">Listeye dön</a></div>'
    if error: content+=f'<p class="error" role="alert">{e(error)}</p>'
    content+=f'<form class="editor-form" method="post" enctype="multipart/form-data" action="{action}"><input type="hidden" name="csrf" value="{e(csrf)}">{fields}<div class="form-actions"><button class="button">Kaydet</button><a href="/admin/{kind}">Vazgeç</a></div></form>'
    if kind=='projeler':
        content += '<section class="admin-help"><h2>Fotoğraf & video galerisi</h2>'+(button('Galeriyi düzenle', '/admin/projeler/'+str(record['id'])+'/galeri') if record.get('id') else '<p>Önce projeyi kaydedin. Düzenleme sayfasından galeriye fotoğraf ve video ekleyebilirsiniz.</p>')+'</section>'
    return admin_shell(title,content,csrf,kind)


def article_form(csrf,record=None,error=''):
    r=record or {}; editing=bool(r.get('id')); title='İçeriği düzenle' if editing else 'Yeni içerik'
    def field(label,key,limit=200,area=False,required=False,typ='text',default=''):
        attrs=f'name="{key}" maxlength="{limit}"'+(' required' if required else '')
        control=f'<textarea {attrs} rows="'+('18' if key=='body' else '3')+f'">{e(r.get(key,default))}</textarea>' if area else f'<input {attrs} type="{typ}" value="{e(r.get(key,default))}">'
        return '<label>'+label+control+'</label>'
    action='/admin/icerikler/'+(str(r['id'])+'/duzenle' if editing else 'yeni')
    options=''.join(f'<option value="{key}" '+('selected' if r.get('category','rehberler')==key else '')+f'>{label}</option>' for key,label in [('rehberler','Rehberler'),('sektor-haberleri','Sektör Haberleri')])
    image_options='<option value="keep">Mevcut kapağı koru</option>' if r.get('image') else ''
    image_options+=''.join(f'<option value="{key}" '+('selected' if r.get('image_choice')==key else '')+f'>{label}</option>' for key,label in [('social','Sosyal medya'),('design','Tasarım'),('production','Prodüksiyon'),('digital','Dijital'),('marketing','Pazarlama'),('brand','Marka')])
    image=f'<img class="editor-cover" src="{e(r["image"])}" alt="Mevcut kapak">' if r.get('image') else ''
    preview=f'<a class="button" href="/admin/icerikler/{r["id"]}/onizle" target="_blank" rel="noopener">Kaydedilmiş yazıyı önizle</a>' if editing else '<p class="form-note">İlk kayıttan sonra yazıyı önizleyebilirsiniz.</p>'
    content=f'<div class="admin-title"><div><span class="eyebrow">İÇERİK REHBERİ</span><h1>{title}</h1></div><a href="/admin/icerikler">Listeye dön</a></div>'
    if error: content+=f'<p class="error" role="alert">{e(error)}</p>'
    content+=f'<form class="article-editor" data-new="{str(not editing).lower()}" method="post" enctype="multipart/form-data" action="{action}"><input type="hidden" name="csrf" value="{e(csrf)}"><div class="editor-main"><section class="editor-panel"><h2>Yazının ana hatları</h2>'+field('Başlık','title',required=True)+field('Sayfa adresi','slug',160,required=True)+'<p class="form-note">Örnek: instagram-reels-icin-5-ipucu. Yayındaki bir yazının adresini değiştirirseniz eski bağlantısı çalışmaz.</p>'+field('Kısa açıklama','summary',400,area=True)+field('Konu etiketi','topic',100)+'</section><section class="editor-panel"><h2>İçerik</h2><button class="plain-button" type="button" data-add-heading hidden>Bölüm başlığı ekle</button><p class="form-note">Bölüm başlıklarına iki diyez ve boşlukla başlayın: <strong>## İlk kareyi planlayın</strong>. Alt satırlara metninizi yazın. HTML gerekmez.</p>'+field('Yazı metni','body',30000,area=True)+field('Son öneri / bir sonraki adım','takeaway',1000,area=True)+'</section><section class="editor-panel"><h2>Kaynak</h2><p class="form-note">Sektör haberlerini yayınlamak için kaynak bağlantısı gereklidir.</p>'+field('Kaynak adı','source_label')+field('Kaynak bağlantısı','source_url',1000,typ='url')+'</section></div><aside class="editor-side"><section class="editor-panel"><h2>Yayın ayarları</h2><label>Kategori<select name="category">'+options+'</select></label>'+field('Yazı tarihi','date',10,required=True,typ='date',default=date.today().isoformat())+'<p class="form-note">Tarih yazıda gösterilir; otomatik yayın zamanlaması yapmaz.</p><label>Gösterim sırası<input type="number" name="position" min="0" max="9999" value="'+e(r.get('position',0))+'" required></label><label class="checkbox"><input type="checkbox" name="published" value="1" '+('checked' if r.get('published') else '')+'> Sitede yayınla</label><p class="form-note">İşaretli değilse taslak olarak kaydedilir. Küçük sıra numarası önce gösterilir.</p><button class="button" type="submit">Değişiklikleri kaydet</button>'+preview+'</section><section class="editor-panel"><h2>Kapak görseli</h2>'+image+'<label>Hazır kapak<select name="image_choice">'+image_options+'</select></label><label>Veya kendi kapağınızı yükleyin<input type="file" name="media" accept="image/png,image/jpeg,image/webp,image/svg+xml"></label><p class="form-note">PNG, JPG, WebP veya SVG; en fazla 5 MB. Yüklediğiniz dosya hazır kapağın yerine geçer.</p></section></aside></form>'
    return admin_shell(title,content,csrf,'icerikler')


def gallery_editor(project,media,csrf):
    base='/admin/projeler/'+str(project['id'])+'/galeri'
    body='<div class="admin-title"><h1>'+e(project['title'])+' — Galeri</h1><a href="/admin/projeler/'+str(project['id'])+'/duzenle">Projeye dön</a></div>'
    body+='<form class="editor-form" method="post" enctype="multipart/form-data" action="'+base+'"><input type="hidden" name="csrf" value="'+e(csrf)+'"><h2>Fotoğraflar veya video ekle</h2><label>Fotoğraflar<input type="file" multiple name="media" accept="image/png,image/jpeg,image/webp,image/svg+xml"></label><p class="form-note">Birden fazla fotoğraf seçebilirsiniz: en fazla 12 fotoğraf, her biri 5 MB, toplam 30 MB. Video için aşağıya YouTube veya Vimeo bağlantısı girin.</p><label>Video bağlantısı<input name="video_url" type="url" maxlength="500" placeholder="https://..."></label><label>Açıklama<input name="caption" maxlength="250"></label><label>Başlangıç sırası<input name="position" type="number" min="0" max="9999" value="0" required></label><button class="button">Galeriye ekle</button></form><div class="admin-gallery">'
    for item in media:
        preview='<img src="'+e(item['url'])+'" alt="" width="240" height="160">' if item['kind']=='image' else '<span>Video</span>'
        body+='<article>'+preview+'<p>'+e(item['caption'] or 'Açıklamasız')+'</p><small>Sıra: '+str(item['position'])+'</small><form method="post" action="'+base+'/'+str(item['id'])+'/sil"><input type="hidden" name="csrf" value="'+e(csrf)+'"><button class="plain-button">Galeriden kaldır</button></form></article>'
    body+='</div><p class="form-note">Galeri, proje yayındaysa ziyaretçilere görünür. Sırayı veya açıklamayı değiştirmek için öğeyi kaldırıp yeniden ekleyebilirsiniz.</p>'
    return admin_shell('Proje galerisi',body,csrf,'projeler')


def delete_page(kind,record,csrf,project_count=0,reference_count=0):
    name=record.get('name') or record.get('title') or record.get('company_name')
    details=f'<p>Bu şirkete bağlı {reference_count} referans da kaldırılır. {project_count} proje korunur; şirket bağlantısı kaldırılır.</p>' if kind=='sirketler' else ''
    content=f'<section class="delete-card"><h1>Kaydı sil</h1><p><strong>{e(name)}</strong> kaydını silmek istediğinizden emin misiniz?</p>{details}<form method="post" action="/admin/{kind}/{record["id"]}/sil"><input type="hidden" name="csrf" value="{e(csrf)}"><div class="form-actions"><button class="button danger-button">Evet, sil</button><a href="/admin/{kind}">Vazgeç</a></div></form></section>'
    return admin_shell('Kaydı sil',content,csrf,kind)


def account_page(csrf,error='',notice=''):
    error_html=f'<p class="error" role="alert">{e(error)}</p>' if error else ''
    content=f'''<h1>Şifre değiştir</h1>{error_html}<form class="editor-form" method="post" action="/admin/hesap"><input name="csrf" type="hidden" value="{e(csrf)}"><label>Mevcut şifre<input type="password" name="current_password" required maxlength="256" autocomplete="current-password"></label><label>Yeni şifre<input type="password" name="password" minlength="12" maxlength="256" required autocomplete="new-password"></label><label>Yeni şifre tekrar<input type="password" name="password_confirm" minlength="12" maxlength="256" required autocomplete="new-password"></label><p class="form-note">En az 12 karakter kullanın. Şifre değişince tüm oturumlar kapatılır.</p><button class="button">Şifreyi değiştir</button></form>'''
    return admin_shell('Hesap',content,csrf,'hesap',notice)


def settings_page(csrf,notice='',error='',values=None):
    settings=values if values is not None else storage.site_settings()
    fields=''.join('<label>'+label+'<input name="'+key+'" value="'+e(settings.get(key,''))+'" maxlength="500" '+('type="url"' if key in ('instagram','linkedin') else '')+'></label>' for key,label in [('email','İletişim e-postası'),('whatsapp','WhatsApp numarası (ülke koduyla, ör. 905xxxxxxxxx)'),('address','Adres'),('instagram','Instagram hesap bağlantısı'),('linkedin','LinkedIn hesap bağlantısı')])
    return admin_shell('Site bilgileri','<h1>Site bilgileri</h1><p class="admin-description">İletişim sayfası, footer ve sosyal bağlantılar aynı bilgileri kullanır.</p>'+('<p class="error" role="alert">'+e(error)+'</p>' if error else '')+'<form class="editor-form" method="post" action="/admin/site-bilgileri"><input type="hidden" name="csrf" value="'+e(csrf)+'">'+fields+'<p class="form-note">Boş bırakılan sosyal medya alanları bağlantı olarak yayınlanmaz. WhatsApp numarasını boşaltırsanız düğme gizlenir.</p><button class="button">Kaydet</button></form>',csrf,'site-bilgileri',notice)


def error_page(status,message):
    if status == 404:
        body = '<section class="container missing-page"><div class="missing-art" aria-hidden="true"><span>4</span><span class="missing-lens"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#spark"/></svg></span><span>4</span></div><span class="eyebrow">404 / SAYFA BULUNAMADI</span><h1>Bu sayfa<br><em>kadrajdan çıkmış.</em></h1><p>Kamerayı çevirdik, burada da yok. Bağlantı değişmiş olabilir.<br>Gelin, sizi doğru sahneye alalım.</p><div class="missing-actions">'+button('Ana sayfaya dön','/')+'<a class="text-link" href="/icerik-rehberi">Hazır gelmişken bir fikir alın <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></div></section>'
        return page('404 · Sayfa bulunamadı', body, '/404')
    return page(str(status),intro(str(status),message)+'<div class="container section-after-intro">'+button('Ana sayfaya dön','/')+'</div>')


def journal_card(item):
    return f'''<a class="journal-card" href="/icerik-rehberi/{e(item['slug'])}"><div class="journal-cover"><img src="{e(item['image'])}" alt="" width="1000" height="700" loading="lazy"><span>{'REHBER' if item['category']=='rehberler' else 'SEKTÖR HABERİ'} <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></span></div><div class="journal-card-copy"><span class="eyebrow">{e(item['topic'])}</span><h2>{e(item['title'])}</h2><p>{e(item['summary'])}</p><time datetime="{item['date']}">{item['date_label']}</time></div></a>'''


def journal_page(path='/icerik-rehberi', preview=None):
    articles=storage.public_articles()
    selected = path.rsplit('/', 1)[-1]
    categories = [('icerik-rehberi','Tümü','/icerik-rehberi'), ('rehberler','Rehberler','/icerik-rehberi/rehberler'), ('sektor-haberleri','Sektör Haberleri','/icerik-rehberi/sektor-haberleri')]
    if path in [c[2] for c in categories]:
        items = articles if selected == 'icerik-rehberi' else [a for a in articles if a['category']==selected]
        title = 'İçerik Rehberi' if selected == 'icerik-rehberi' else next(c[1] for c in categories if c[0]==selected)
        tabs = ''.join(f'<a href="{url}"'+(' aria-current="page"' if key==selected else '')+f'>{label}</a>' for key,label,url in categories)
        body = '<section class="container editorial-intro journal-intro"><span class="eyebrow">SEYSA MEDYA / FİKİR NOTLARI</span><h1>'+('İÇERİK<br><em>REHBERİ.</em>' if selected=='icerik-rehberi' else e(title).upper()+'.')+'</h1><p>Daha iyi içerikler için pratik fikirler.<br>Sosyal medya, prodüksiyon ve dijital dünyadan notlar.</p></section><section class="container journal-list"><nav class="journal-tabs" aria-label="İçerik kategorileri">'+tabs+'</nav><div class="journal-grid">'+''.join(journal_card(a) for a in items)+'</div></section>'
        return page(title, body, path, 'İçerik pazarlaması rehberleri, Reels ipuçları ve kaynaklı sektör haberleri.')
    item = preview or next((a for a in articles if a['slug']==selected),None)
    if not item or path != '/icerik-rehberi/'+selected:
        return None
    count = sum(len(text.split()) for _,text in item['sections'])
    minutes = max(1, (count+149)//150)
    toc = ''.join(f'<a href="#bolum-{i}">{e(title)}</a>' for i,(title,_) in enumerate(item['sections'],1))
    sections = ''.join(f'<section id="bolum-{i}"><h2>{e(title)}</h2><p>{e(text)}</p></section>' for i,(title,text) in enumerate(item['sections'],1))
    takeaway = '<div class="journal-takeaway"><span class="eyebrow">BİR SONRAKİ ADIM</span><p>'+e(item['takeaway'])+'</p></div>' if item['takeaway'] else ''
    source = ''
    if item.get('source'):
        source = f'<p class="journal-source">Kaynak: <a href="{e(item["source"][1])}" target="_blank" rel="noopener noreferrer">{e(item["source"][0])} <svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-up-right"/></svg></a></p>'
    related = [a for a in articles if a['slug'] != selected and a['category']==item['category']][:2]
    body = f'''<article class="container journal-article"><header><a class="text-link" href="/icerik-rehberi"><svg class="ui-icon" aria-hidden="true" focusable="false" viewBox="0 0 24 24"><use href="/assets/icons.svg#arrow-left"/></svg> İçerik Rehberi</a><span class="eyebrow">{e(item['topic'])}</span><h1>{e(item['title'])}</h1><p class="journal-lead">{e(item['summary'])}</p><div class="journal-meta"><span>Seysa Medya</span><time datetime="{item['date']}">{item['date_label']}</time><span>{minutes} dk okuma</span></div></header><img class="journal-hero" src="{e(item['image'])}" alt="" width="1400" height="700"><div class="journal-reading"><aside><span class="eyebrow">BU YAZIDA</span><nav aria-label="Yazı içindekiler">{toc}</nav></aside><div class="journal-prose">{sections}{takeaway}{source}</div></div></article><section class="container journal-related"><h2>Bir fikir daha.</h2><div class="journal-grid">{''.join(journal_card(a) for a in related)}</div></section><section class="container contact-callout"><h2>Bu fikirleri markanıza uyarlayalım.</h2>{button('Birlikte planlayalım','/iletisim')}</section>'''
    if preview: body='<div class="preview-banner">Yönetici önizlemesi · '+('Yayında' if item['published'] else 'Taslak')+' · <a href="/admin/icerikler/'+str(item['id'])+'/duzenle">Düzenlemeye dön</a></div>'+body
    return page(item['title'], body, path, item['summary'])
