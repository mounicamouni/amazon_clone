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
from Amazonapp.models import Cart, Cart1, Product, Order

class OrderListView(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = User
    context_object_name = 'user_list'
    template_name = "order.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, **self.kwargs)

    def get_context_data(self,**kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        user = context.get('user_list')
        context['userID'] = user.id

        print(type(user))
        order = list(
            Order.objects.values('product__id','product__title','product__description', 'product__image', 'product__price', 'units','date').order_by('date').filter(user_id=user.id))

        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
            'order':order,
        })
        return context
@login_required
def order(request,**kwargs):
    return redirect('order_html', request.user.id)

@login_required
def place_order(request,**kwargs):
    try:
        c=list(Cart1.objects.values().filter(user_id=request.user.id))

        for i in c:
            prod = get_object_or_404(Product, pk=i['product_id'])
            order=Order(product=prod,user=request.user,units=i['units'])
            order.save()
            car = Cart1.objects.get(id=i['id'])
            car.delete()
    except:
        pass
    return redirect('order_html',request.user.id)