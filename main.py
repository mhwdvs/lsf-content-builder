from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import lxml
import re
import os
import subprocess

# define runtime variables
fadetime = 24*3 #3 seconds
fadein = fadetime

# funtion to get duration of clip for use later
def getLength(filename):
    result = subprocess.Popen(["ffprobe", "-show_streams", filename],
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    dirty = [x for x in result.stdout.readlines() if "nb_frames" in x.decode()]
    dirty = dirty[0]
    clean = re.findall(r'\d+', str(dirty))
    return int(clean[0])

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
print("-------------------")
print("All video urls:")
print(videourls)
print("-------------------")

# Downloads and preprocesses all clips
for i in range(len(videourls)):
    clipname = "clip" + str(i) + ".mp4"
    outname = "out" + str(i) + ".mp4"

    #download clip
    os.system("curl " + videourls[i] + " -o " + clipname)

    # all files will be made into 1080p, 24fps format to prevent any issues later on
    os.system("ffmpeg -i " + clipname + " -vf scale=1920:1080,fps=fps=24 " + outname)

    # Get file duration in frames
    frames = getLength(outname)
    print("")
    print(frames)
    print("")
    fadeout = frames - fadetime
    print(fadeout)
    print("")
    fadename = "faded" + str(i) + ".ts"
    os.system("ffmpeg -i " + outname + """ -vf "fade=in:0:""" + str(fadein) + """" 1""" + outname)
    os.system("ffmpeg -i 1" + outname + """ -vf "fade=out:"""+ str(fadeout) + ":" + str(fadetime) + """" 2""" + outname)
    os.system("ffmpeg -i 2" + outname + " " + fadename)


# combines all faded files together and transcodes them back to mp4
os.system("""ffmpeg -i "concat:faded0.ts|faded1.ts" -c copy final.ts""")
os.system("ffmpeg -i final.ts final.mp4")
