from unittest import skip
from django.test import TestCase

from lists.forms import ItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        # list1 = List.objects.create()
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-group-lg"', form.as_p())
        # print(form.instance.text)
        self.assertEqual(form.instance.list_id, None)

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR]
        )

    def test_form_validation_for_duplicate_items(self):
        list1 = List.objects.create()
        Item.objects.create(list=list1, text="ata")
        form = ItemForm(for_list=list1, data={'text': 'ata'})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [DUPLICATE_ITEM_ERROR]
        )

    def test_form_save_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(for_list=list_, data={'text': 'do me'})
        new_item = form.save()
        self.assertEqual(new_item.list, list_)

