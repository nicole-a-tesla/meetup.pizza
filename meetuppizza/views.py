from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from meetuppizza.forms import RegistrationForm
import pdb

def index(request):
  return render(request, 'index.html')

def sign_up(request):
  if request.method == 'GET':
    args = {}
    args['form'] = RegistrationForm().as_ul
    return render(request, 'sign_up.html', args)

  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()

      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)

        return redirect('/welcome')
    else:
      return render(request, 'sign_up.html', {'form': form})

def welcome(request):
  return render(request, 'welcome.html')
