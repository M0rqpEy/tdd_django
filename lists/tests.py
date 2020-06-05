from django.urls import resolve
from django.http import HttpRequest
from django.test import TestCase

from lists.views import home_page
from lists.models import Item


# Create your tests here.
class HomePageTests(TestCase):
    """тест домашней страницы"""

    def test_root_url_resolves_to_home_page(self):
        """тест: корневой урл преобразуется в представлении
            домашней страницы"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_uses_home_template(self):
        """тест: дом. страница возвращает правильный html"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        """тест перенаправление после post-запроса"""
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response['location'],
            '/lists/new-to-do-items/'
        )

    def test_only_saves_items_when_necessary(self):
        """тест сохраняет елементы только когда нужно"""
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListsViewsTest(TestCase):
    """тест представления списка"""

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""
        response = self.client.get('/lists/new-to-do-items/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items(self):
        """тест: отображаются все элементы списка"""
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get(
                '/lists/new-to-do-items/'
        )

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


class ItemModelTests(TestCase):
    """тест модели елемента списка"""

    def test_saving_and_retrieving_items(self):
        """тест: сохранения и получения елем. списка"""
        first_item = Item()
        first_item.text = 'The first item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first item')
        self.assertEqual(second_saved_item.text, 'Item the second')