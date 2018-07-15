from django.forms import forms
from django.views import View

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import *
from django.views.generic.detail import *
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *

from Amazonapp.models import *

# class SubcategoryList(DetailView):
#     # login_url = '/login/'
#
#     # model = Subcategory
#     # context_object_name = 'subcategory_list'
#     # template_name = "category.html"
#     #
#     # def get_context_data(self, **kwargs):
#     #     context = super(SubcategoryList, self).get_context_data(**kwargs)
#     #     x=context['subcategory_list']
#     #     z=list(
#     #          Subcategory.objects.values('id','title','image', 'description').filter(
#     #              id=x.id))
#     #     print(z)
#     #     import ipdb
#     #     ipdb.set_trace()
#     #     pass
#     #     context.update({
#     #             'user_permissions': self.request.user.get_all_permissions(),
#     #             'subcategory':z ,
#     #         })
#     #
#     #     return context
#
#     login_url = '/login/'
#
#     model = Category
#     context_object_name = 'category_list'
#     template_name = "subcategory.html"
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Category, **self.kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super(SubcategoryList, self).get_context_data(**kwargs)
#         category = context.get('category_list')
#
#         context['categoryID'] = category.id
#         # import ipdb
#         # ipdb.set_trace()
#         # pass
#         print(type(category))
#         subcategory = list(
#             Category.objects.values('id', 'subcategory__id', 'subcategory__title','subcategory__image', 'subcategory__description').filter(
#                 id=category.id))
#
#
#         context.update({
#             'user_permissions': self.request.user.get_all_permissions(),
#             'subcategory':subcategory ,
#         })
#         return context


class SubcategoryList(DetailView):
    # login_url = '/login/'

    # model = Subcategory
    # context_object_name = 'subcategory_list'
    # template_name = "category.html"
    #
    # def get_context_data(self, **kwargs):
    #     context = super(SubcategoryList, self).get_context_data(**kwargs)
    #     x=context['subcategory_list']
    #     z=list(
    #          Subcategory.objects.values('id','title','image', 'description').filter(
    #              id=x.id))
    #     print(z)
    #     import ipdb
    #     ipdb.set_trace()
    #     pass
    #     context.update({
    #             'user_permissions': self.request.user.get_all_permissions(),
    #             'subcategory':z ,
    #         })
    #
    #     return context

    login_url = '/login/'

    model = Category
    context_object_name = 'category_list'
    template_name = "subcategory.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Category, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubcategoryList, self).get_context_data(**kwargs)
        category = context.get('category_list')

        context['categoryID'] = category.id
        # import ipdb
        # ipdb.set_trace()
        # pass
        print(type(category))
        subcategory = list(
            Subcategory.objects.values('category__id', 'id', 'title','image', 'description').filter(
                category_id=category.id))


        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
            'subcategory':subcategory ,
        })
        return context

from django import forms
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        exclude= ['id','category']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control' ,'placeholder':'enter title'  }),
            'active': forms.CheckboxInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter active out of the Is Dropped'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter description'}),

        }

from django.views.generic.edit import CreateView
class CreateSubcategoryView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'subcategoryForm.html'
    def get_context_data(self, **kwargs):
        context = super(CreateSubcategoryView, self).get_context_data(**kwargs)
        context.update({'subcategory_form': context.get('form')})
        return context
    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=kwargs['pk'])
        subcategory_form = SubcategoryForm(request.POST,request.FILES)
        form_class = SubcategoryForm
        # import ipdb
        # ipdb.set_trace()
        # pass
        if subcategory_form.is_valid():
            subcategory = subcategory_form.save(commit=False)
            subcategory.category = category
            subcategory.save()
        return redirect('subcategory_html', self.kwargs.get('pk'))

class UpdateSubcategoryView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'subcategoryForm.html'
    def get_context_data(self, **kwargs):
        context = super(UpdateSubcategoryView, self).get_context_data(**kwargs)
        subcategory_form = context.get('subcategory')
        context.update({'subcategory_form': context.get('form')})
        return context

    def post(self, request, *args, **kwargs):
        subcategory = Subcategory.objects.get(pk=kwargs.get('pk'))
        form = SubcategoryForm(request.POST,request.FILES, instance=subcategory)
        form.save()
        return redirect('subcategory_html', self.kwargs.get('category_id'))


class DeleteSubcategoryView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    # login_url = '/login/'
    # permission_required = 'onlineapp.college_list'
    # permission_denied_message = 'Sorry ! u cant add..login before u add'
    model=Subcategory
    success_url = reverse_lazy('category_html')
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        self.delete(request, args, kwargs)
        return redirect("subcategory_html", self.kwargs.get('category_id'))