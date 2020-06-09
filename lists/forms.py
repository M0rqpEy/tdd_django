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

    def __init__(self, for_list=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def clean_text(self):
        cd = self.cleaned_data
        try:
            list_ = self.instance.list
        except:
            list_ = None
        if list_ is not None and \
            cd['text'] in list_.item_set.values_list('text', flat=True):
            raise forms.ValidationError(DUPLICATE_ITEM_ERROR)
        return self.cleaned_data['text']