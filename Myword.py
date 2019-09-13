import pandas as pd
import numpy as np
import os
import random
import tkinter
from tkinter import *
from numpy import *
from PIL import Image, ImageTk

os.chdir("C:\\Users\\tangz\\Desktop")
count=-1


word=pd.read_csv("Mywords.csv", encoding='utf-8')
English=list(word.English)
Chinese=list(word.中文)
Frequecy =list(word.次数)
arr=len(English)
Overall = list(word.总次数)
x=zeros(arr)
c = list(zip(English, Chinese, Frequecy,Overall))
random.shuffle(c)
English[:], Chinese[:],Frequecy[:] ,Overall[:]= zip(*c)

def on_closing():
    global Frequecy
    global Overall
    n = x + Frequecy
    Overall=Overall+ones(arr)
    word.English = pd.Series(English)
    word.中文 = pd.Series(Chinese)
    Frequecy = n
    word.次数 = pd.Series(Frequecy)
    word.总次数=pd.Series(Overall)
    ned=ones(arr)-Frequecy/Overall
    word.正确率=pd.Series(ned)
    if min(Overall)> 5:
        word[word['正确率'] >0.8]
    word.to_csv("Mywords.csv",encoding='utf_8_sig',index=False)
    root.destroy()

def show_Answer():
    global cur_word
    global count
    if count > arr:
        on_closing()
    count +=1
    danci=str(English[count])
    text.config(text=danci)
    text2.config(text='')
    root.update_idletasks()

def show_Answer1():
    global cur_word
    danci=str(Chinese[count])
    text2.config(text=danci,fg = "Black")
    root.update_idletasks()

def show_Answer2():
    global cur_word
    danci=str(Chinese[count])
    text2.config(text=danci,fg = "Purple")
    x[count]=1
    root.update_idletasks()

root=tkinter.Tk()
root.title('给劳资背单词')

canvas=tkinter.Canvas(root,width=100,height=7,bd=0,highlightthickness=10)
img = ImageTk.PhotoImage(Image.open('peopleSpolaore.jpg'))
root.image=img
background_label = Label(root, image=img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#canvas.create_image(200,50, anchor=NW,image=img)
canvas.pack()

text = Label(root, width=15, height=1,font=('',20))  # 30的意思是30个平均字符的宽度，height设置为两行
#text.config(font=("Courier", 10))
text.pack()

text2 = Label(root, width=15, height=1, font=(100))  # 30的意思是30个平均字符的宽度，height设置为两行
text2.pack(pady=30)

B1= tkinter.Button(root,text="下一个",command=show_Answer,relief=RIDGE)
B2= tkinter.Button(root,text="知道",command=show_Answer1,relief=RIDGE)
B3= tkinter.Button(root,text="不知道",command=show_Answer2,relief=RIDGE)

B1.pack()
B2.pack()
B3.pack()

root.withdraw()  # hide window
root.resizable(False, False)

# add some widgets to the root window...
root.update_idletasks()
root.deiconify()  # now window size was calculated
root.withdraw()  # hide window again
root.geometry("180x220+550+120")
root.deiconify()
root.attributes("-alpha",0.9)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

