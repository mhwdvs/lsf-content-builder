from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import lxml
import re
import os

url = "https://livestreamfails.com/top"
browser = webdriver.Chrome()
browser.get(url)
delay = 5 #seconds
browser.execute_script("loadPostTimeFrameSelect(this, 'day')") # uses js to filter posts from the last 24h

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-deck')))
    print("Page is ready!")

except TimeoutException:
    print("Page took too long to load!")

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

links = []
for link in soup.find_all("a", attrs={"href": re.compile("^https://livestreamfails.com/post/")}):
    links.append(link.get("href"))

links = list(set(links)) # removes duplicate links (bcause there are 3 different links for each post; picture, title etc)
print(links)
# links is now an array/list of all the links to the top posts of the past 24 hours

for link in links:
    browser = webdriver.Chrome()
    browser.get(link)
    delay = 5 #seconds
    clips = 0

    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-title')))
        print("Page is ready!")

    except TimeoutException:
        print("Page took too long to load!")

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')

    links = []
    for link in soup.find_all("source", attrs={"src": re.compile("^https://stream.livestreamfails.com/video/")}):
        links.append(link.get("src"))

    titles = []
    for link in soup.find_all("h4",{"class":"post-title"}):
        titles.append(link.text)

    print(links)
    print(titles)
    clips = clips + 1
    # break loop when total video time is greater than 5 minutes
    if clips > 14:
        break

for i in links:
	os.system("curl " + links[i] + " -o clip" + i)