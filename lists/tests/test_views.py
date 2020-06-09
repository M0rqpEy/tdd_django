from unittest import skip
from django.urls import resolve, reverse
from django.test import TestCase
from django.utils.safestring import mark_safe

from lists.views import home_page, view_list
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


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

    def test_home_page_uses_item_form(self):
        response = self.client.get(reverse('home'))
        self.assertIsInstance(response.context['form'], ItemForm)


class ViewListTest(TestCase):
    """тест представления списка"""

    def post_invalid_input(self):
        list_ =  List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            data={'text': ''}
        )

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
        another_list = List.objects.create()
        Item.objects.create(text='item1', list=list_)
        Item.objects.create(text='item2', list=list_)
        Item.objects.create(text='item3', list=another_list)
        Item.objects.create(text='item4', list=another_list)

        response = self.client.get(
                f'/lists/{list_.id}/'
        )

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'item3')
        self.assertNotContains(response, 'item4')

    def test_pass_correct_list_to_template(self):
        """тест: передается правильный шаблон спискa """
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        """тест: можно сохранить post-запрос в существующий список"""
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post(f'/lists/{correct_list.id}/',
                         data={'text': 'item1'}
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
            f'/lists/{correct_list.id}/',
            data={'text': 'item1'}
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_display_item_form(self):
        list_ =  List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    @skip
    def test_duplicate_item_validation_error_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 =  Item.objects.create(list=list1, text="ata")
        response = self.client.post(
            f'/lists/{list1.id}/',
            data={'text': 'ata'}
        )

        expected_error = mark_safe("You've already got this in your list")
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'lists/list.html')
        self.assertEqual(Item.objects.count(), 1)

class NewListTest(TestCase):
    """тест нового списка"""

    def test_can_save_a_POST_request(self):
        """тест: можно сохранить post-запрос"""
        self.client.post('/lists/new', data={'text': 'new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new list item')

    def test_redirects_after_POST(self):
        """тест: переадресует после post-запроса"""
        response = self.client.post(
                            '/lists/new',
                            data={'text': 'new list item'}
        )
        list_ = List.objects.first()
        self.assertRedirects(response, f'/lists/{list_.id}/')

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    # def test_validation_error_are_sent_back_to_home_page_template(self):
    #     response = self.client.post('/lists/new', data={'item_text': ''})
    #
    #
    #
    def test_for_invalid_input_renders_home_page(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lists/home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertContains(response, EMPTY_ITEM_ERROR)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertIsInstance(response.context['form'], ItemForm)
