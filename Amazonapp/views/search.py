import operator
from functools import reduce

from django.db.models import Q

from Amazonapp.views import CategoryListView, ListView, redirect
from Amazonapp.models import *
from django.shortcuts import render

# class SearchProductView(ListView):
#     template_name = "product.html"
#
#     def get_queryset(self, *args, **kwargs):
#         import ipdb
#         ipdb.set_trace()
#         request = self.request
#         method_dict = request.GET
#         query = method_dict.get('q', None) # method_dict['q']
#         print(query)
#         if query is not None:
#             x=Product.objects.filter(title__icontains=query)
#             return x
#         return Product.objects.featured()

def SearchCategoryView(request,string):
    if string is not None:
        x = list(Category.objects.filter(title__icontains=string))
        #
        # import ipdb
        # ipdb.set_trace()

        return render(request, 'category.html', {'category': x})
    pass
def SearchSubcategoryView(request,string):
    if string is not None:
        # x = list(Subcategory.objects.filter(title__icontains=string))
        subcategory = list(
            Subcategory.objects.values('category__id', 'id', 'title', 'image', 'description').filter(
                title__icontains=string))

        return render(request, 'subcategory.html', {'subcategory': subcategory})
    pass
def SearchProductView(request,string):
    string = " ".join(string.split('-'))
    import ipdb
    ipdb.set_trace()
    if string is not None:
        # x = list(Subcategory.objects.filter(title__icontains=string))

        product = list(
            Product.objects.values('subcategory__category__id','subcategory__id', 'id', 'title', 'image', 'price',
                                       'description').filter(title__icontains=string))



        return render(request, 'product_search.html', {'product': product})
    return render(request, 'product_search.html')

def search_all(request,**kwargs):
    import ipdb
    ipdb.set_trace()
    method_dict = dict(request.GET)
    str='-'.join(list(method_dict['q'][0].split()))
    if(method_dict['q'][0]==''):
        return render(request,'no_search.html')
    if(method_dict['r'])==['subcategory']:
        return redirect('list_subcategory',str)
    elif (method_dict['r']) == ['category']:
        return redirect('list_category',str)
    elif (method_dict['r']) == ['product']:
        return redirect('list_product',str)