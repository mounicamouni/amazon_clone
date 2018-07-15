from Amazonapp.forms import *
from django.shortcuts import  *
from django.contrib.auth import authenticate,login,logout
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.signals import post_save

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from Amazonapp.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.mobileno = form.cleaned_data.get('mobileno')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('category_html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class LoginController(View):
    def get(self,request):
        form=LoginForm()
        return render(
            request,
            template_name='Login.html',
            context={'form': form, 'title': 'Login'}
        )

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data
            user=authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request,user)
                return redirect('category_html')
            else:
                messages.error(request,"invalid credentials")
        else:
            messages.error(request,"invalid credentials")
def logout_user(request):
    logout(request)
    return redirect('home')
