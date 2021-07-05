import tkinter as tk
from tkinter import *
from tkcalendar import Calendar

root = Tk()

def submit():
    global ntweets
    global keyword
    global start_date
    ntweets = horizontal.get()
    keyword = k.get()
    start_date = cal.get_date()

def Close():
    root.destroy()

def get_date():
   cal.config(text=cal.get_date())

def responsetxt():
    btn = Label(root, text="Submitted")
    btn.pack()

# Title
root.title("TWITTER SENTIMENT ANALYSIS")

# root.iconbitmap('C:/Users/darre/Downloads/twitter_icon.ico')
root.geometry('500x500')
label1=Label(root, text="Enter keyword or hashtag:")
label1.pack()

# Keyword
k = Entry(root)
k.pack(pady=5.0)


# Slider
label2=Label(root, text="Select number of Tweets:").pack()
horizontal = Scale(root, from_=0, to=500, sliderlength=15, resolution=10, orient=HORIZONTAL)
horizontal.pack(pady = 20.0) 

# Date 
cal = Calendar(root, selectmode = 'day',
               year = 2020, month = 5,
               day = 22)
cal.pack(pady = 20.0)

button2 = Button(root, text="SUBMIT", bg="green", command=lambda: [submit(), responsetxt()])
button2.pack(pady = 20.0)

# Button for closing
exit_button = Button(root, text="Next", command=Close)
exit_button.pack(pady=20)



root.mainloop()
