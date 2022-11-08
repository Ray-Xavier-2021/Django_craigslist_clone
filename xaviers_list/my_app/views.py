from django.shortcuts import render
import requests

from bs4 import BeautifulSoup

# Create your views here.
def home(request):
  template = 'base.html'
  return render(request, template)

def new_search(request):
  search_template = 'my_app/new_search.html'

  # Pull data from search bar
  search = request.POST.get('search')

  # print(search)

  # Things passed to frontend
  frontend = {
    'search': search,
  }


  return render(request, search_template, frontend)
