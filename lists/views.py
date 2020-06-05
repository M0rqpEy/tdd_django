from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

# Create your views here.
def home_page(request):
    """домашня страница"""
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text')
        Item.objects.create(text=new_item_text)
        return redirect('/lists/new-to-do-items/')
    else:
        new_item_text = ""
    return render(request, 'lists/home.html')

def view_list(request):
    """представление списка"""
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})