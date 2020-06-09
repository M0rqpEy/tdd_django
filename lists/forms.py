from django import forms
from django.utils.safestring import mark_safe

from .models import Item

EMPTY_ITEM_ERROR = mark_safe("You can't have an empty list item")
DUPLICATE_ITEM_ERROR = mark_safe("You've already got this in your list")


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': "form-control input-group-lg",
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def clean_text(self):
        # print(dir(self.instance))
        # print(self.instance._get_unique_checks())
        return self.cleaned_data['text']