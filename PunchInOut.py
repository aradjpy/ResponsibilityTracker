from tkinter import *
import time as t
from datetime import datetime as dt
# import pandas as pd
import numpy as np
import os

root=Tk()


root.title('punch In Out')
root.geometry('500x500')
root.resizable(0,0)


root.columnconfigure(0,weight=100)
root.rowconfigure(0,weight=33)
root.rowconfigure(1,weight=33)
root.rowconfigure(2,weight=33)

topSec = Frame(root)
topSec.grid(row=0,column=0,sticky='nsew')

topSec.rowconfigure(0,weight=100)
topSec.columnconfigure(0,weight=50)
topSec.columnconfigure(1,weight=50)

isPunchedIn=False
thisTime = None
timeData = None
secondsPassed = 0
minutesPassed = 0
hoursPassed = 0

def timer():
    global isPunchedIn
    global TimerLable
    global timeData
    global secondsPassed
    global minutesPassed
    global hoursPassed

    secondsPassed+=1
    arr = np.array(list(TimerLable["text"]))
    if secondsPassed < 60:
        arr[-2:] = list('0' + str(secondsPassed)) if len(str(secondsPassed)) < 2 else list(str(secondsPassed))
        TimerLable.config(text=''.join(arr))
    elif minutesPassed < 60:
        secondsPassed = 0
        minutesPassed += 1
        arr[-2:] = list('0' + str(secondsPassed)) if len(str(secondsPassed)) < 2 else list(str(secondsPassed))
        arr[-5:-3] = list('0' + str(minutesPassed)) if len(str(minutesPassed)) < 2 else list(str(minutesPassed))
        TimerLable.config(text=''.join(arr))
    else:
        minutesPassed = 0
        hoursPassed += 1
        arr[-2:] = list('0' + str(secondsPassed)) if len(str(secondsPassed)) < 2 else list(str(secondsPassed))
        arr[-5:-3] = list('0' + str(minutesPassed)) if len(str(minutesPassed)) < 2 else list(str(minutesPassed))
        arr[0:2] = list('0' + str(hoursPassed)) if len(str(hoursPassed)) < 2 else list(str(hoursPassed))
        TimerLable.config(text=''.join(arr))
    timeData = root.after(1000,timer)
    # print(timeData)


def punchIn():
    global isPunchedIn
    global thisTime
    global secondsPassed

    if isPunchedIn == False:
        isPunchedIn=True
        try:
            with open(os.path.dirname(__file__) + '/punchIndate.txt', 'r+') as f:
                f.truncate(0)
                f.write(dt.now())
        except:
            with open(os.path.dirname(__file__)  + '/punchIndate.txt', 'w') as f:
                f.write(str(dt.now()))
    
    thisTime = t.time()
    secondsPassed = 0
    timer()
    # remember to start threading in order to do your timer :-)

def punchOut():
    global timeData
    isPunchedIn = False
    root.after_cancel(timeData)


punchIn = Button(topSec,text='Punch In',command=punchIn)
punchIn.grid(row=0,column=0,sticky='nsew')

punchOut = Button(topSec,text='Punch out',command=punchOut)
punchOut.grid(row=0,column=1,sticky='nsew')

timerSec = Frame(root)
timerSec.grid(row=1,column=0,sticky='nsew')


TimerLable = Label(timerSec, text="00:00:00",font=("", 22))
TimerLable.pack(expand=True)


bottmSec = Frame(root)
bottmSec.grid(row=2,column=0,sticky='nsew')


leadWorkingTimes = Button(bottmSec, text='leaderboard')
leadWorkingTimes.pack(anchor='center',fill='both',expand=True)
print(os.getcwd() + '/punchIndate.txt')

root.mainloop()