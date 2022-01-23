#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ### Visit the NASA Mars News Site

url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# Create a new dataframe from the HTML table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
# Assign columns to the new DataFrame for additional clarity.
df.columns=['Description', 'Mars', 'Earth']
# By using the .set_index() function, we're turning the Description column into the DataFrame's index.
df.set_index('Description', inplace=True)
df

# Use Pandas to convert the DataFrame back into HTML-ready code using the .to_html() function
df.to_html()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a', class_='itemLink product-item')
browser.visit(url+images[0]['href'])

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a')
img_url = url+images[3]['href']
title = hemi_soup.find_all('h2', class_="title")[0].text
hemisphere_image_urls.append({'img_url': img_url, 'title': title})
browser.back()

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a', class_='itemLink product-item')
browser.visit(url+images[2]['href'])

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a')
img_url = url+images[3]['href']
title = hemi_soup.find_all('h2', class_="title")[0].text
hemisphere_image_urls.append({'img_url': img_url, 'title': title})
browser.back()

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a', class_='itemLink product-item')
browser.visit(url+images[4]['href'])

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a')
img_url = url+images[3]['href']
title = hemi_soup.find_all('h2', class_="title")[0].text
hemisphere_image_urls.append({'img_url': img_url, 'title': title})
browser.back()

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a', class_='itemLink product-item')
browser.visit(url+images[7]['href'])

html_hemi = browser.html
hemi_soup = soup(html_hemi, 'html.parser')
images = hemi_soup.find_all('a')
img_url = url+images[3]['href']
title = hemi_soup.find_all('h2', class_="title")[0].text
hemisphere_image_urls.append({'img_url': img_url, 'title': title})
browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()