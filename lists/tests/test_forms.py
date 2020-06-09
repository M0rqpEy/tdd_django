from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-group-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_save_handles_saveng_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(commit=False)
        new_item.list = list_
        self.assertEqual(new_item.list, list_)