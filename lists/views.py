from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    """домашня страница"""
    return render(request, 'lists/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    """представление списка"""
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == "POST":
        try:
            item = Item(text=request.POST.get('item_text'), list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError as e:
            error = mark_safe("You can't have an empty list item")

    return render(request, 'lists/list.html', {"error": error, "list": list_})


def new_list(request):
    """новый список"""
    list_ = List.objects.create()
    item = Item(text=request.POST.get('item_text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError as e:
        list_.delete()
        error = mark_safe("You can't have an empty list item")
        return render(
            request,
            'lists/home.html',
            {"error": error}
        )
    return redirect(f'/lists/{list_.id}/')
