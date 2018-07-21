from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.forms import forms
from django.http import HttpResponseRedirect
from django.views import View

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import *
from django.views.generic.detail import *
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *
from Amazonapp.models import Cart, Cart1, Product


# class CartListView(DetailView):
#     model = User
#     context_object_name = 'user_list'
#     template_name = "cart.html"
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(User, **self.kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(CartListView, self).get_context_data(**kwargs)
#         user = context.get('user_list')
#         import ipdb
#         ipdb.set_trace()
#         pass
#         context['userID'] = user.id
#         print(type(user))
#         cart = list(
#             Cart.objects.get(user_id=user.id).products.all().values())
#
#         context.update({
#             'user_permissions': self.request.user.get_all_permissions(),
#             'cart':cart,
#         })
#         return context
#
#
# class CartListView(DetailView):
#     model = User
#     context_object_name = 'user_list'
#     template_name = "cart1.html"
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(User, **self.kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(CartListView, self).get_context_data(**kwargs)
#         user = context.get('user_list')
#         import ipdb
#         ipdb.set_trace()
#         pass
#         context['userID'] = user.id
#         print(type(user))
#         cart = list(
#             Cart1.objects.values('product__title', 'product__image', 'product__price').annotate(
#                 count=Count("product")).filter(user_id=user.id))
#         total=0
#         for i in cart:
#             total+=i['product__price']*i['count']
#         context.update({
#             'user_permissions': self.request.user.get_all_permissions(),
#             'cart':cart,
#             'total':total,
#         })
#         return context



class CartListView(LoginRequiredMixin,DetailView):
    login_url = "/login/"
    model = User
    context_object_name = 'user_list'
    template_name = "cart1.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, **self.kwargs)

    def get_context_data(self,**kwargs):
        context = super(CartListView, self).get_context_data(**kwargs)
        user = context.get('user_list')
        # import ipdb
        # ipdb.set_trace()
        # pass
        context['userID'] = user.id
        print(type(user))
        cart = list(
            Cart1.objects.values('product__id','product__title', 'product__image', 'product__price', 'units').filter(user_id=user.id))
        total=0
        for i in cart:
            total+=i['product__price']*i['units']
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
            'cart':cart,
            'total':total,
        })
        return context
@login_required
def cart(request,**kwargs):
    return redirect('cart_html', request.user.id)

@login_required
def cart_create(request,**kwargs):
    login_url="/login/"
    prod = get_object_or_404(Product, pk=kwargs['pk'])

    try:
        c=list(Cart1.objects.values().get(product_id=prod.id,user_id=request.user.id))
        c = Cart1.objects.get(product_id=prod.id, user_id=request.user.id)
        c.units = c.units + 1
        c.save()
    except:
        c=Cart1(units=1,product=prod,user=request.user)
        c.save()
    return redirect('cart_html',request.user.id)
@login_required
def increment_cart(request,**kwargs):
    login_url = "/login/"
    prod = get_object_or_404(Product, pk=kwargs['pk'])
    c = Cart1.objects.get(product_id=prod.id, user_id=request.user.id)
    c.units = c.units + 1
    c.save()
    return redirect('cart_html', request.user.id)

@login_required
def decrement_cart(request,**kwargs):
    login_url = "/login/"
    prod = get_object_or_404(Product, pk=kwargs['pk'])
    c = Cart1.objects.get(product_id=prod.id, user_id=request.user.id)
    if c.units==1:
        pass
    else:
        c.units = c.units - 1
        c.save()
    return redirect('cart_html', request.user.id)

@login_required
def delete_cart(request,**kwargs):
    login_url = "/login/"
    prod=get_object_or_404(Product,pk=kwargs['pk'])
    c = Cart1.objects.get(product_id=prod.id, user_id=request.user.id)
    c.delete()
    return redirect('cart_html', request.user.id)