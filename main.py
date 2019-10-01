import requests

page = requests.get("https://livestreamfails.com/top")
links = page.text

# regex to get only links in the page
# remove unwanted links (nav bar etc)
# extract links and place into a list
# iterate over links
