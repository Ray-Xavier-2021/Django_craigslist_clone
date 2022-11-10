from django.shortcuts import render
import requests

from bs4 import BeautifulSoup

# TBD
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from requests.compat import quote_plus

from . import models

BASE_CRAIGSLIST_URL = 'https://newyork.craigslist.org/search/?query={}#search=1~gallery~0~0'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
  template = 'base.html'
  return render(request, template)

def new_search(request):
  search_template = 'my_app/new_search.html'

  # Pull data from search bar
  search = request.POST.get('search')
  models.Search.objects.create(search=search)
  final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))

  # configure browser to run JavaScript
  browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
  browser.get(final_url)
  # print(browser.page_source)
  response = requests.get(final_url)
  data = response.text
  html = browser.page_source

  # Create soup object
  soup = BeautifulSoup(html, features='html.parser')
  # browser.close()

  # FInd all post listings
  post_listings = soup.find_all('li', {'class': 'cl-search-result'})
  # post_title = post_listings[0].find(class_='titlestring').text
  # post_url = post_listings[0].find('a').get('href')
  # post_price = post_listings[0].find(class_='priceinfo')
  # post_image = post_listings[0].find('img', {'class': 'src'})


  final_postings = []

  # loop through each post and grab the data
  for post in post_listings:
    post_title = post.find(class_='titlestring').text
    post_url = post.find('a').get('href')

    print(post_url)

    # Check if there is a price for display if so, display if not N/A
    if post.find(class_='priceinfo'):
      post_price = post.find(class_='priceinfo').text
      print(post_price)
    else:
      post_price = 'N/A'

      # print(post_price)

    # Check if there is an image for display if so, display if not alternate
    if post.find(class_='src'):
      post_image_id = post.find('img').get('src').split('/')[3].split('_3')[0]
      post_image_url = BASE_IMAGE_URL.format(post_image_id)
      print(post_image_url)
    else:
      post_image_url = 'https://craigslist.org/images/peace.jpg'
  
    # Append tuple of data to list
    final_postings.append((post_title, post_url, post_price, post_image_url))

  # Things passed to frontend
  frontend = {
    'search': search,
    'final_postings': final_postings,
  }

  return render(request, search_template, frontend)
