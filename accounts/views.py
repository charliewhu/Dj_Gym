from accounts.forms import RegistrationForm
from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib import messages



def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}')
            return redirect('accounts:login')

    context={
        'form':form,
        'title':'Register',
        'year':datetime.now().year,
        }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')