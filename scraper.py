# ## Mission To Mars

# Import All Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import tweepy
import json
import time
import config


def scrape():
#Scraping for All Data
# ### NASA Mars News
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    html_news = browser.html
    soup_news = BeautifulSoup(html_news, 'html.parser')

    News_header = (soup_news.find('div', class_='content_title')).string
    News_article = (soup_news.find('div', class_='article_teaser_body')).string

    # ### JPL Mars Space Images - Featured Image

    url_feat = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_feat)
    browser.find_by_css('a.button').click()
    time.sleep(10)
    soup = BeautifulSoup(browser.html,'html.parser')
    end = soup.find('img',class_='fancybox-image')['src']
    JPL_image = "https://www.jpl.nasa.gov"+end

    # ### Mars Weather

    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    access_token = config.access_token
    access_token_secret = config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target = "@MarsWxReport"
    weather = (api.user_timeline(target, count=1, result_type="recent"))[0]["text"]

    # ### Mars Facts

    url_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_facts)[0]
    table_build = tables.to_html()

    # ### Mars Hemisphers
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    soup = BeautifulSoup(browser.html, 'html.parser')

    headers=[]
    titles = soup.find_all('h3')
    for title in titles:
        headers.append(title.text)

    images=[]
    count=0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count=count+1

    hemisphere_image_urls = []
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1

    data = {"News_Header":News_header,"News_Article":News_article,"JPL_Image":JPL_image,"Weather":weather,"Facts":table_build,"Hemispheres":hemisphere_image_urls}

    return data
# scrape()