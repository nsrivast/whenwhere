# Scrapes FullTextArchive for full-text books

import os
import sys
import time
import pdb

from selenium import webdriver
from bs4 import BeautifulSoup

# ======
# SCRAPE
# ======
if False:
  reload(sys)  
  sys.setdefaultencoding('utf8')
  chromedriver = "./chromedriver"
  os.environ["webdriver.chrome.driver"] = chromedriver
  driver = webdriver.PhantomJS()

  book_urls = []
  for i in range(42, 794):
    time.sleep(2)
    driver.get("http://www.fulltextarchive.com/search//{}/7945/".format(i))
    print("page {}".format(i))
    html = driver.page_source
    data = BeautifulSoup(html, 'lxml')
    results_div = data.find("div", {"id": "results"})

    for a in results_div.find_all("a"):
      book_url = a['href']
    
      with open("book_links.txt", "a") as c:
        c.write(book_url + "\n")

# ======
# DOWNLOAD
# ======

import csv
import requests

if False:
  with open('book_links.txt', 'rb') as f:
    reader = csv.reader(f)
    book_urls = list(reader)
  
  book_urls = [x[0] for x in book_urls]
  completed_urls = []
  n_start = 898
  for i, book_url in enumerate(book_urls[n_start:]):
    print(i)
    if not book_url in completed_urls:
      book_name = book_url[6:-1]
      book_url_true = 'http://www.fulltextarchive.com/pdfs/{}.pdf'.format(book_name)
      response = requests.get(book_url_true, stream=True)
      
      with open('./texts/pdfs/{}.pdf'.format(book_name), 'wb') as f:
        f.write(response.content)
    
      completed_urls.append(book_url)


# ======
# CONVERT TO TEXT
# ======

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import glob
import re

#converts pdf, returns its text content as a string
def convert(fname, pages=None):
  if not pages:
    pagenums = set()
  else:
    pagenums = set(pages)
  output = StringIO()
  manager = PDFResourceManager()
  converter = TextConverter(manager, output, laparams=LAParams())
  interpreter = PDFPageInterpreter(manager, converter)
  infile = file(fname, 'rb')
  for page in PDFPage.get_pages(infile, pagenums):
    interpreter.process_page(page)
  infile.close()
  converter.close()
  text = output.getvalue()
  output.close
  return text 

if True:
  n_start = 35
  pdf_files = glob.glob("texts/pdfs/*.pdf")
  for i, pdf_file in enumerate(pdf_files[n_start:]):
    
    try:
      print("{}: {}".format(i + n_start, pdf_file))
      stub = pdf_file.split("/")[-1][:-4]
      text = convert(pdf_file)
      text_clean = re.sub(r"page \d+ / \d+", r"", text).replace("\n"," ")
      with open("texts/txts/{}.txt".format(stub), "w") as f:
        f.write(text_clean)
    except Exception as e:
      print(e)


#import csv

#with open('GEGlass.csv', 'wb') as csvfile:
#	spamwriter = csv.writer(csvfile, delimiter=',')
#	for i in reviews:
#		spamwriter.writerow(i)



