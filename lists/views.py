from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

# Create your views here.
def home_page(request):
    """домашня страница"""
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text')
        Item.objects.create(text=new_item_text)
        return redirect('/')
    else:
        new_item_text = ""
    return render(
               request,
               'lists/home.html',
               {'items': Item.objects.all()}
    )
