from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import forms
from django.http import HttpResponseRedirect
from django.views import View

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import *
from django.views.generic.detail import *
from django.views.generic import ListView, DetailView ,CreateView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import *

from Amazonapp.models import Address


class AddressListView(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = User
    context_object_name = 'user_list'
    template_name = "address.html"

    def get_object(self, queryset=None):
        return get_object_or_404(User, **self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddressListView, self).get_context_data(**kwargs)
        user = context.get('user_list')
        context['userID'] = user.id

        print(type(user))
        address = list(
            Address.objects.values('id', 'country', 'fullname','mobileno','pincode','city','street',
             'landmark','state' ,'address_type').filter(user_id=user.id))

        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
            'address': address,
        })
        return context
@login_required
def address(request,**kwargs):
    login_url='/login/'
    return redirect('address_html', request.user.id)

from django import forms
class AddressForm(forms.ModelForm):
    mobileno = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mobileno'}),
                                help_text=(
                                    "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")),

    class Meta:
        model = Address
        exclude= ['id','user']

        # fields = ('country', 'fullname', 'pincode','street','mobileno','landmark','city','state','address_type' , )
        widgets={
            'country':forms.TextInput(attrs={'class':'form-control' ,'placeholder':'enter title'  }),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'mobileno':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
            'address_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter title'}),
        }


from django.views.generic.edit import CreateView
class CreateAddressView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Address
    form_class = AddressForm
    template_name = 'addressForm.html'

    def get_context_data(self, **kwargs):
        context = super(CreateAddressView, self).get_context_data(**kwargs)
        context.update({'address_form': context.get('form')})
        return context
    def post(self, request, *args, **kwargs):
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
        return redirect('address_html',request.user.id)

class UpdateAddressView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Address
    form_class = AddressForm
    template_name = 'addressForm.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateAddressView, self).get_context_data(**kwargs)
        address_form = context.get('address')
        context.update({'address_form': context.get('form')})
        return context

    def post(self, request, *args, **kwargs):
        address = Address.objects.get(pk=kwargs.get('pk'))
        form = AddressForm(request.POST, request.FILES, instance=address)
        form.save()
        return redirect('address_html',request.user.id)


class DeleteAddressView(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model=Address
    success_url = reverse_lazy('address_add_html')
    def get(self, request, *args, **kwargs):
        return self.post(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        self.delete(request, args, kwargs)
        return redirect("address_html", request.user.id)