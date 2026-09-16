#!/usr/bin/env python3
"""Seysa Medya: multi-page website with a server-side, persistent admin panel."""
import argparse
import hashlib
import json
import mimetypes
import os
import re
import secrets
import sqlite3
import time
import traceback
import xml.etree.ElementTree as ET
from email import policy
from email.parser import BytesParser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

from seysa import storage, views
from seysa.content import SERVICES

TABLES = {'sirketler':'companies','projeler':'projects','referanslar':'reference_items'}
MAX_BODY = 6 * 1024 * 1024
MAX_IMAGE = 5 * 1024 * 1024


def safe_image(data):
    if not data or len(data)>MAX_IMAGE:
        raise ValueError('Görsel en fazla 5 MB olabilir.')
    if data.startswith(b'\x89PNG\r\n\x1a\n') and len(data)>24: return data, '.png'
    if data.startswith(b'\xff\xd8\xff') and data.endswith(b'\xff\xd9'): return data, '.jpg'
    if data[:4]==b'RIFF' and data[8:12]==b'WEBP': return data, '.webp'
    try:
        text=data.decode('utf-8-sig')
        if re.search(r'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet',text,re.I): raise ValueError()
        root=ET.fromstring(text)
        if root.tag.split('}')[-1]!='svg': raise ValueError()
        allowed={'svg','g','path','circle','ellipse','rect','line','polyline','polygon','text','tspan','defs','style','linearGradient','radialGradient','stop','clipPath','mask','title','desc','use','symbol'}
        for el in root.iter():
            if el.tag.split('}')[-1] not in allowed: raise ValueError()
            for name,val in el.attrib.items():
                name=name.split('}')[-1].lower()
                if name.startswith('on') or name in ('src','base'): raise ValueError()
                if name=='href' and not val.startswith('#'): raise ValueError()
                if re.search(r'url\s*\(\s*[\'"]?\s*(?!#)[^\s]',val,re.I) or re.search(r'javascript\s*:|data\s*:|@import',val,re.I): raise ValueError()
            if el.tag.split('}')[-1]=='style':
                css=el.text or ''
                if re.search(r'url\s*\(|@import|expression\s*\(|javascript\s*:|\\',css,re.I): raise ValueError()
        return ET.tostring(root,encoding='utf-8',xml_declaration=True), '.svg'
    except (UnicodeError, ET.ParseError, ValueError):
        raise ValueError('Geçerli bir PNG, JPG, WebP veya dış kaynak içermeyen SVG yükleyin.')


def video_embed(value):
    parsed = urlsplit(value)
    if parsed.scheme != 'https' or parsed.username or parsed.password:
        raise ValueError('HTTPS ile başlayan bir YouTube veya Vimeo bağlantısı girin.')
    host = parsed.hostname
    key = ''
    if host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        key = parse_qs(parsed.query).get('v', [''])[0] if parsed.path == '/watch' else parsed.path.split('/')[-1] if parsed.path.startswith(('/shorts/', '/embed/')) else ''
    elif host == 'youtu.be': key = parsed.path.strip('/')
    if re.fullmatch(r'[A-Za-z0-9_-]{11}', key): return 'https://www.youtube-nocookie.com/embed/' + key
    if host in ('vimeo.com', 'www.vimeo.com') and re.fullmatch(r'/\d+', parsed.path):
        return 'https://player.vimeo.com/video/' + parsed.path.strip('/')
    raise ValueError('Geçerli bir YouTube veya Vimeo video bağlantısı girin.')


class SiteServer(ThreadingHTTPServer):
    daemon_threads=True
    allow_reuse_address=True


