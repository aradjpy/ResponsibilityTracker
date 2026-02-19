from tkinter import *
import time as t
from datetime import datetime as dt
import numpy as np
import os
from tkinter import messagebox
import math
import re

## remember to somehow make it able to fully run in the background like other background apps.

with open(os.path.dirname(__file__) + '/dayProductivity.txt', 'a') as f:
    f.write(str(dt.now()) + '\n\n')

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
topSec.columnconfigure(0,weight=33)
topSec.columnconfigure(1,weight=33)
topSec.columnconfigure(2,weight=33)

isPunchedIn=False
# thisTime = None
timeData = None
secondsPassed = 0
minutesPassed = 0
hoursPassed = 0
leadList = []
lList = None
dataL = {}
lastindex = 0
alreadyStarted = False
timePaused = False
secondaryTime = 0

def get_exp():
    global dataL
    print(lList.curselection())
    listedDataL = list(dataL.items())

    said=listedDataL[lList.curselection()[0]][1]
    messagebox.showinfo(title='Information', message=said)
    # OK, this is the game plan, you change the structure, so start introducing the explaination with the timers in the same text file, seprated by ~, now whenever the user inputs an explaination it also adds ~THE EXPLAINATION
    # Now we make that a dictionary, and then apply dict(sorted(dictionary.items())) then we make a list of all the dictionaries
    # then everytime the user clicks on either one, it takes the index of the list that's clicked and then chooses that one but this time with the explaination, and it also makes sure the ones with no explaination are just empty or with space that get's returned :)
    
def clearE():
    global dataL
    with open(os.path.dirname(__file__) + '/dayProductivity.txt', 'a') as f:
        for i,j in dataL.items():
            f.writelines(f'{int(i)/60} minutes on: {j}\n')

    with open(os.path.dirname(__file__) + '/times.txt', 'w') as f:
        f.write('')
    lList.delete(0,len(dataL))
    print(dataL)
    dataL = {}

def leaderBoard():
    global lList
    global lastindex
    global dataL

    lb = Tk()
    lb.title('Leader Board')
    lb.geometry('500x500')
    lb.resizable(0,0)
    fileInfo = ''
    lList=Listbox(lb,fg="black",font=("Aerial", 14, "bold italic"))
    show_explain = Button(lb, text='Show explaination', command=get_exp)
    clearDates = Button(lb, text='Clear Day', command=clearE)
    try:
        with open(os.path.dirname(__file__) + '/times.txt', 'r') as f:
            fileInfo = f.read()
            fileInfo = re.split(r'[~\n]',fileInfo)
        fTime = [fileInfo[i] for i in range(len(fileInfo)) if fileInfo[i] != '']
        lstT = []
        for i in range(0,len(fTime) - 1,2):
            lstT.append([fTime[i], fTime[i+1]])
        dataL.update(lstT)
        fTime = list(dataL.keys())
        fTime = [int(math.ceil(float(fTime[i]))) for i in range(len(fTime)) if fTime[i] != '']
        fTime.sort(reverse=True)
        dataL = dict(sorted(dataL.items(), key=lambda x: math.ceil(float(x[0])), reverse=True))
        lastindex = len(fTime) - 1
        [lList.insert(END,str(i) + ' Seconds') for i in fTime]
        lList.pack()
    except:
        messagebox.showerror(title='Not Found', message='Please make sure you have used the timer before :)')
    show_explain.pack()
    clearDates.pack()
    return fileInfo

    lb.mainloop()

def timer():
    global isPunchedIn
    global TimerLable
    global timeData
    global secondsPassed
    global minutesPassed
    global hoursPassed

    secondsPassed+=1
    arr = np.array(list(TimerLable["text"]))

    hoursPassed = secondsPassed // 3600
    minutesPassed = (secondsPassed % 3600) // 60
    secs = secondsPassed % 60

    arr[-2:] = list(f"{secs:02}")

    arr[-5:-3] = list(f"{minutesPassed:02}")

    arr[0:2] = list(f"{hoursPassed:02}")
    TimerLable.config(text=''.join(arr))
    timeData = root.after(1000,timer)


def punchIn():
    global isPunchedIn
    global thisTime
    global secondsPassed
    global timeData
    global timePaused

    if isPunchedIn == False:
        isPunchedIn=True
        try:
            with open(os.path.dirname(__file__) + '/punchIndate.txt', 'w') as f:
                f.write(dt.now())
        except:
            with open(os.path.dirname(__file__)  + '/punchIndate.txt', 'w') as f:
                f.write(str(dt.now()))
    
        # thisTime = t.time()
        secondsPassed = 0
        timer()
    elif timePaused == False:
        m = messagebox.askokcancel(title='timer already started!', message='You already have a timer, you sure you want to restart?')
        if m:
            # thisTime = t.time()
            secondsPassed = 0
            root.after_cancel(timeData)
            timer()
    else:
        #thisTime = t.time()
        # secondsPassed = secondaryTime - 1 
        secondsPassed-=1
        timePaused = False
        #there's a problem with pause, when you pause and write a note, it does not clock it, and the other problem is 
        # when you either pause, run and then re run it doesn't re start, or when you re start multiple times an issue happens.
        timer()

def punchOut():
    global timeData
    isPunchedIn = False
    global explaination
    global secondsPassed
    global minutesPassed
    global hoursPassed
    global thisTime

    timeSpent = ((hoursPassed * 60) * 60) + (minutesPassed * 60) + secondsPassed

    try:
        eg = str(explaination.get())
        if eg == '':
            eg = 'None :('
    except:
        eg = 'None :('
    

    with open(os.path.dirname(__file__) + '/times.txt', 'a+') as f:
        f.write(str(timeSpent) + '~' + eg + '\n')

    # if len(explaination.get()) > 1:
    #     with open(os.path.dirname(__file__) + '/explain.txt', 'a') as f:
    #         f.write(explaination.get())
    root.after_cancel(timeData)

def pauseTime():
    global thisTime
    global secondsPassed
    global timeData
    global timePaused
    global isPunchedIn
    global secondaryTime
    global hoursPassed
    global minutesPassed

    timePaused = True

    if isPunchedIn == False:
        messagebox.showerror(title='YOU HAVE TO START THE TIMER FIRST!')
    else:
        # secondaryTime = ((hoursPassed * 60) * 60) + (minutesPassed * 60) + secondsPassed
        root.after_cancel(timeData)





punchIn = Button(topSec,text='Punch In',command=punchIn)
punchIn.grid(row=0,column=0,sticky='nsew')


pause = Button(topSec,text='Pause',command=pauseTime)
pause.grid(row=0,column=1,sticky='nsew')

punchOut = Button(topSec,text='Punch out',command=punchOut)
punchOut.grid(row=0,column=2,sticky='nsew')

timerSec = Frame(root)
timerSec.grid(row=1,column=0,sticky='nsew')


TimerLable = Label(timerSec, text="00:00:00",font=("", 22))
TimerLable.pack(expand=True)


bottmSec = Frame(root)
bottmSec.grid(row=2,column=0,sticky='nsew')

bottmSec.rowconfigure(0,weight=100)
bottmSec.columnconfigure(0,weight=50)
bottmSec.columnconfigure(1,weight=50)


leadWorkingTimes = Button(bottmSec, text='leaderboard',command=leaderBoard)
leadWorkingTimes.grid(row=0,column=0,sticky='nsew' )
print(os.getcwd() + '/punchIndate.txt')

explaination = Entry(bottmSec)
explaination.grid(row=0,column=1,sticky='nsew')

# I add the budgeting section here


root.mainloop()