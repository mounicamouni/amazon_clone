import operator
from functools import reduce

from django.db.models import Q

from Amazonapp.views import CategoryListView, ListView, redirect
from Amazonapp.models import *
from django.shortcuts import render


def SearchCategoryView(request,string):
    string = " ".join(string.split('-'))
    if string is not None:
        x = list(Category.objects.filter(title__icontains=string))
        return render(request, 'category.html', {'category': x})
    pass
def SearchSubcategoryView(request,string):
    string = " ".join(string.split('-'))
    if string is not None:
        subcategory = list(
            Subcategory.objects.values('category__id', 'id', 'title', 'image', 'description').filter(
                title__icontains=string))

        return render(request, 'subcategory.html', {'subcategory': subcategory})
    pass
def SearchProductView(request,string):
    string = " ".join(string.split('-'))
    if string is not None:
        product = list(
            Product.objects.values('subcategory__category__id','subcategory__id', 'id', 'title', 'image', 'price',
                                       'description').filter(title__icontains=string))

        return render(request, 'product_search.html', {'product': product})
    return render(request, 'product_search.html')

def search_all(request,**kwargs):
    method_dict = dict(request.GET)
    str = '-'.join(list(method_dict['q'][0].split()))
    if (method_dict['q'][0] == ''):
        return render(request, 'no_search.html')
    if (method_dict['r']) == ['subcategory']:
        return redirect('list_subcategory', str)
    elif (method_dict['r']) == ['category']:
        return redirect('list_category', str)
    elif (method_dict['r']) == ['product']:
        return redirect('list_product', str)