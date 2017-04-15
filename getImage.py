import requests
from bs4 import BeautifulSoup
import urllib.request
import os
import errno

#https://twitter.com/search?f=images&q=%23cutepuppy&src=typd

query_entered = "#cutepuppy"  # >> %23cutepuppy

link = "https://twitter.com/search?f=images&q=%23"+ query_entered[1:]+"&src=typd"

def get_page(url):
    try:
        r = requests.get(url)
        soup = str(BeautifulSoup(r.content))
        return soup
    except:
        return ""


def get_next_target(page):
    start_link = page.find('data-url="')
    if start_link == -1:
        return None, 0
    else:
        start_quote = page.find('"', start_link+1)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos: ]
        else:
            break
    return links

content = get_page(link)
images = get_all_links(content)
print (images)


directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mediafiles")

pic_num = 0
for image in images:
    name = str(pic_num)+".jpg"
    filename = os.path.join(directory, name)
    urllib.request.urlretrieve(image, filename)
    pic_num+=1
