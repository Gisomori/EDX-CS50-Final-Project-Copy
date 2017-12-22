import requests
from bs4 import BeautifulSoup

def get_rss_feed(website_url):
    if website_url is None:
        print("URL should not be null")
    else:
        x = []
source_code = requests.get("bbc.co.uk/news")
plain_text = source_code.text

FEED_LINKS_ATTRIBUTES = {
    (('type', 'application/rss+xml'),),
    (('type', 'application/atom+xml'),),
    (('type', 'application/rss'),),
    (('type', 'application/atom'),),
    (('type', 'application/rdf+xml'),),
    (('type', 'application/rdf'),),
    (('type', 'text/rss+xml'),),
    (('type', 'text/atom+xml'),),
    (('type', 'text/rss'),),
    (('type', 'text/atom'),),
    (('type', 'text/rdf+xml'),),
    (('type', 'text/rdf'),),
    (('rel', 'alternate'), ('type', 'text/xml')),
    (('rel', 'alternate'), ('type', 'application/xml')),
}
"link", {"type" : "application/rss+xml"}

soup = BeautifulSoup(plain_text,"lxml")

for attrs in FEED_LINKS_ATTRIBUTES:
    for link in soup.find_all("link", dict(attrs)):
        href = link.get('href')
        print(href)
        #print("RSS feed for " + website_url + "is -->" + str(href))
        x.append(href)
        return(x)