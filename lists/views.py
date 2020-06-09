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
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            # new_item = form.save(commit=False)
            # new_item.list = list_
            # new_item.save()
            form.save()
            return redirect(list_)
    return render(request, 'lists/list.html', {"list": list_, 'form': form})


def new_list(request):
    """новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        new_item = form.save(commit=False)
        new_item.list = list_
        new_item.save()
        return redirect(list_)
    else:
        return render(request, 'lists/home.html', {"form": form})

