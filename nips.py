import os
from lxml import html
import requests
import urllib.request


BASE_URL = 'https://papers.nips.cc/'
page = requests.get(BASE_URL)
tree = html.fromstring(page.content)
books = [ href.attrib['href'] for href in tree.xpath('//a') if 'book' in href.attrib['href']]


cwd = os.getcwd()


def make_dir(dir):
    if not os.path.exists(dir):
        print(">> making dir", dir)
        os.makedirs(dir)


for book in books:
    # if "2016" in book or "2017" in book or "2018" in book or "2019" in book:
    if "2017" in book or "2018" in book or "2019" in book:
        year = book.split("-")[-1]
        book_page = requests.get(BASE_URL + book)
        tree = html.fromstring(book_page.content)
        papers = [ href.attrib['href'] for href in tree.xpath('//a') if 'paper' in href.attrib['href']]
        for paper in papers:
            paper_page = requests.get(BASE_URL + paper)        
            tree = html.fromstring(paper_page.content)
            links = [ href.attrib['href'] for href in tree.xpath('//a') if 'pdf' in href.attrib['href']]
            for link in links:
                local = link.split('/')[-1]
                dir_save = os.path.join(cwd, "nips", year)
                make_dir(dir_save)
                local = os.path.join(dir_save, local)
                if not os.path.exists(local):
                    print(">> downloading", local)
                    urllib.request.urlretrieve(BASE_URL + link, local)
                else:
                    print(">> skipping", local)