import pandas as pd
import tkinter
from tkinter import *
from numpy import *
from PIL import Image, ImageTk
import os

os.chdir("C:\\Users\\tangz\\Documents\\GitHub\\Ned")
count=-1


word=pd.read_csv("List.csv", encoding='utf-8')
English=list(word.English)
Chinese=list(word.中文)
Frequecy =list(word.次数)
arr=len(English)
Overall = list(word.总次数)
same=list(word.同义)
x=zeros(arr)
y=zeros(arr)
c = list(zip(English, Chinese, Frequecy,Overall,same))
random.shuffle(c)
English[:], Chinese[:],Frequecy[:] ,Overall[:],same[:]= zip(*c)


def on_closing():
    global Frequecy
    global Overall
    global word
    Frequecy= x + Frequecy
    Overall=y+Overall
    word.English = pd.Series(English)
    word.中文 = pd.Series(Chinese)
    word.次数 = pd.Series(Frequecy)
    word.同义=pd.Series(same)
    word.总次数=pd.Series(Overall)
    ned=ones(arr)-Frequecy/Overall
    word.正确率=pd.Series(ned)
    global word1
    word=word[(word.正确率<0.7) | (word.总次数<3)]
    word.to_csv("List.csv",encoding='utf_8_sig',index=False)
    root.destroy()


def search(event=None):
    verbal=text.get("1.0",END)
    text.delete('1.0', 'end')
    verbal=verbal.strip('\n')
    if verbal in English:
        number=English.index(verbal)
        danci1 = str(Chinese[number])
        tongyi=str(same[number])
        text4.config(text=tongyi)
        text2.config(text=danci1, fg="Black")
        text.insert(END,verbal)
        root.update_idletasks()

def shanchu(event=None):
    text.focus_set()
    text.delete('1.0', 'end')

def delete(event=None):
    text.focus_set()

def processWheel(event):
    if event.delta < 0:
        text.delete('1.0', 'end')
        show_Answer()
    else:
        global count
        if count <= 0:
            return;
        count -= 1
        text.delete('1.0', 'end')
        danci = str(English[count])
        danci1 = str(Chinese[count])
        tongyi = str(same[count])
        text.insert(END,danci)
        text4.config(text=tongyi)
        text2.config(text=danci1, fg="Black")
        text3.config(text=str(count + 1) + ":" + str(arr))
        root.update_idletasks()

def show_Answer(event=None):
    global cur_word
    global count
    if count == arr-1:
        on_closing()
    count +=1
    y[count]=1
    danci=str(English[count])
    tongyi=str(same[count])
    text.insert(END,danci)
    text.tag_configure(danci, justify='center')
    #text.config(text=danci)
    text4.config(text=tongyi)
    text2.config(text='')
    text3.config(text=str(count+1)+":"+str(arr))
    root.update_idletasks()

def show_Answer1(event=None):
    global cur_word
    if count!=-1:
        danci=str(Chinese[count])
        text2.config(text=danci,fg = "Black")
        x[count]=0
        root.update_idletasks()
def show_Answer2(event=None):
    global cur_word
    if count != -1:
        danci=str(Chinese[count])
        text2.config(text=danci,fg = "red")
        x[count]=1
        root.update_idletasks()

'''def show_Answer4():
    global count
    if count<=0:
        return;
    count -= 1
    danci=str(English[count])
    danci1 = str(Chinese[count])
    tongyi=str(same[count])
    text.config(text=danci)
    text4.config(text=tongyi)
    text2.config(text=danci1,fg = "Black")
    text3.config(text=str(count + 1) + ":" + str(arr))
    root.update_idletasks()'''
root=tkinter.Tk()
root.title('给劳资背单词')

canvas=tkinter.Canvas(root,width=100,height=7,bd=0,highlightthickness=12)
img = ImageTk.PhotoImage(Image.open('peopleSpolaore.jpg'))
root.image=img
background_label = Label(root, image=img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas.pack()


text = Text(root, width=15, height=1,font=('',12))  # 30的意思是30个平均字符的宽度，height设置为两行
text.tag_add("center", "1.0", "end")
#text.bind("<Return>",search)
text.pack()
text.place(x=19,y=20)



text4 = Label(root, width=15, height=1,font=('',12))  # 30的意思是30个平均字符的宽度，height设置为两行
text4.pack(anchor=CENTER)
text4.place(x=19,y=90)

text2 = Label(root, width=15, height=1, font=('',10))  # 30的意思是30个平均字符的宽度，height设置为两行
text2.pack()
text2.place(x=26,y=150)
text3=Label(root,width=10,height=1,text=arr)
text3.pack(side='left')
text3.config( fg='Purple')
text3.place(x=55,y=188)


'''B1= tkinter.Button(root,text="下一个",command=show_Answer,relief=RIDGE,width=5,height=1)
B2= tkinter.Button(root,text="知道",command=show_Answer1,relief=RIDGE,width=5, height=1 )
B3= tkinter.Button(root,text="不知道",command=show_Answer2,relief=RIDGE,width=5, height=1 )
B4=tkinter.Button(root,text="上一个",command=show_Answer4,relief=RIDGE,width=5,height=1)

B1.pack()

#B1.bind("<Button-3>",show_Answer1())

B2.pack()
B3.pack()
B3.pack()

B1.place(x=90,y=160)
B2.place(x=90,y=184)
B3.place(x=45,y=184)
B4.place(x=45,y=160)'''

root.withdraw()  # hide window
root.resizable(False, False)
root.bind("<MouseWheel>",processWheel)
root.bind("<Button-1>",show_Answer2)
root.bind("<Button-3>",show_Answer1)
root.bind("<BackSpace>",delete)
root.bind("<Return>",search)
root.bind("<Delete>",shanchu)
# add some widgets to the root window...
root.update_idletasks()
root.deiconify()  # now window size was calculated
root.withdraw()  # hide window again
root.geometry("180x220+550+200")
root.deiconify()
root.attributes("-alpha",0.9)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
