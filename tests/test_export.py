import unittest
from urllib.parse import urljoin
from export_static import rewrite_html


class ExportTests(unittest.TestCase):
    def test_error_page_links_work_at_unknown_nested_urls(self):
        html = '<a href="/">Home</a><link href="/assets/creative.css"><use href="/assets/icons.svg#spark"/>'
        result = rewrite_html(html, 0, root_prefix='/seysam/')
        self.assertIn('href="/seysam/index.html"', result)
        self.assertIn('href="/seysam/assets/creative.css"', result)
        self.assertIn('href="/seysam/assets/icons.svg#spark"', result)
        self.assertEqual(urljoin('https://example.com/seysam/missing/deep/path', '/seysam/index.html'), 'https://example.com/seysam/index.html')

    def test_gallery_and_navigation_resolve_under_pages_subdirectory(self):
        html = '<a href="/projeler/2">Proje</a><button data-full-image="/uploads/test.jpg"><img src="/uploads/test.jpg"></button><a href="https://example.com/">Dış bağlantı</a>'
        result = rewrite_html(html, 2)
        self.assertIn('href="../../projeler/2/index.html"', result)
        self.assertIn('data-full-image="../../uploads/test.jpg"', result)
        self.assertIn('src="../../uploads/test.jpg"', result)
        self.assertIn('href="https://example.com/"', result)
