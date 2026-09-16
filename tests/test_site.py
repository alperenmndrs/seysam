"""End-to-end HTTP and persistence checks, isolated from real website data."""
import base64
import hashlib
import http.client
import re
import tempfile
import threading
import unittest
from html.parser import HTMLParser
from pathlib import Path
import server
from seysa import storage
from seysa.content import SERVICES, NAV
from seysa.journal import ARTICLES

PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')

class Client:
    def __init__(self,port): self.port=port;self.cookie=''
    def request(self,path,fields=None,origin=None,upload=None,csrf=True):
        headers={};body=None
        if self.cookie: headers['Cookie']=self.cookie
        if fields is not None:
            headers['Origin']=origin or f'http://127.0.0.1:{self.port}'
            if upload:
                boundary='SeysaTestBoundary'
                body=b''
                for k,v in fields.items(): body+=f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
                for photo in (upload if isinstance(upload,list) else [upload]):
                    body+=f'--{boundary}\r\nContent-Disposition: form-data; name="media"; filename="logo.png"\r\nContent-Type: image/png\r\n\r\n'.encode()+photo+b'\r\n'
                body+=f'--{boundary}--\r\n'.encode()
                headers['Content-Type']='multipart/form-data; boundary='+boundary
            else:
                from urllib.parse import urlencode
                body=urlencode(fields).encode(); headers['Content-Type']='application/x-www-form-urlencoded'
        con=http.client.HTTPConnection('127.0.0.1',self.port,timeout=10)
        con.request('POST' if fields is not None else 'GET',path,body,headers)
        response=con.getresponse();data=response.read();status=response.status;out=dict(response.getheaders())
        if 'Set-Cookie' in out:self.cookie=out['Set-Cookie'].split(';')[0]
        con.close()
        return status,data,out
    def token(self):
        status,data,_=self.request('/admin')
        return re.search(rb'name="csrf" value="([^"]+)"',data).group(1).decode()

