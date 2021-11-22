# Building the scraping app
###
# Dependencies

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

###
# Set-Ups

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    # headless True means the browser will not phyiscally open so we can watch it

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemis": mars_hemis(browser)
      }

    # Stop webdriver and return data
    browser.quit()
    return data  


###
# Start creating the program...


def mars_news(browser):
# When we add the word "browser" as an argument to our function, 
# we're telling Python that we'll be using the browser variable we defined outside the function. 
# All of our scraping code utilizes an automated browser, and without this section, our function wouldn't work.


    # Visit the mars nasa news site
    url3 = 'https://redplanetscience.com'
    browser.visit(url3)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    html3 = browser.html
    news_soup = soup(html3, 'html.parser')

    # We're going to add a try and except clause addressing AttributeErrors
    #  By adding this error handling, we are able to continue with our other scraping portions even if this one doesn't work.
    try: 
        slide_elem = news_soup.select_one('div.list_text')
        
        # chain get_text() method to find() and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # now use similar code to scrape the teaser paragraph
        news_paragraph = slide_elem.find('div',class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_paragraph

def featured_image(browser):

    # Visit URL
    url4 = 'https://spaceimages-mars.com'
    browser.visit(url4)

    # Find and click the full image button - it's 2 of 9 'button' tags found in the doc, so we'll use the [1] index
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # now that we're on the page with the full image, now we parse
    html4 = browser.html
    img_soup = soup(html4, 'html.parser')

    # error handling try/except block
    try:            
        # find the image URL
        img_url = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    
           
    # append this to the base url for a full url
    img_url_full = f'https://spaceimages-mars.com/{img_url}'
    
    return img_url_full

def mars_facts():
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    # df.set_index('description', inplace=True)
    

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(index=False)






def mars_hemis(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemi_img_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemis = {}
        img_find = browser.find_by_tag('h3')[i]
    #     1. click on each hemisphere link 

        img_find.click()
        
    #     2. retrieve image URL (.jpg)
        try:
            loop_html = browser.html
            loop_soup = soup(loop_html, 'html.parser')
            img_item = loop_soup.find('li').find('a')['href']
            img_link = f'https://marshemispheres.com/{img_item}'

            #     3. retrieve title

            title = loop_soup.find('h2').text
            hemis = {'title':title,'img_link':img_link}
            hemi_img_urls.append(hemis)
    #         print(hemi_img_urls)
            
            
        except BaseException as e:
            print(e)
            
    #     4. use browser.back()

        browser.back()
    return hemi_img_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())