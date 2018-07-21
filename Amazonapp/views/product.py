from django.forms import forms
from django.views import View

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import *
from django.views.generic.detail import *
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *

from Amazonapp.models import *


class SubcategoryProductList(DetailView):
    login_url = '/login/'
    model = Subcategory
    context_object_name = 'subcategory_list'
    template_name = "product.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Subcategory, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubcategoryProductList, self).get_context_data(**kwargs)
        subcategory = context.get('subcategory_list')
        context['subcategoryID'] = subcategory.id
        print(type(subcategory))
        product = list(
            Product.objects.values('subcategory__id', 'id', 'title','image','price','rating','description').filter(
                subcategory_id=subcategory.id))

        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
            'product':product ,
        })
        return context


from django import forms
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude= ['id','subcategory']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control' ,'placeholder':'enter title'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'units': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter units'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter rating'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter description'}),
        }

from django.views.generic.edit import CreateView
class CreateSubcategoryProductView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'

    model = Product
    form_class = ProductForm
    template_name = 'productForm.html'
    def get_context_data(self, **kwargs):
        context = super(CreateSubcategoryProductView, self).get_context_data(**kwargs)
        context.update({'subcategory_form': context.get('form')})
        return context
    def post(self, request, *args, **kwargs):
        subcategory = get_object_or_404(Subcategory, pk=kwargs['pk'])
        product_form = ProductForm(request.POST,request.FILES)
        form_class = ProductForm
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.subcategory = subcategory
            product.save()
        return redirect('product_html',self.kwargs.get('category_id'), self.kwargs.get('pk'))

class UpdateSubcategoryProductView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model = Product
    form_class = ProductForm
    template_name = 'productForm.html'
    def get_context_data(self, **kwargs):
        context = super(UpdateSubcategoryProductView, self).get_context_data(**kwargs)
        product_form = context.get('product')
        context.update({'product_form': context.get('form')})
        return context

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        form = ProductForm(request.POST,request.FILES, instance=product)
        form.save()
        return redirect('product_html',self.kwargs.get('category_id'), self.kwargs.get('subcategory_id'))


class DeleteSubcategoryProductView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model=Product
    success_url = reverse_lazy('category_html')
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        self.delete(request, args, kwargs)
        return redirect('product_html',self.kwargs.get('category_id'), self.kwargs.get('subcategory_id'))

