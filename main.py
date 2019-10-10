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
browser.close()

links = []
for link in soup.find_all("a", attrs={"href": re.compile("^https://livestreamfails.com/post/")}):
    links.append(link.get("href"))

links = list(set(links)) # removes duplicate links (bcause there are 3 different links for each post; picture, title etc)
print(links)
# links is now an array/list of all the links to the top posts of the past 24 hours
videourls = []
titles = []
clips = 0

for link in links:
    browser = webdriver.Chrome()
    browser.get(link)
    delay = 5 #seconds

    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-title')))
        print("Page is ready!")

    except TimeoutException:
        print("Page took too long to load!")

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    browser.close()

    links = []
    for link in soup.find_all("source", attrs={"src": re.compile("^https://stream.livestreamfails.com/video/")}):
        videourls.append(link.get("src"))

    titles = []
    for link in soup.find_all("h4",{"class":"post-title"}):
        titles.append(link.text)

    print(videourls)
    print(titles)
    clips = clips + 1
    # break loop when total video time is greater than 5 minutes
    if clips > 1:
        break

print("All video urls:")
print(videourls)

for i in range(len(videourls)):
    os.system("curl " + videourls[i] + " -o clip" + str(i) +".mp4")
    os.system("ffmpeg -i clip" + i + ".mp4 -vf scale=1920:1080 out" + i + ".ts")


#used ffmpeg to cocant 15 MPEG-2 files losslessly into a single MPEG-2 output file, which must then be reencoded into mp4
#os.system("""ffmpeg -i "concat:out1.ts|out2.ts|out3.ts|out4.ts|out5.ts|out6.ts|out7.ts|out8.ts|out9.ts|out10.ts|out11.ts|out12.ts|out13.ts|out14.ts|out15.ts" -c copy final.ts""")
#os.system("ffmpeg -i final.ts -o final.mp4")
os.system("ffmpeg-concat -t circleopen -d 100 -f jpg -o final.mp4 clip0.mp4 clip1.mp4")