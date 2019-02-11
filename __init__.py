# Using Python 3
import re
import urllib.request
from bs4 import BeautifulSoup
import requests
from os.path import basename

links = set()
already_downloaded = set()


class WebCrawler:
    # Page downloader
    def get_html(url):
        respond = urllib.request.urlopen(url)
        html = respond.read()
        return html

    # Page parser
    def download_img(url):
        global links
        global already_downloaded
        try:
            html = WebCrawler.get_html(url)
        except urllib.error.HTTPError:
            print("Warning:", url, "doesn't exist")
            return

        print('Getting ', url)
        if b'html' not in html[0:200]:
            return

        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        a_tags = soup.find_all('a', href=re.compile('^http://ualr.edu/informationscience/'))

        # /Download begin/
        images = soup.find_all('img')
        for img in images:
            if "http" in img.get('src'):
                Img = img.get('src')
                with open(basename(Img), "wb") as f:
                    f.write(requests.get(Img).content)
        # /Download finished/

        for a_tag in a_tags:
            if a_tag['href'] not in already_downloaded:
                links.add(a_tag['href'])
        for link in links:
            already_downloaded.add(link)
            links = links.difference(already_downloaded)
            WebCrawler.download_img(link)


WebCrawler.download_img("http://ualr.edu/informationscience/")