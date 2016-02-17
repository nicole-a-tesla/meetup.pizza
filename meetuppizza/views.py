from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def index(request):
  # template_name = "template/index.html"
  # template = loader.get_template('templates/index.html')
  return render(request, 'index.html')