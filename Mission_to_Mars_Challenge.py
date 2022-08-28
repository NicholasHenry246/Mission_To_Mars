#!/usr/bin/env python
# coding: utf-8

# In[524]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver



# In[525]:

def scrape_all():
# Set the executable path and initialize Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    data = {
      "news_title": news_title,
      #"news_paragraph": mars_news,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      #"last_modified": dt.datetime.now()
      "hemispheres": images(browser)
    }
      
    return data
# ### Visit the NASA Mars News Site

# In[526]:

def news_title(browser):
# Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

# Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[527]:


# Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')

# In[528]:

        slide_elem.find('div', class_='content_title')

# In[529]:

# Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
    # news_title


# In[530]:


# Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    # news_p

    except AttributeError:
        return None, None

    return news_title, news_p
# ### JPL Space Images Featured Image

# In[531]:

def featured_image(browser):
# Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


# In[532]:


# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


# In[533]:


# Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup


# In[534]:


# find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        # img_url_rel


# In[535]:

    except AttributeError:
        return None
# Use the base url to create an absolute url

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    # img_url

    return img_url
# ### Mars Facts

# In[536]:
def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
        #df.head()

    except BaseException:
        return None
# In[537]:


    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()


# In[538]:

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[539]:

def images(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    # In[540]:


    # https://python.hotexamples.com/examples/splinter/Browser/find_by_css
    # /python-browser-find_by_css-method-examples.html

    # 2. Create a list to hold the images and titles.

    # https://python.hotexamples.com/examples/splinter/Browser/find_by_css
    # /python-browser-find_by_css-method-examples.html
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    html = browser.html
    img_soup = soup(html, 'html.parser')
    hemispheres = img_soup.find_all("div", class_="item")

    for hemisphere in hemispheres:
        try:
            img_url = hemisphere.find("a").get("href")
            sample_page = browser.visit(f"{url}{img_url}") 
            title = hemisphere.find("h3").text
            full_img_click = browser.find_by_text('Sample').click()
            full_img_soup = soup(browser.html, 'html.parser')
            full_img = full_img_soup.find("a", string="Sample").get("href")
            
            #https://stackoverflow.com/questions/38395751/
            # python-beautiful-soup-find-string-and-extract-following-string
            # print(full_img)
            
            img_url_scrape = url + full_img
            Hemisphere_url_title = {"Image Url": img_url_scrape, "Title": title}

            

            hemisphere_image_urls.append(Hemisphere_url_title)
        except AttributeError:
            return None
        browser.back()
        

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

    # In[541]:


    # 4. Print the list that holds the dictionary of each image url and title.
    #hemisphere_image_urls


    # In[542]:


    # 5. Quit the browser
    # browser.quit()


    # In[ ]:




