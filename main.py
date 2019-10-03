from bs4 import BeautifulSoup
from selenium import webdriver

url = "https://livestreamfails.com/top"
browser = webdriver.Chrome()
browser.get(url)
html = browser.page_source

soup = BeautifulSoup(html, 'lxml')
a = soup.find('section', 'wrapper')


# regex to get only links in the page
# remove unwanted links (nav bar etc)
# extract links and place into a list
# iterate over links
