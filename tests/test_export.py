import unittest
from export_static import rewrite_html


class ExportTests(unittest.TestCase):
    def test_gallery_and_navigation_resolve_under_pages_subdirectory(self):
        html = '<a href="/projeler/2">Proje</a><button data-full-image="/uploads/test.jpg"><img src="/uploads/test.jpg"></button><a href="https://example.com/">Dış bağlantı</a>'
        result = rewrite_html(html, 2)
        self.assertIn('href="../../projeler/2/index.html"', result)
        self.assertIn('data-full-image="../../uploads/test.jpg"', result)
        self.assertIn('src="../../uploads/test.jpg"', result)
        self.assertIn('href="https://example.com/"', result)