class Handler(BaseHTTPRequestHandler):
    server_version='Seysa'
    def log_message(self, fmt, *args):
        # Do not log query strings, cookies or form values.
        print(f'{self.command} {urlsplit(self.path).path}',flush=True)

    def send(self, body, status=200, content_type='text/html; charset=utf-8', headers=None):
        if isinstance(body,str): body=body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type',content_type)
        self.send_header('Content-Length',str(len(body)))
        if not headers or 'Cache-Control' not in headers:
            self.send_header('Cache-Control','no-store' if '/admin' in self.path or content_type.startswith('text/html') else 'public, max-age=300')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','same-origin')
        self.send_header('X-Frame-Options','DENY')
        csp = "default-src 'none'; script-src 'none'; style-src 'unsafe-inline'; object-src 'none'; base-uri 'none'" if content_type=="image/svg+xml" else "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'"
        if content_type.startswith('text/html'): csp += "; frame-src https://www.youtube-nocookie.com https://player.vimeo.com"
        self.send_header('Content-Security-Policy',csp)
        for key,val in (headers or {}).items(): self.send_header(key,val)
        self.end_headers()
        if self.command!='HEAD': self.wfile.write(body)

    def redirect(self,path,cookie=None):
        headers={'Location':path}
        if cookie: headers['Set-Cookie']=cookie
        self.send('',303,headers=headers)

    def fail(self,status,message):
        self.send(views.error_page(status,message),status)

    def valid_host(self):
        return self.headers.get('Host','').lower() in self.server.allowed_hosts

    def cookie(self,token='',clear=False):
        result='seysa_session='+token+'; Path=/; HttpOnly; SameSite=Strict; Max-Age='+('0' if clear else '43200')
        if self.server.secure: result+='; Secure'
        return result

    def get_session(self):
        try:
            c=SimpleCookie(self.headers.get('Cookie',''))
            token=c['seysa_session'].value if 'seysa_session' in c else ''
            if not re.fullmatch(r'[A-Za-z0-9_-]{43}',token): return None
            hashed=hashlib.sha256(token.encode()).hexdigest()
            with storage.connect() as db:
                row=db.execute('SELECT * FROM sessions WHERE token=? AND expires>?',(hashed,int(time.time()))).fetchone()
            return dict(row) if row else None
        except Exception:
            return None

    def new_session(self,user=None,old=None):
        token=secrets.token_urlsafe(32)
        session={'token':hashlib.sha256(token.encode()).hexdigest(),'csrf':secrets.token_urlsafe(32),'user_id':user,'expires':int(time.time())+43200}
        with storage.connect() as db:
            db.execute('DELETE FROM sessions WHERE expires<?',(int(time.time()),))
            if old: db.execute('DELETE FROM sessions WHERE token=?',(old['token'],))
            db.execute('INSERT INTO sessions(token,csrf,user_id,expires) VALUES(?,?,?,?)',tuple(session.values()))
        return session, self.cookie(token)

    def setup_allowed(self):
        # Initial ownership is established only directly on loopback, never through a proxy.
        return self.server.local_setup and self.client_address[0] in ('127.0.0.1','::1') and not any(self.headers.get(h) for h in ('Forwarded','X-Forwarded-For','X-Forwarded-Host'))

    def read_form(self):
        try: length=int(self.headers.get('Content-Length','0'))
        except ValueError: raise ValueError('İstek okunamadı.')
        gallery_upload=bool(re.fullmatch(r'/admin/projeler/\d+/galeri',urlsplit(self.path).path))
        limit=31*1024*1024 if gallery_upload else MAX_BODY
        if length<=0 or length>limit: raise ValueError('Galeri yüklemesi toplam 30 MB sınırını aşıyor.' if gallery_upload else 'Form en fazla 6 MB olabilir.')
        body=self.rfile.read(length)
        content_type=self.headers.get('Content-Type','')
        fields={}; uploads=[]
        if content_type.startswith('multipart/form-data'):
            msg=BytesParser(policy=policy.default).parsebytes(('Content-Type: '+content_type+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+body)
            if not msg.is_multipart(): raise ValueError('Form okunamadı.')
            for part in msg.iter_parts():
                name=part.get_param('name',header='content-disposition')
                if not name: continue
                data=part.get_payload(decode=True) or b''
                if part.get_filename():
                    if name=='media' and data:
                        uploads.append(data)
                        if len(uploads)>12: raise ValueError('Tek seferde en fazla 12 fotoğraf seçin.')
                else:
                    if len(data)>50000: raise ValueError('Metin çok uzun.')
                    fields[name]=data.decode('utf-8')
        elif content_type.startswith('application/x-www-form-urlencoded'):
            fields={k:v[-1] for k,v in parse_qs(body.decode('utf-8'),keep_blank_values=True,max_num_fields=30).items()}
        else: raise ValueError('Desteklenmeyen form türü.')
        if not gallery_upload and len(uploads)>1: raise ValueError('Bu alan için yalnızca bir görsel seçin.')
        return fields,uploads if gallery_upload else (uploads[0] if uploads else None)

    def record(self,kind,ident):
        with storage.connect() as db:
            if kind=='referanslar':
                row=db.execute('SELECT r.*, c.name AS company_name FROM reference_items r JOIN companies c ON c.id=r.company_id WHERE r.id=?',(ident,)).fetchone()
            else: row=db.execute('SELECT * FROM '+TABLES[kind]+' WHERE id=?',(ident,)).fetchone()
        return dict(row) if row else None

    def companies(self):
        with storage.connect() as db: return [dict(r) for r in db.execute('SELECT * FROM companies ORDER BY name COLLATE NOCASE')]

    def do_HEAD(self): self.do_GET()

    def do_GET(self):
        try:
            if not self.valid_host(): return self.fail(400,'Geçersiz adres.')
            parsed=urlsplit(self.path)
            path=unquote(parsed.path)
            if '\x00' in path or '..' in path.split('/'): return self.fail(404,'Sayfa bulunamadı.')
            if path!='/' and path.endswith('/'): return self.redirect(path.rstrip('/')+('?' + parsed.query if parsed.query else ''))
            if path=='/index.html': return self.redirect('/')
            if path in ('/style.css','/main.js') or path.startswith('/assets/'):
                file=(storage.ROOT/path.lstrip('/')).resolve()
                if path.startswith('/assets/') and not str(file).startswith(str(storage.ROOT/'assets')+os.sep): return self.fail(404,'Dosya bulunamadı.')
                if file.is_file(): return self.send(file.read_bytes(),content_type=mimetypes.guess_type(str(file))[0] or 'application/octet-stream')
                return self.fail(404,'Dosya bulunamadı.')
            if path.startswith('/uploads/'):
                name=path.rsplit('/',1)[-1]
                if not re.fullmatch(r'[a-f0-9]{32}\.(png|jpg|webp|svg)',name): return self.fail(404,'Görsel bulunamadı.')
                file=storage.UPLOADS/name
                if not file.is_file(): return self.fail(404,'Görsel bulunamadı.')
                # Draft-only media requires the same admin authorization as the draft.
                with storage.connect() as db:
                    published=db.execute('SELECT 1 FROM projects WHERE image=? AND published=1 UNION ALL SELECT 1 FROM companies c JOIN reference_items r ON r.company_id=c.id WHERE c.logo=? AND r.published=1 UNION ALL SELECT 1 FROM project_media m JOIN projects p ON p.id=m.project_id WHERE m.url=? AND p.published=1 LIMIT 1',(path,path,path)).fetchone()
                session=self.get_session()
                if not published and not (session and session['user_id']): return self.fail(404,'Görsel bulunamadı.')
                return self.send(file.read_bytes(),content_type=mimetypes.guess_type(str(file))[0],headers={'Cache-Control':'private, no-store'})
            if path.startswith('/admin'): return self.admin_get(path,parsed.query)
            projects,refs=storage.public_data()
            if path=='/': body=views.home(projects,refs)
            elif path=='/hizmetler' or path in SERVICES: body=views.services_page(path)
            elif path=='/projeler': body=views.projects_page(projects)
            elif re.fullmatch(r'/projeler/\d+',path): body=views.projects_page(projects,int(path.rsplit('/',1)[1]))
            elif path=='/referanslar': body=views.references_page(refs)
            elif path=='/paketler': body=views.packages_page()
            elif path=='/hakkimizda': body=views.about_page()
            elif path=='/iletisim': body=views.contact_page(parse_qs(parsed.query).get('hizmet',[''])[0])
            elif path=='/robots.txt': return self.send('User-agent: *\nDisallow: /admin\n',content_type='text/plain; charset=utf-8')
            else: body=None
            if body is None: return self.fail(404,'Aradığınız sayfa bulunamadı.')
            self.send(body)
        except (BrokenPipeError,ConnectionResetError): pass
        except Exception:
            traceback.print_exc()
            self.fail(500,'Sayfa şu anda açılamıyor. Lütfen tekrar deneyin.')

    def admin_get(self,path,query):
        with storage.connect() as db: user=db.execute('SELECT id FROM users LIMIT 1').fetchone()
        session=self.get_session()
        if not user:
            if not self.setup_allowed(): return self.fail(403,'Yönetici hesabı henüz oluşturulmadı. İlk kurulumu sunucuda yerel olarak tamamlayın.')
            cookie=None
            if not session: session,cookie=self.new_session()
            return self.send(views.auth_page(session['csrf'],setup=True),headers={'Set-Cookie':cookie} if cookie else None)
        if not session or not session['user_id']:
            cookie=None
            if not session: session,cookie=self.new_session()
            return self.send(views.auth_page(session['csrf']),headers={'Set-Cookie':cookie} if cookie else None)
        csrf=session['csrf']
        if path=='/admin/site-bilgileri': return self.send(views.settings_page(csrf,'Bilgiler kaydedildi.' if parse_qs(query).get('kaydedildi') else ''))
        gallery_match=re.fullmatch(r'/admin/projeler/(\d+)/galeri',path)
        if gallery_match:
            project=self.record('projeler',int(gallery_match[1]))
            if not project: return self.fail(404,'Proje bulunamadı.')
            with storage.connect() as db: media=[dict(r) for r in db.execute('SELECT * FROM project_media WHERE project_id=? ORDER BY position,id',(project['id'],))]
            return self.send(views.gallery_editor(project,media,csrf))
        if path in ('/admin','/admin/giris','/admin/kurulum'):
            with storage.connect() as db: counts={key:db.execute('SELECT COUNT(*) FROM '+table).fetchone()[0] for key,table in TABLES.items()}
            return self.send(views.dashboard(csrf,counts))
        if path=='/admin/hesap': return self.send(views.account_page(csrf))
        match=re.fullmatch(r'/admin/(sirketler|projeler|referanslar)(?:/(yeni|\d+)(?:/(duzenle|sil))?)?',path)
        if not match: return self.fail(404,'Sayfa bulunamadı.')
        kind,ident,action=match.groups()
        if not ident:
            with storage.connect() as db:
                if kind=='referanslar': sql='SELECT r.*, c.name AS company_name, c.logo FROM reference_items r JOIN companies c ON c.id=r.company_id ORDER BY r.position,r.id DESC'
                else: sql='SELECT * FROM '+TABLES[kind]+' ORDER BY id DESC'
                rows=[dict(r) for r in db.execute(sql)]
            notice={'kaydedildi':'Kayıt kaydedildi.','silindi':'Kayıt silindi.'}.get(parse_qs(query).get('durum',[''])[0],'')
            return self.send(views.record_list(kind,rows,csrf,notice))
        if ident=='yeni' and action is None: return self.send(views.record_form(kind,csrf,self.companies()))
        if not ident.isdigit(): return self.fail(404,'Kayıt bulunamadı.')
        record=self.record(kind,int(ident))
        if not record: return self.fail(404,'Kayıt bulunamadı.')
        if action=='duzenle': return self.send(views.record_form(kind,csrf,self.companies(),record))
        if action=='sil':
            with storage.connect() as db:
                pc=db.execute('SELECT COUNT(*) FROM projects WHERE company_id=?',(ident,)).fetchone()[0] if kind=='sirketler' else 0
                rc=db.execute('SELECT COUNT(*) FROM reference_items WHERE company_id=?',(ident,)).fetchone()[0] if kind=='sirketler' else 0
            return self.send(views.delete_page(kind,record,csrf,pc,rc))
        return self.fail(404,'Sayfa bulunamadı.')

    def do_POST(self):
        try:
            if not self.valid_host(): return self.fail(400,'Geçersiz adres.')
            if self.headers.get('Origin') != self.server.origin: return self.fail(403,'İstek doğrulanamadı. Formu yeniden açın.')
            path=urlsplit(self.path).path
            session=self.get_session()
            if not session: return self.fail(403,'Oturum sona erdi. Formu yeniden açın.')
            fields,upload=self.read_form()
            if not secrets.compare_digest(fields.get('csrf',''),session['csrf']): return self.fail(403,'Form doğrulanamadı. Sayfayı yenileyin.')
            if path in ('/admin/giris','/admin/kurulum'): return self.login(path,fields,session)
            if not session['user_id']: return self.fail(401,'Bu işlem için giriş yapın.')
            if path=='/admin/cikis':
                with storage.connect() as db: db.execute('DELETE FROM sessions WHERE token=?',(session['token'],))
                return self.redirect('/admin',self.cookie(clear=True))
            if path=='/admin/hesap': return self.change_password(fields,session)
            if path=='/admin/site-bilgileri':
                values={k:fields.get(k,'').strip() for k in ('whatsapp','address','instagram','linkedin')}
                if any(len(v)>500 for v in values.values()): raise ValueError('Alanlar en fazla 500 karakter olabilir.')
                values['whatsapp']=re.sub(r'[\s()+-]','',values['whatsapp'])
                if values['whatsapp'] and not re.fullmatch(r'[1-9]\d{9,14}',values['whatsapp']): raise ValueError('Telefonu ülke koduyla girin.')
                for key,hosts in [('instagram',('instagram.com','www.instagram.com')),('linkedin',('linkedin.com','www.linkedin.com','tr.linkedin.com'))]:
                    if values[key]:
                        url=urlsplit(values[key])
                        if url.scheme!='https' or url.hostname not in hosts or url.username or url.password: raise ValueError('Geçerli bir '+key+' HTTPS hesap bağlantısı girin.')
                with storage.connect() as db:
                    for key,value in values.items(): db.execute('INSERT INTO app_meta(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value',('site_'+key,value))
                return self.redirect('/admin/site-bilgileri?kaydedildi=1')
            gallery_match=re.fullmatch(r'/admin/projeler/(\d+)/galeri(?:/(\d+)/sil)?',path)
            if gallery_match: return self.save_gallery(gallery_match,fields,upload)
            match=re.fullmatch(r'/admin/(sirketler|projeler|referanslar)/(yeni|\d+)(?:/(duzenle|sil))?',path)
            if not match: return self.fail(404,'İşlem bulunamadı.')
            kind,ident,action=match.groups()
            current=self.record(kind,int(ident)) if ident.isdigit() else None
            if ident.isdigit() and not current: return self.fail(404,'Kayıt bulunamadı.')
            if action=='sil' and current:
                with storage.connect() as db: db.execute('DELETE FROM '+TABLES[kind]+' WHERE id=?',(ident,))
                return self.redirect('/admin/'+kind+'?durum=silindi')
            if (ident=='yeni' and action is None) or (ident.isdigit() and action=='duzenle'):
                return self.save_record(kind,fields,upload,current,session)
            return self.fail(404,'İşlem bulunamadı.')
        except (ValueError,UnicodeError) as ex:
            self.fail(400,str(ex))
        except (BrokenPipeError,ConnectionResetError): pass
        except Exception:
            traceback.print_exc()
            self.fail(500,'İşlem tamamlanamadı. Geri dönüp bilgilerinizi kontrol ederek tekrar deneyin.')

    def login(self,path,fields,session):
        username=fields.get('username','').strip()
        password=fields.get('password','')
        setup=path.endswith('/kurulum')
        now=int(time.time());ip=self.client_address[0]
        with storage.connect() as db:
            attempt=db.execute('SELECT * FROM login_attempts WHERE ip=?',(ip,)).fetchone()
            user=db.execute('SELECT * FROM users WHERE id=1').fetchone()
        if attempt and attempt['blocked_until']>now:
            return self.send(views.auth_page(session['csrf'],setup,'Çok fazla deneme yapıldı. 10 dakika sonra tekrar deneyin.',username),429)
        if setup:
            if user or not self.setup_allowed(): return self.fail(403,'İlk kurulum kullanılamıyor.')
            error=None
            if not re.fullmatch(r'[\w.@-]{3,80}',username): error='Kullanıcı adı 3–80 karakter olmalı; harf, rakam, nokta, tire veya alt çizgi kullanın.'
            if not 12<=len(password)<=256: error='Şifre 12–256 karakter olmalı.'
            if password!=fields.get('password_confirm'): error='Şifreler eşleşmiyor.'
            if error: return self.send(views.auth_page(session['csrf'],True,error,username),400)
            with storage.connect() as db:
                try: db.execute('INSERT INTO users(id,username,password) VALUES(1,?,?)',(username,storage.password_hash(password)))
                except sqlite3.IntegrityError: return self.fail(409,'Yönetici hesabı zaten oluşturulmuş.')
        else:
            valid=bool(user and username==user['username'] and len(password)<=256 and storage.password_matches(password,user['password']))
            if not valid:
                with storage.connect() as db:
                    failures=(attempt['failures'] if attempt and attempt['blocked_until']==0 else 0)+1
                    db.execute('INSERT INTO login_attempts(ip,failures,blocked_until) VALUES(?,?,?) ON CONFLICT(ip) DO UPDATE SET failures=excluded.failures, blocked_until=excluded.blocked_until',(ip,failures,now+600 if failures>=5 else 0))
                return self.send(views.auth_page(session['csrf'],False,'Kullanıcı adı veya şifre hatalı.',username),401)
        with storage.connect() as db: db.execute('DELETE FROM login_attempts WHERE ip=?',(ip,))
        new,cookie=self.new_session(1,session)
        self.redirect('/admin',cookie)

    def change_password(self,fields,session):
        with storage.connect() as db: user=db.execute('SELECT * FROM users WHERE id=1').fetchone()
        password=fields.get('password',''); current=fields.get('current_password','')
        error=None
        if len(current)>256 or not storage.password_matches(current,user['password']): error='Mevcut şifre hatalı.'
        elif not 12<=len(password)<=256: error='Yeni şifre 12–256 karakter olmalı.'
        elif password!=fields.get('password_confirm'): error='Yeni şifreler eşleşmiyor.'
        if error: return self.send(views.account_page(session['csrf'],error=error),400)
        with storage.connect() as db:
            db.execute('UPDATE users SET password=? WHERE id=1',(storage.password_hash(password),))
            db.execute('DELETE FROM sessions')
        return self.redirect('/admin',self.cookie(clear=True))

    def save_record(self,kind,fields,upload,current,session):
        current=current or {}; values={}; saved_file=None
        try:
            def text(name,limit,required=False):
                val=fields.get(name,'').strip()
                if required and not val: raise ValueError('Lütfen zorunlu alanları doldurun.')
                if len(val)>limit: raise ValueError('Alanlardan biri izin verilen uzunluğu aşıyor.')
                return val
            if kind=='sirketler':
                values=dict(name=text('name',200,True),sector=text('sector',200),website=text('website',200),logo=current.get('logo',''))
                if values['website']:
                    parsed=urlsplit(values['website'])
                    if parsed.scheme not in ('https','http') or not parsed.hostname or parsed.username or parsed.password: raise ValueError('Web sitesi http:// veya https:// ile başlayan geçerli bir adres olmalı.')
            else:
                company_id=fields.get('company_id','')
                if company_id and (not company_id.isdigit() or not any(str(c['id'])==company_id for c in self.companies())): raise ValueError('Geçerli bir şirket seçin.')
                if kind=='referanslar' and not company_id: raise ValueError('Referans için bir şirket seçin.')
                try: position=int(fields.get('position','0'))
                except ValueError: raise ValueError('Gösterim sırası bir sayı olmalı.')
                if not 0<=position<=9999: raise ValueError('Gösterim sırası 0–9999 arasında olmalı.')
                values=dict(company_id=int(company_id) if company_id else None,published=1 if fields.get('published')=='1' else 0,position=position)
                if kind=='projeler':
                    service=text('service',200)
                    if service and service not in [s['title'] for s in SERVICES.values()]: raise ValueError('Geçerli bir hizmet seçin.')
                    values.update(title=text('title',200,True),summary=text('summary',400),body=text('body',12000),service=service,image=current.get('image',''))
                    for key in ('brief','process','result'): values[key]=text(key,8000) if key in fields else current.get(key,'')
                else: values.update(quote=text('quote',2000),author=text('author',200),is_sample=1 if fields.get('is_sample')=='1' else 0)
            media_key='logo' if kind=='sirketler' else 'image' if kind=='projeler' else None
            if media_key:
                if fields.get('remove_media')=='1': values[media_key]=''
                if upload:
                    data,ext=safe_image(upload)
                    saved_file=storage.UPLOADS/(secrets.token_hex(16)+ext)
                    saved_file.write_bytes(data)
                    os.chmod(saved_file,0o600)
                    values[media_key]='/uploads/'+saved_file.name
            with storage.connect() as db:
                if current.get('id'):
                    db.execute('UPDATE '+TABLES[kind]+' SET '+','.join(k+'=?' for k in values)+' WHERE id=?',tuple(values.values())+(current['id'],))
                else:
                    db.execute('INSERT INTO '+TABLES[kind]+'('+','.join(values)+') VALUES('+','.join('?' for k in values)+')',tuple(values.values()))
            return self.redirect('/admin/'+kind+'?durum=kaydedildi')
        except (ValueError,sqlite3.IntegrityError) as ex:
            if saved_file and saved_file.exists(): saved_file.unlink()
            error='Bu şirket zaten referanslar arasında. Mevcut kaydı düzenleyin.' if isinstance(ex,sqlite3.IntegrityError) else str(ex)
            retained={**current,**fields}
            retained['published']=fields.get('published')=='1'
            retained['is_sample']=fields.get('is_sample')=='1'
            if current.get('id'): retained['id']=current['id']
            if upload: error+=' Güvenlik nedeniyle dosyayı yeniden seçmeniz gerekir.'
            return self.send(views.record_form(kind,session['csrf'],self.companies(),retained,error),400)

    def save_gallery(self,match,fields,upload):
        project_id,media_id=match.groups()
        if not self.record('projeler',int(project_id)): return self.fail(404,'Proje bulunamadı.')
        if media_id:
            with storage.connect() as db: db.execute('DELETE FROM project_media WHERE id=? AND project_id=?',(media_id,project_id))
        else:
            caption=fields.get('caption','').strip()
            if len(caption)>250: raise ValueError('Açıklama en fazla 250 karakter olabilir.')
            try: position=int(fields.get('position','0'))
            except ValueError: raise ValueError('Sıra numarası geçerli olmalı.')
            if not 0<=position<=9999: raise ValueError('Sıra numarası 0–9999 arasında olmalı.')
            video=fields.get('video_url','').strip()
            if bool(upload)==bool(video): raise ValueError('Bir fotoğraf veya bir video bağlantısı seçin.')
            saved=[]
            if upload:
                if sum(map(len,upload))>30*1024*1024: raise ValueError('Fotoğrafların toplamı en fazla 30 MB olabilir.')
                images=[safe_image(data) for data in upload]
                if position+len(images)-1>9999: raise ValueError('Başlangıç sırası daha küçük olmalı.')
            else: images=[]
            rows=[]
            try:
                for index,(data,ext) in enumerate(images):
                    file=storage.UPLOADS/(secrets.token_hex(16)+ext)
                    saved.append(file)
                    file.write_bytes(data)
                    os.chmod(file,0o600)
                    rows.append((project_id,'image','/uploads/'+file.name,caption,position+index))
                if not images: rows.append((project_id,'video',video_embed(video),caption,position))
                with storage.connect() as db: db.executemany('INSERT INTO project_media(project_id,kind,url,caption,position) VALUES(?,?,?,?,?)',rows)
            except Exception:
                for file in saved: file.unlink(missing_ok=True)
                raise
        return self.redirect('/admin/projeler/'+project_id+'/galeri')


def make_server(host='127.0.0.1',port=4173,origin=None):
    storage.initialize()
    server=SiteServer((host,port),Handler)
    actual=server.server_address[1]
    server.origin=origin or 'http://127.0.0.1:'+str(actual)
    parsed=urlsplit(server.origin)
    if parsed.scheme not in ('http','https') or not parsed.netloc or parsed.path not in ('','/'):
        server.server_close();raise ValueError('SITE_ORIGIN geçerli bir http/https origin olmalı.')
    server.origin=server.origin.rstrip('/')
    server.allowed_hosts={parsed.netloc.lower()}
    server.secure=parsed.scheme=='https'
    server.local_setup=host in ('127.0.0.1','::1') and parsed.hostname in ('127.0.0.1','localhost','::1')
    return server


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Seysa Medya web sitesi')
    parser.add_argument('--port',type=int,default=int(os.environ.get('PORT','4173')))
    parser.add_argument('--host',default=os.environ.get('HOST','127.0.0.1'))
    args=parser.parse_args()
    server=make_server(args.host,args.port,os.environ.get('SITE_ORIGIN'))
    print('Seysa Medya: '+server.origin,flush=True)
    print('Yönetim: '+server.origin+'/admin',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
