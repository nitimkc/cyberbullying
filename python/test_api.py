import requests
from bs4 import BeautifulSoup
import pandas as pd

# request data from website and store in a variable
website_url = requests.get("https://twitter.com/home")
website_content = website_url.text

# convert data to soup object for easy html parsing
soup = BeautifulSoup(website_content, "lxml")
my_table = soup.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"})
