import requests
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import date
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')

    links = soup.find("table", class_="data").find_all_next("tr")

    return links

class DailyExchangeRate:
    date = date
    quantity = 1
    rate = 0.0
    def __init__(self, date, quantity, rate):
        self.date = date
        self.quantity = quantity
        self.rate = rate
    def __str__(self):
        return self.date + ' ' + str(self.quantity) + ' ' + str(self.rate)

def draw_plot(rates, step, start, end):
    ratesToDraw = rates
    data_x = []
    data_y = []
    try:
        startDate = datetime.strptime(start, '%d.%m.%Y').date()
    except:
        startDate = rates[0].date
    try:
        endDate = datetime.strptime(end, '%d.%m.%Y').date()
    except:
        endDate = rates[len(rates)-1].date

    ratesToDraw = [rate for rate in ratesToDraw if rate.date >= startDate and rate.date <= endDate]

    if step != 1:
        ratesToDraw = course_per_step(ratesToDraw, step)

    for rate in ratesToDraw:
        data_x.append(rate.date)
        data_y.append(rate.rate/rate.quantity)

    plt.cla()
    plt.clf()
    plt.plot(data_x, data_y, label='Rate')

    plt.ylabel('Динамика курса валюты Индийская рупия')

    df = pd.Series(data_y, index=data_x, name='Prices')

    short_rolling = df.rolling(window=10).mean().to_frame()
    long_rolling = df.rolling(window=100).mean().to_frame()

    plt.plot(long_rolling.loc[:, :].index, long_rolling.loc[:, 'Prices'],
            label='100-days SMA')
    plt.plot(short_rolling.loc[:, :].index, short_rolling.loc[:, 'Prices'],
            label='10-days SMA')

    fig = plt.gcf()
    fig.legend( bbox_to_anchor=(0.85, 0.97), ncol=3)

    # toolbar = NavigationToolbar2Tk(canvas, window)
    canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().place(x=200, y=50)
    window.geometry("900x600")
    # toolbar = NavigationToolbar2Tk(canvas, window)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    # plt.show()

def course_per_step(rates, step):
    daysQuantity = len(rates)
    for stepSection in range(0, daysQuantity, step):
        if stepSection > daysQuantity:
            break
        endSection = stepSection + step - 1
        if endSection > daysQuantity:
            endSection = daysQuantity - 1

        stepRate = rates[stepSection//step].rate
        stepQuantity = rates[stepSection//step].quantity
        for day in range(stepSection, endSection - 1):
            stepRate += rates[stepSection//step + 1].rate
            stepQuantity += rates[stepSection//step + 1].quantity
            rates.pop(stepSection//step + 1)

        rates[stepSection//step].rate = stepRate / step
        rates[stepSection // step].quantity = stepQuantity // step
    return rates

def main():
    url = "https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01270&UniDbQuery.From=28.03.2010&UniDbQuery.To=28.03.2020"

    all_links = get_all_links(get_html(url))
    all_links.pop(0)    # Remove
    all_links.pop(0)    # first and second tr objects

    rates = list()

    for tr in all_links:
        tds = tr.find_all("td")
        rates.append( DailyExchangeRate(datetime.strptime(tds[0].text, '%d.%m.%Y').date(), int(tds[1].text), float(tds[2].text.replace(',', '.') ) ) )

    step = selected.get()
    start = fromTxt.get()
    end = toTxt.get()
    if start == "":
        start = '0'
    elif end == "":
        end = '0'

    draw_plot(rates, step, start, end)

window = Tk()
window.geometry("200x350")
window.title("Practice1")
window.resizable(width=False, height=False)

selected = IntVar()

rad1 = Radiobutton(window, text='Day', value=1, variable=selected)
rad2 = Radiobutton(window, text='Week', value=7, variable=selected)
rad3 = Radiobutton(window, text='Month', value=30, variable=selected)
rad4 = Radiobutton(window, text='Year', value=365, variable=selected)

rad1.place(x=70, y=50)
rad2.place(x=70, y=75)
rad3.place(x=70, y=100)
rad4.place(x=70, y=125)

fromLbl = Label(window, text="from:")
fromLbl.place(x=70, y=175)
fromTxt = Entry(window, width=10)
fromTxt.place(x=70, y=200)

toLbl = Label(window, text="to:")
toLbl.place(x=70, y=225)
toTxt = Entry(window, width=10)
toTxt.place(x=70, y=250)

btn = Button(window, text="Go", command=main)
btn.place(x=70, y=300)

window.mainloop()
