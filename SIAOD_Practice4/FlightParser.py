import requests
import matplotlib.pyplot as plt
from datetime import datetime
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver

from datetime import date
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html)

    # links = soup.find("div", id="flightPageActivityLog")
    links = soup
    return links

def main():
    url = 'https://ru.flightaware.com/live/flight/AFL1132'

    # all_links = get_all_links(get_html(url))

    browser = webdriver.Opera()
    browser.get(url)
    content = browser.page_source
    # print(content)

main()