import matplotlib.pyplot as plt
from datetime import *
import requests
from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

class DailyTemperature:
    temperature = 0.

    def __init__(self, date, temperaure):
        self.date = date
        self.temperature = temperaure

    def __str__(self):
        return self.date.__str__() + ' ' + str(self.temperature)


def draw_plot(temperatures, step, start, end):
      temperaturesToDraw = temperatures
      data_x = []
      data_y = []
      try:
          startDate = datetime.strptime(start, '%d.%m.%Y').date()
      except:
          startDate = temperatures[0].date
      try:
          endDate = datetime.strptime(end, '%d.%m.%Y').date()
      except:
          endDate = temperatures[len(temperatures)-1].date

      temperaturesToDraw = [rate for rate in temperaturesToDraw if rate.date >= startDate and rate.date <= endDate]

      if step != 1:
          temperaturesToDraw = course_per_step(temperaturesToDraw, step)

      for temperature in temperaturesToDraw:
          data_x.append(temperature.date)
          data_y.append(temperature.temperature)

      plt.cla()
      plt.clf()

      plt.plot(data_x, data_y)
      plt.ylabel('График температуры в Москве')

      fig = plt.gcf()
      canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
      canvas.draw()
      canvas.get_tk_widget().place(x=200, y=50)
      window.geometry("900x600")

def course_per_step(temperatures, step):
      daysQuantity = len(temperatures)
      for stepSection in range(0, daysQuantity, step):
          if stepSection > daysQuantity:
              break
          endSection = stepSection + step - 1
          if endSection > daysQuantity:
              endSection = daysQuantity - 1

          stepTemp = temperatures[stepSection//step].temperature

          for day in range(stepSection, endSection - 1):
              stepTemp += temperatures[stepSection//step + 1].temperature
              temperatures.pop(stepSection//step + 1)

          temperatures[stepSection//step].temperature = stepTemp / step

      return temperatures



def main():
    
    url = 'https://api.meteostat.net/v1/history/daily?station=27612&start=2010-01-01&end=2020-04-01&key=XBuKlwBW'

    resp = requests.get(url)
    data = resp.json()
    temperatures = list()
    for day in data['data']:
        if day['temperature'] != None:
            temperatures.append( DailyTemperature( datetime.strptime(day['date'], '%Y-%m-%d').date(), day['temperature']) )
        elif day['temperature_max'] != None and day['temperature_min'] != None:
            temperatures.append( DailyTemperature( datetime.strptime(day['date'], '%Y-%m-%d').date(), day['temperature_max'] + day['temperature_min'] / 2 ) )

    step = selected.get()
    start = fromTxt.get()
    end = toTxt.get()
    if start == "":
        start = '0'
    elif end == "":
        end = '0'

    draw_plot(temperatures, step, start, end)

window = Tk()
window.geometry("200x350")
window.title("Practice3")
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