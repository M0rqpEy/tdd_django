from django import forms
from django.utils.safestring import mark_safe

from .models import Item

#
# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': "form-control input-group-lg",
#         })
#     )
EMPTY_ITEM_ERROR = mark_safe("You can't have an empty list item")

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