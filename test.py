
# loop through each post and grab the data
  for post in post_listings:
    post_title = post.find(class_='titlestring').text
    post_url = post.find('a').get('href')

    # Check if there is a price for display if so, display if not N/A
    if post.find(class_='priceinfo'):
      post_price = post.find(class_='priceinfo').text
      print(post_price)
    else:
      post_price = 'N/A'

      print(post_price)

    # Check if there is an image for display if so, display if not alternate
    if post.find(class_='src'):
      post_image_id = post.find('img').get('src').split('/')[3].split('_3')[0]
      # print(post_image_id)
      # print(type(post_image_id))
      # print(type(post.find('img').get('src')))
      post_image_url = BASE_IMAGE_URL.format(post_image_id)
      # print(type(post_image_url))
      # print(post_image_url)
    elif post.find(class_='src') == None:
      print('No src Attribute')
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