class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='seysa-tests-')
        storage.DATA=Path(self.temp.name); storage.DB=storage.DATA/'site.sqlite3'; storage.UPLOADS=storage.DATA/'uploads'
        server.Handler.log_message=lambda *args:None
        self.http=server.make_server(port=0)
        self.thread=threading.Thread(target=self.http.serve_forever,daemon=True);self.thread.start()
        self.client=Client(self.http.server_address[1])
    def tearDown(self):
        self.http.shutdown();self.http.server_close();self.thread.join();self.temp.cleanup()
    def setup_admin(self):
        fields={'csrf':self.client.token(),'username':'test-admin','password':'Test-only-password-2026','password_confirm':'Test-only-password-2026'}
        self.assertEqual(self.client.request('/admin/kurulum',fields)[0],303)
        return self.client.token()
    def test_public_routes_and_private_files(self):
        for path in [p for p,t in NAV]+list(SERVICES):
            with self.subTest(path=path):
                status,data,headers=self.client.request(path)
                self.assertEqual(status,200)
                self.assertEqual(data.count(b'<h1'),1)
                self.assertIn(b'/assets/seysa-logo.svg',data)
                self.assertIn('script-src',headers['Content-Security-Policy'])
        for path in ['/server.py','/.data/site.sqlite3','/archive/original-static/index.html','/../README.md','/projeler/999']:
            self.assertEqual(self.client.request(path)[0],404)
        for path in ['/style.css','/main.js','/assets/seysa-logo.svg']:
            self.assertEqual(self.client.request(path)[0],200)

    def test_editorial_categories_articles_and_missing_pages(self):
        for item in ARTICLES:
            status,data,_=self.client.request('/icerik-rehberi/'+item['slug'])
            self.assertEqual(status,200)
            self.assertIn(item['title'],data.decode())
            self.assertEqual(data.count(b'<h1'),1)
        for category in ['rehberler','sektor-haberleri']:
            status,data,_=self.client.request('/icerik-rehberi/'+category)
            self.assertEqual(status,200)
            html=data.decode()
            for item in ARTICLES:
                self.assertEqual(('href="/icerik-rehberi/'+item['slug']+'"') in html,item['category']==category)
        for path in ['/olmayan/bir/sayfa','/icerik-rehberi/yok','/icerik-rehberi/yok/rehberler']:
            status,data,_=self.client.request(path)
            self.assertEqual(status,404)
            self.assertIn('kadrajdan çıkmış',data.decode())
        home=self.client.request('/')[1].decode()
        for symbol in ['✳','↗','☰']:
            self.assertNotIn(symbol,home)
        self.assertIn('/assets/icons.svg#spark',home)
        self.assertEqual(self.client.request('/assets/icons.svg')[0],200)
    def test_crud_publication_uploads_persistence_and_deletion(self):
        csrf=self.setup_admin();other=Client(self.client.port)
        # Authenticated company and image upload; logo remains private until referenced publicly.
        self.assertEqual(self.client.request('/admin/sirketler/yeni',{'csrf':csrf,'name':'Deneme & Şirket','sector':'Medya'},upload=PNG)[0],303)
        with storage.connect() as db: company=dict(db.execute('SELECT * FROM companies').fetchone())
        self.assertEqual(other.request(company['logo'])[0],404)
        self.assertEqual(self.client.request(company['logo'])[0],200)
        ref={'csrf':csrf,'company_id':company['id'],'published':'1','position':'2','is_sample':'1'}
        self.assertEqual(self.client.request('/admin/referanslar/yeni',ref)[0],303)
        self.assertEqual(other.request(company['logo'])[0],200)
        self.assertIn('Deneme &amp; Şirket',other.request('/referanslar')[1].decode())
        self.assertIn('Örnek yerleşim',other.request('/referanslar')[1].decode())
        self.assertEqual(self.client.request('/admin/referanslar/yeni',ref)[0],400)
        project={'csrf':csrf,'title':'Test <script>alert(1)</script>','company_id':company['id'],'summary':'Açıklama','body':'Türkçe içerik','service':'Fotoğraf Çekimi','position':'0'}
        self.assertEqual(self.client.request('/admin/projeler/yeni',project,upload=PNG)[0],303)
        with storage.connect() as db: p=dict(db.execute('SELECT * FROM projects').fetchone())
        self.assertEqual(other.request('/projeler/'+str(p['id']))[0],404)
        self.assertEqual(other.request(p['image'])[0],404)
        project['published']='1'
        self.assertEqual(self.client.request('/admin/projeler/'+str(p['id'])+'/duzenle',project)[0],303)
        status,body,_=other.request('/projeler/'+str(p['id']))
        self.assertEqual(status,200); self.assertIn(b'&lt;script&gt;',body); self.assertNotIn(b'<script>alert',body)
        self.assertEqual(other.request(p['image'])[0],200)
        # Persistence across re-initialization; no reseeding or in-memory data.
        storage.initialize()
        self.assertEqual(len(storage.public_data()[0]),1)
        self.assertEqual(self.client.request('/admin/sirketler/'+str(company['id'])+'/sil')[0],200)
        self.assertEqual(self.client.request('/admin/sirketler/'+str(company['id'])+'/sil',{'csrf':csrf})[0],303)
        with storage.connect() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM reference_items').fetchone()[0],0)
            self.assertIsNone(db.execute('SELECT company_id FROM projects').fetchone()[0])
        self.assertEqual(other.request('/projeler/'+str(p['id']))[0],200)
    def test_gallery_and_site_settings(self):
        csrf=self.setup_admin(); visitor=Client(self.client.port)
        self.assertEqual(self.client.request('/admin/projeler/yeni',{'csrf':csrf,'title':'Galeri testi','brief':'Hedef <script>','process':'Üretim planı','result':'Teslim edilen dosyalar'})[0],303)
        with storage.connect() as db: project_id=db.execute('SELECT id FROM projects').fetchone()[0]
        gallery=f'/admin/projeler/{project_id}/galeri'
        self.assertEqual(self.client.request(gallery,{'csrf':csrf,'position':'10'},upload=[PNG,PNG])[0],303)
        with storage.connect() as db:
            self.assertEqual([r[0] for r in db.execute('SELECT position FROM project_media ORDER BY position')],[10,11])
            before_files=len(list(storage.UPLOADS.iterdir()))
        self.assertEqual(self.client.request(gallery,{'csrf':csrf},upload=[PNG,b'not an image'])[0],400)
        with storage.connect() as db: self.assertEqual(db.execute('SELECT COUNT(*) FROM project_media').fetchone()[0],2)
        self.assertEqual(len(list(storage.UPLOADS.iterdir())),before_files)
        self.assertEqual(visitor.request(gallery,{'csrf':visitor.token()},upload=PNG)[0],401)
        self.assertEqual(self.client.request(gallery,{'csrf':'wrong'},upload=PNG)[0],403)
        self.assertEqual(self.client.request(gallery,{'csrf':csrf,'caption':'Fotoğraf','position':'2'},upload=PNG)[0],303)
        self.assertEqual(self.client.request(gallery,{'csrf':csrf,'video_url':'https://youtu.be/abcdefghijk','caption':'Video','position':'1'})[0],303)
        self.assertEqual(self.client.request(gallery,{'csrf':csrf,'video_url':'https://evil.example/embed/abcdefghijk'})[0],400)
        with storage.connect() as db: photo=dict(db.execute("SELECT * FROM project_media WHERE kind='image'").fetchone())
        self.assertEqual(visitor.request(photo['url'])[0],404)
        self.assertEqual(self.client.request(photo['url'])[0],200)
        self.assertEqual(self.client.request(f'/admin/projeler/{project_id}/duzenle',{'csrf':csrf,'title':'Galeri testi','published':'1'})[0],303)
        self.assertEqual(visitor.request(photo['url'])[0],200)
        status,body,headers=visitor.request(f'/projeler/{project_id}')
        self.assertEqual(status,200)
        self.assertIn(b'id="image-viewer"',body)
        self.assertIn(b'Hedef &lt;script&gt;',body)
        self.assertIn('Üretim planı'.encode(),body)
        self.assertIn(b'Teslim edilen dosyalar',body)
        self.assertIn(b'https://www.youtube-nocookie.com/embed/abcdefghijk',body)
        self.assertLess(body.index(b'<iframe'),body.index(b'class="gallery-open"'))
        self.assertIn('frame-src',headers['Content-Security-Policy'])
        self.assertEqual(self.client.request(gallery+f'/{photo["id"]}/sil',{'csrf':csrf})[0],303)
        self.assertEqual(visitor.request(photo['url'])[0],404)
        settings={'csrf':csrf,'whatsapp':'+90 588 888 88 88','address':'Test adresi','instagram':'https://www.instagram.com/seysamedya/','linkedin':'https://www.linkedin.com/company/seysamedya/'}
        self.assertEqual(self.client.request('/admin/site-bilgileri',settings)[0],303)
        home=visitor.request('/')[1]
        self.assertIn(b'https://wa.me/905888888888',home)
        self.assertIn(b'Test adresi',home)
        settings['instagram']='javascript:alert(1)'
        self.assertEqual(self.client.request('/admin/site-bilgileri',settings)[0],400)
        self.assertEqual(self.client.request(f'/admin/projeler/{project_id}/sil',{'csrf':csrf})[0],303)
        with storage.connect() as db: self.assertEqual(db.execute('SELECT COUNT(*) FROM project_media').fetchone()[0],0)

    def test_auth_csrf_logout_and_upload_safety(self):
        anonymous_token=self.client.token()
        self.assertEqual(self.client.request('/admin/sirketler/yeni',{'csrf':anonymous_token,'name':'Blocked'})[0],401)
        csrf=self.setup_admin()
        self.assertEqual(self.client.request('/admin/sirketler/yeni',{'csrf':'wrong','name':'Blocked'})[0],403)
        self.assertEqual(self.client.request('/admin/sirketler/yeni',{'csrf':csrf,'name':'Blocked'},origin='https://evil.example')[0],403)
        self.assertEqual(self.client.request('/admin/kurulum',{'csrf':csrf,'username':'replacement','password':'long-password-123','password_confirm':'long-password-123'})[0],403)
        for svg in [b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>',b'<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>',b'<svg xmlns="http://www.w3.org/2000/svg"><use href="https://example.com/x"/></svg>']:
            with self.assertRaises(ValueError):server.safe_image(svg)
        with storage.connect() as db:
            password=db.execute('SELECT password FROM users').fetchone()[0]
            self.assertNotIn('Test-only-password',password)
        self.assertEqual(self.client.request('/admin/cikis',{'csrf':csrf})[0],303)
        self.assertIn('Yönetici girişi',self.client.request('/admin')[1].decode())
        token=self.client.token()
        self.assertEqual(self.client.request('/admin/giris',{'csrf':token,'username':'test-admin','password':'Test-only-password-2026'})[0],303)

if __name__=='__main__':unittest.main(verbosity=2)
