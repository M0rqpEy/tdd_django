from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

# Create your tests here.
class HomePageTests(TestCase):
    """тест домашней страницы"""

    def test_root_url_resolves_to_home_page(self):
        """тест: корневой урл преобразуется в представлении
            домашней страницы"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)