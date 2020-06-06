from django.urls import resolve
from django.http import HttpRequest
from django.test import TestCase

from lists.views import home_page, view_list
from lists.models import Item, List


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


class ListsViewsTest(TestCase):
    """тест представления списка"""

    def test_lists_url_resolves(self):
        """тест: корневой урл преобразуется в представлении
            домашней страницы"""
        list_ = List.objects.create()
        found = resolve(f'/lists/{list_.id}/')
        self.assertEqual(found.func, view_list)

    def test_uses_list_template(self):
        """тест: используется шаблон списка"""
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_display_all_items_for_that_list(self):
        """тест: отображаются все элементы списка"""
        list_ = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)

        response = self.client.get(
                f'/lists/{list_.id}/'
        )

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def test_pass_correct_list_to_template(self):
        """тест: передается правильный шаблон спискa """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class ListAndItemModelTests(TestCase):
    """тест модели елемента списка"""

    def test_saving_and_retrieving_items(self):
        """тест: сохранения и получения елем. списка"""
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""
        self.client.post('/lists/new', data={'item_text': 'new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запроса"""
        response = self.client.post(
                            '/lists/new',
                            data={'item_text': 'new list item'}
        )
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')


class NewItemTest(TestCase):
    """тест нового элемента списка"""

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можно сохранить post-запрос в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(f'/lists/{correct_list.id}/add_item',
                         data={'item_text': 'item1'}
                         )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'item1')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """тест: переадресуется в представление списка"""
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
                        f'/lists/{correct_list.id}/add_item',
                        data={'item_text': 'item1'}
                    )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
