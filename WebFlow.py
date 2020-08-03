import pandas as pd
import regex as re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from IPython.display import HTML


# Speicific google chrome as web browser
webdriver_path = '/Users/alicewang/Desktop/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

# Download html with Selenium
url = 'https://forum.webflow.com/'
driver.get(url)

# Parse html with beautifulSoup
soup = BeautifulSoup(driver.page_source,'lxml')
post_links = []



# get the initial height of web page
# lastHeight = driver.execute_script("return document.body.scrollHeight")

# tell selenium to scroll down to the current bottom of webpage
# driver.execute_script("window.scrollTo(arguments[0], document.body.scrollHeight);", lastHeight)

# Parse html with beautifulSoup
soup = BeautifulSoup(driver.page_source, 'lxml')
# locate the html section with posts
body = soup.find('body')
main_outlet = body.find('div', {'class': "contents ember-view"})
# get all hyperlinks of post
all_a = main_outlet.findAll('a', {'class': 'title raw-link raw-topic-link'})
for a in all_a:
    post_link = a.get('href')
    print(post_link)
    post_links.append(post_link)


usernames = []
likes = []
categories = []
title_tags = []
contents = []

for link in post_links[1:]:
    url = 'https://forum.webflow.com'+link
    driver.get(url)

    # Parse html with beautifulSoup
    soup = BeautifulSoup(driver.page_source, 'lxml')
    header = soup.find('div',{'class':'title-wrapper'})
    title_tag = header.find('a', {'class': 'fancy-title'}).getText().strip()
    cat_tag = header.find('div', {'class': 'topic-category ember-view'}).findAll('span', {'class': 'category-name'})
    category = cat_tag[0].getText()
    post_class = soup.find('div', {'class': 'container posts'})
    all_posts = post_class.find('div', {'class': 'post-stream'})
    for reply in all_posts.findAll('article', {'id': re.compile("post_[0-9]*[0-9]")}):
        partial = reply.find('div', {'class': 'names trigger-user-card'})
        usernames.append(partial.find('span', {'class': re.compile("^first username")}).getText())
        contents.append(reply.find('div', {'class': 'cooked'}).getText())
        check = reply.find('li', {'class': "secondary likes"})
        if check is not None:
            likes.append(check.find('span').getText())
        else:
            likes.append("0")

        title_tags.append(title_tag)
        categories.append(category)

    posts_dict = {}
    posts_dict['username'] = usernames
    posts_dict['title_tag'] = title_tags
    posts_dict['category'] = categories
    posts_dict['content'] = contents
    posts_dict['likes'] = likes

    df = pd.DataFrame.from_dict(posts_dict,orient='index')
    sentence = title_tag.replace(" ", "_")
    df.to_csv(sentence + '.csv', encoding='utf-8')







