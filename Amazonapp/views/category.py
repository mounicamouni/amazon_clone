from django.forms import forms
from django.http import HttpResponseRedirect
from django.views import View

from django.shortcuts import render,get_object_or_404
from django.views.generic.list import *
from django.views.generic.detail import *
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *

from Amazonapp.models import *

class CategoryListView(ListView):
    login_url = '/login/'
    model = Category
    context_object_name='category'
    template_name = "category.html"

    def get_context_data(self,**kwargs):
        context=super(CategoryListView,self).get_context_data(**kwargs)
        # import ipdb
        # ipdb.set_trace()
        # pass
        return context



from django import forms
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude= ['id']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control' ,'placeholder':'enter title'  }),
            'active': forms.CheckboxInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter active out of the Is Dropped'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter description'}),
        }

from django.views.generic.edit import CreateView
class CreateCategoryView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model=Category
    form_class = CategoryForm
    success_url=reverse_lazy('category_html')
    template_name = 'categoryForm.html'



# def upload_file(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = CategoryForm(image=request.FILES['file'])
#             instance.save()
#             return HttpResponseRedirect('category_html')
#     else:
#         form = CategoryForm()
#     return render(request, 'category.html', {'form': form})

class UpdateCategoryView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model = Category
    form_class = CategoryForm
    template_name = 'categoryForm.html'
    success_url = reverse_lazy('category_html')


class DeleteCategoryView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/login/'
    permission_required = 'category_html'
    permission_denied_message = 'Sorry ! u cant add..login before u add'
    model=Category
    success_url = reverse_lazy('category_html')
    def get(self,request,*args,**kwargs):
        return self.post(request,args,kwargs)