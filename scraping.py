# Imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": [{'img_url': 'https://marshemispheres.com/images/full.jpg',
            'title': 'Cerberus Hemisphere Enhanced'},
            {'img_url': 'https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg',
            'title': 'Schiaparelli Hemisphere Enhanced'},
            {'img_url': 'https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg',
            'title': 'Syrtis Major Hemisphere Enhanced'},
            {'img_url': 'https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg',
            'title': 'Valles Marineris Hemisphere Enhanced'}]
    } 

    # Stop webdriver and return data
    browser.quit()
    return data 

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object and then quit browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
   
    except AttributeError:
        return None, None    

    return news_title, news_p


# ### JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None 

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts

def mars_facts():

    # Add try/except for error handling
    try:
        # Create a new dataframe from the HTML table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns to the new DataFrame for additional clarity.
    df.columns=['Description', 'Mars', 'Earth']

    # By using the .set_index() function, we're turning the Description column into the DataFrame's index.
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres():

    # Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
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
    browser.visit(url+images[7]['href'])

    html_hemi = browser.html
    hemi_soup = soup(html_hemi, 'html.parser')
    images = hemi_soup.find_all('a')
    img_url = url+images[3]['href']
    title = hemi_soup.find_all('h2', class_="title")[0].text
    hemisphere_image_urls.append({'img_url': img_url, 'title': title})
    browser.back()

    hemisphere_image_urls

    browser.quit()

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())