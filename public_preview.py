"""Read-only public preview proxy; never forwards admin routes or cookies."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, unquote
from urllib.request import urlopen, Request
from urllib.error import HTTPError


class Preview(BaseHTTPRequestHandler):
    def do_GET(self):
        target = urlsplit(self.path)
        path = unquote(target.path)
        allowed = path in ('/', '/style.css', '/main.js', '/projeler', '/referanslar', '/paketler', '/hakkimizda', '/iletisim', '/hizmetler') or path.startswith(('/hizmetler/', '/projeler/', '/assets/', '/uploads/'))
        if not allowed or '..' in path.split('/') or '\x00' in path:
            self.send_error(404)
            return
        try:
            result = urlopen(Request('http://127.0.0.1:4173' + target.path + ('?' + target.query if target.query else '')), timeout=15)
        except HTTPError as error:
            result = error
        except OSError:
            self.send_error(502)
            return
        with result:
            data = result.read()
            self.send_response(result.status)
            for key in ('Content-Type', 'Content-Security-Policy', 'X-Content-Type-Options'):
                if result.headers.get(key): self.send_header(key, result.headers[key])
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Robots-Tag', 'noindex, nofollow')
            self.end_headers()
            self.wfile.write(data)


if __name__ == '__main__':
    print('Public preview proxy: http://127.0.0.1:4180', flush=True)
    ThreadingHTTPServer(('127.0.0.1', 4180), Preview).serve_forever()
