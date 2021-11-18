#!/usr/bin/env python
# coding: utf-8


##########################
# 10.3.2
# Practice with Splinter and BeautifulSoup
##########################



from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)



# http://quotes.toscrape.com/



# Scrape the Top 10 Tags

###

# Visit the Quotes to Scrape site
url = 'http://quotes.toscrape.com/'
browser.visit(url)



# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')



# Scrape the Title - use .text at the end to grab the text only
title = html_soup.find('h2').text
title

# IMPORTANT
# There are two methods used to find tags and attributes with BeautifulSoup:

# .find() is used when we want only the first class and attribute we've specified.
# .find_all() is used when we want to retrieve all of the tags and attributes.


# Scrape the top ten tags
tag_box = html_soup.find('div', class_='tags-box')

# tag_box
tags = tag_box.find_all('a', class_='tag')

# without using .text, we grab the whole line
tags

# now using .text again to only grab the text
for tag in tags:
    word = tag.text
    print(word)



# In the next cell, we'll create a for loop that will do the following:

# Create a BeautifulSoup object
# Find all the quotes on the page
# Print each quote from the page
# Click the "Next" button at the bottom of the page
# We'll use range(1, 6) in our for loop to visit the first five pages of the website.


for x in range(1, 6):
    html = browser.html
    quote_soup = soup(html, 'html.parser')
    quotes = quote_soup.find_all('span', class_='text')
    
    for quote in quotes:
        print('page:', x, '----------')
        print(quote.text)
        
    browser.links.find_by_partial_text('Next').click()



# SKILL DRILL
# Stretch your scraping skills by visiting Books to Scrape (Links to an external site.) 
# and scraping the book URL list on the first page.

# Visit the Books to Scrape site
url2 = 'http://books.toscrape.com/'
browser.visit(url2)

# Parse the HTML
html = browser.html
html_soup = soup(html, 'html.parser')

# bookurls occur at <h3 />'s

bookurls = html_soup.find_all('h3')
bookurls


# i can't figure out how to scrape the URL, only title...(???)
for book in bookurls:
    site = book.text
    print(site)





##########################
# 10.3.3
# Scrape Mars Data: The News
##########################



# Visit the mars nasa news site
url3 = 'https://redplanetscience.com'
browser.visit(url3)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# wait_time =1 ...
# The optional delay is useful because sometimes dynamic pages take a little while to load


html3 = browser.html
news_soup = soup(html3, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')
slide_elem

# Notice how we've assigned slide_elem as the variable to look for the <div /> tag and its descendent 
# (the other tags within the <div /> element)? This is our parent element. This means that this element holds all 
# of the other elements within it, and we'll reference it when we want to filter search results even further. 
# The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag 
# with the class of list_text. CSS works from right to left, such as returning the last item on the list 
# instead of the first. Because of this, when using select_one, the first matching element returned 
# will be a <li /> element with a class of slide and all nested elements within it.



# drill down on the 'slide_elem' variable to find only the title, which lives in 'content_title' class

slide_elem.find('div', class_='content_title')



# chain get_text() method to find() and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title



# now use similar code to scrape the teaser paragraph
news_p = slide_elem.find('div',class_='article_teaser_body').get_text()
news_p


# ##########################
# # 10.3.4
# # Scrape Mars Data: Featured Image
# ##########################

# # Feature Images
# 

# Visit URL
url4 = 'https://spaceimages-mars.com'
browser.visit(url4)



# Find and click the full image button - it's 2 of 9 'button' tags found in the doc, so we'll use the [1] index
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()



# now that we're on the page with the full image, now we parse
html4 = browser.html
img_soup = soup(html4, 'html.parser')



# find the image URL
img_url = img_soup.find('img', class_='fancybox-image').get('src')
img_url



# append this to the base url for a full url
img_url_full = f'https://https://spaceimages-mars.com/{img_url}'
img_url_full


# ##########################
# # 10.3.5
# # Scrape Mars Data: Mars Facts
# ##########################


import pandas as pd



df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df2 = pd.read_html('https://galaxyfacts-mars.com')[0]
df2



df.to_html()



browser.quit()



##########################
# 10.3.6
# Export to Python
##########################

