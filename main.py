from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import lxml
import re
import os
import subprocess
import time

print("<------------------>")
print("LSF CONTENT BUILDER")
print("by @__ized - github.com/izedout")
print("")
print("PagChomp")
print("<------------------>")
print("")

# define runtime variables
fadetime = 24*3 #3 seconds
fadein = fadetime
options = Options()
options.add_argument("--headless")

# funtion to get duration of clip in frames
def getLength(filename):
    result = subprocess.Popen(["ffprobe", "-show_streams", filename],
        stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    dirty = [x for x in result.stdout.readlines() if "nb_frames" in x.decode()]
    dirty = dirty[0]
    clean = re.findall(r'\d+', str(dirty))
    return int(clean[0])

print("GETTING CLIPS:")
url = "https://livestreamfails.com/top"
print("Navigating to " + url + "!")
browser = webdriver.Chrome()
browser.get(url)
delay = 5 #seconds max loading time before being considered timed out
print("Filtering for posts made in the past 24h!")
browser.execute_script("loadPostTimeFrameSelect(this, 'day')") # uses js to filter posts from the last 24h

try:
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-deck')))
    print("Page is ready!")
except TimeoutException:
    print("Page took too long to load!")

html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
browser.close()

print("Parsing HTML!")
# Gets the links of all the posts on the current page
links = []
for link in soup.find_all("a", attrs={"href": re.compile("^https://livestreamfails.com/post/")}):
    links.append(link.get("href"))
links = list(set(links)) # removes duplicate links (bcause there are 3 different links for each post; picture, title etc)
print("Here are all of the top posts from the past 24h:" + str(links)) # links is now an array/list of all the links to the top posts of the past 24 hours
print("<----------------------->")
print("")

videourls = []
titles = []
clips = 0

print("ENUMERATING CLIPS:")
for link in links:
    print("Navigating to clip" + str(clips) + "!")
    browser = webdriver.Chrome(chrome_options=options)
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

    print("Parsing clip" + str(clips) + "!")
    for link in soup.find_all("source", attrs={"src": re.compile("^https://stream.livestreamfails.com/video/")}):
        videourls.append(link.get("src"))

    for link in soup.find_all("h4",{"class":"post-title"}):
        titles.append(link.text)

    clips += 1
    # break loop when the number of clips is 15
    if clips > 14:
        break

print("<------------------->")
print("All video urls:")
print(videourls)
print("All video titles:")
print(titles)
print("<------------------->")
print("")

# Downloads and preprocesses all clips
print("DOWNLOADING + PROCESSING CLIPS!")
for i in range(len(videourls)):
    # have to create additional files for ffmpeg to operate 
    clipname = "clip" + str(i) + ".mp4"
    outname = "out" + str(i) + ".mp4"

    #download clip
    print("Downloading clip" + str(i) + "!")
    os.system("curl " + videourls[i] + " -o " + clipname)

    # all files will be made into 1080p, 24fps format to prevent any issues later on
    # this has to be done seperate from fades, because fadeout transition relies on number of frames, which changes
    os.system("ffmpeg -i " + clipname + """ -vf scale=1920:1080,fps=fps=24,drawtext="fontfile=Lato-Bold.ttf:text='""" + str(titles[i]) +"""':fontcolor=white:fontsize=40:box=1:boxcolor=black@0.5:boxborderw=5:x=0:y=0" """ + outname)
    os.system("del " + clipname)

    # Add overlay with clip title here

    frames = getLength(outname)     # Get file duration in frames
    fadeout = frames - fadetime     # Gets the time in frames when the fadeout transition should begin

    # adds in and out fades and transcodes to MPEG2 simultaneously
    os.system("ffmpeg -i " + outname + """ -vf "fade=in:0:""" + str(fadein) + ",fade=out:"+ str(fadeout) + ":" + str(fadetime) + """" """ + str(i) + ".mp4")
    os.system("del " + outname)

print("<----------------------->")
print("")

print("RUNNING FINAL CONCAT AND TRANSCODE ON CLIPS!")
# makes folder with date
named_tuple = time.localtime()
time_string = time.strftime("%d-%m-%y", named_tuple)
os.system("mkdir " + time_string)
# combines all faded files together and transcodes them back to mp4
os.system("ffmpeg -safe 0 -f concat -i mylist.txt -c copy " + time_string + "/output.mp4")
os.system("del 0.mp4 && del 1.mp4 && del 2.mp4 && del 3.mp4 && del 4.mp4 && del 5.mp4 && del 6.mp4 && del 7.mp4 && del 8.mp4 && del 9.mp4 && del 10.mp4 && del 11.mp4 && del 12.mp4 && del 13.mp4 && del 14.mp4")
print("Done!")
