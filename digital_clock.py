import sys
from tkinter import *
import time

def tick():
	time_string = time.strftime("%H:%M:%S")
	clock.config(text=time_string)
	clock.after(200, tick)

root = Tk(screenName="My_Clock")
clock = Label(root, font= ("times", 50, "bold"), bg= "White")
clock.grid(row= 0, column= 1)
tick()
root.mainloop()