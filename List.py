from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox, Tk, Canvas, Label, Text, Button
from csv import DictReader, DictWriter
import random




def text_input(text, tags, *, color=None):
    if color is None:
        color = default_color
    x = canvas.create_text(tags[0], font=tags[1], fill=color, text=text,
                           anchor=tags[3], tags=tags[2])
    return x


def on_closing(event=None):
    global word
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Frequecy= x + Frequecy
        # Overall=y+Overall
        # word.English = pd.Series(English)
        # word.中文 = pd.Series(Chinese)
        # word.错误次数 = pd.Series(Frequecy)
        # word.词性=pd.Series(same)
        # word.假名=pd.Series(kana)
        # word.总次数=pd.Series(Overall)
        for i in range(0, arr):
            if word[i]['总次数'] > 0:
                word[i]['正确率'] = 1 - word[i]['错误次数'] / word[i]['总次数']
            del word[i]['wrong'], word[i]['current']
        final_word = []
        for i in word:
            if i['总次数'] < 10:
                final_word.append(i)
            else:
                if i['正确率'] < 0.7:
                    final_word.append(i)
        with open(file_name, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = DictWriter(csvfile, fieldnames=word[0].keys())
            writer.writeheader()
            for i in final_word:
                writer.writerow(i)

        # word['正确率']=(pd.Series([1]*arr)-word.错误次数/word.总次数).fillna(0)
        # word=word[(word.正确率<0.7) | (word.总次数<10)]
        # word=word.drop(columns=['current'])

        # word.to_csv("List.csv",encoding='utf_8_sig',index=False)
        root.destroy()


def search(event):
    canvas.delete('text2')
    canvas.delete('text')
    canvas.delete('text3')
    canvas.delete('text4')
    canvas.delete('text5')
    verbal = text.get("1.0", 'end-1c')
    text_input(verbal, text_tags)
    text.place_forget()
    canvas.focus_set()
    if verbal in word_set:
        number = word_index[verbal]
        text_input(word[number]['词性'], text4_tags)
        text_input(word[number]['中文'], text2_tags)
        text_input(word[number]['假名'], text5_tags)
        # text2_position = canvas.bbox(text2)
        # canvas.move(text2, 0, -(text2_position[3] - text2_position[1]) / 2)
        # text5_position = canvas.bbox(text5)
        # canvas.move(text5, 0, -(text5_position[3] - text5_position[1]) / 2)
        root.update_idletasks()
    # number = word.index.iloc[word.English == verbal]

    return 'break'


def spelling_test(event=None):
    correct = word[count]['假名']
    verbal = text1.get("1.0", 'end')
    verbal = verbal.strip('\n')
    canvas.delete('text2')
    canvas.delete('text5')
    if verbal == correct:
        if word[count]['current'] == 0:
            word[count]['总次数'] += 1
            word[count]['current'] = 1
        if count < arr - 1:
            show_Answer()
        else:
            text_input(word[count]['中文'], text2_tags)
            text_input(word[count]['假名'], text5_tags)
            # danci = word.中文.iloc[count]
            # danci2 = word.假名.iloc[count]
            # text_input(danci2,text5_tags)
            # text5_position = canvas.bbox(text5)
            # canvas.move(text5, 0, -(text5_position[3] - text5_position[1]) / 2)
            # text2.config(text=danci, fg=f'{default_color}')
            # text_input(danci,text2_tags)
            # text2_position = canvas.bbox(text2)
            # canvas.move(text2, 0, -(text2_position[3] - text2_position[1]) / 2)
        root.update_idletasks()
    else:
        # danci = word.中文.iloc[count]
        # danci2 = word.假名.iloc[count]
        text_input(word[count]['中文'], text2_tags, color=error_color)
        text_input(word[count]['假名'], text5_tags, color=error_color)
        # text2.config(text=danci, fg=f"{error_color}")
        # text5.config(text=danci2, fg=f"{error_color}")
        # text5=text_input(danci2,text5_tags,color=error_color)
        # text5_position = canvas.bbox(text5)
        # canvas.move(text5, 0, -(text5_position[3] - text5_position[1]) / 2)
        # text2.config(text=danci, fg=f'{default_color}')
        # text2 = text_input(danci,text2_tags,color=error_color)
        # text2_position = canvas.bbox(text2)
        # canvas.move(text2, 0, -(text2_position[3] - text2_position[1]) / 2)
        if word[count]['current'] == 0:
            word[count]['总次数'] += 1
            word[count]['current'] = 1
        if word[count]['wrong'] == 0:
            word[count]['错误次数'] += 1
            word[count]['wrong'] = 1
        else:
            pass
        root.update_idletasks()
    return 'break'


def shanchu(event=None):
    focused_widget = root.focus_get()
    focused_widget.delete('1.0', 'end')


def delete(event=None):
    focused_widget = root.focus_get()


def processWheel(event):
    global count
    global text6, text
    try:
        text.place_forget()
    except:
        pass
    # text1.delete('1.0', 'end')
    if event.delta < 0:
        show_Answer()
    else:
        if count <= 0:
            return;
        canvas.delete('text3')
        canvas.delete('text2')
        canvas.delete('text5')
        canvas.delete('text')
        canvas.delete('text4')
        count -= 1

        # text.delete('1.0', 'end')
        # danci = word.English.iloc[count]
        # danci1 = word.中文.iloc[count]
        # danci2=word.假名.iloc[count]
        # tongyi = word.词性.iloc[count]
        # text.insert('end',danci)
        if word[count]['wrong'] == 0:
            text_input(word[count]['English'], text_tags)
            text_input(word[count]['中文'], text2_tags)
            text_input(word[count]['假名'], text5_tags)
            text_input(word[count]['词性'], text4_tags)
        else:
            text_input(word[count]['English'], text_tags)
            text_input(word[count]['中文'], text2_tags, color=error_color)
            text_input(word[count]['假名'], text5_tags, color=error_color)
            text_input(word[count]['词性'], text4_tags)
        # text4.config(text=tongyi)
        # text_input(tongyi,text4_tags)
        # text2.config(text=danci1, fg=f'{default_color}')
        # text5.config(text=danci2, fg=f'{default_color}')
        # text5 = text_input(danci2,text5_tags)
        # text5_position = canvas.bbox(text5)
        # canvas.move(text5, 0, -(text5_position[3] - text5_position[1]) / 2)
        # text2.config(text=danci, fg=f'{default_color}')
        # text3.config(text=str(count + 1) + ":" + str(arr))
        # text2.place(relx=0.995, rely=0.5, anchor='e')
        # text2 = text_input(danci1,text2_tags)
        # text2_position = canvas.bbox(text2)
        # canvas.move(text2, 0, -(text2_position[3] - text2_position[1]) / 2)

        text3 = text_input(str(count + 1) + ":" + str(arr), text3_tags, color='purple')
        text3_position = canvas.bbox(text3)
        canvas.move(text3, (text3_position[2] - text3_position[0]) / 2, 0)
        root.update_idletasks()


# Show next word
def show_Answer(event=None):
    global cur_word
    global count
    global text1
    text1.delete('1.0', 'end')
    # if count==-1:
    # text4.place(relx=0.005, rely=0.45, anchor='nw')
    # text2.place(relx=0.995, rely=0.5, anchor='e')
    # text5.place(relx=0.9, rely=0.5, anchor='e')
    # text1.delete('1.0', 'end')
    if count == arr - 1:
        return
    if count < arr - 1:
        count += 1
        if word[count]['current'] == 0:
            word[count]['总次数'] += 1
            word[count]['current'] = 1
    if count <= arr - 1:
        canvas.delete('text3')
        canvas.delete('text2')
        canvas.delete('text')
        canvas.delete('text4')
        canvas.delete('text5')
        # danci=word.English.iloc[count]
        # tongyi=word.词性.iloc[count]
        # text = text_input(danci,text_tags)
        # text4.config(text=tongyi,fg=f'{default_color}')
        # text_input(tongyi,text4_tags)
        # text2.config(text='')
        # text5.config(text='')
        text_input(word[count]['English'], text_tags)
        text_input(word[count]['词性'], text4_tags)
        text3 = text_input(str(count + 1) + ":" + str(arr), text3_tags, color='purple')
        text3_position = canvas.bbox(text3)
        canvas.move(text3, (text3_position[2] - text3_position[0]) / 2, 0)
        root.update_idletasks()
    return 'break'


# Correct answer
def show_Answer1(event):
    global cur_word
    if event.x_root != w_x or event.y_root != w_y:
        return
    else:
        show_me()


def show_me(event=None):
    if count != -1:
        canvas.delete('text2')
        canvas.delete('text5')
        canvas.delete('text')
        if word[count]['wrong'] == 1:
            word[count]['错误次数'] -= 1
            word[count]['wrong'] = 0
        text_input(word[count]['English'], text_tags)
        text_input(word[count]['中文'], text2_tags)
        text_input(word[count]['假名'], text5_tags)
        # danci=word.中文.iloc[count]
        # danci2=word.假名.iloc[count]
        # text2 = text_input(danci,text2_tags)
        # text = text_input(word.English.iloc[count],text_tags)
        # text2_position = canvas.bbox(text2)
        # canvas.move(text2, 0, -(text2_position[3] - text2_position[1]) / 2)
        # text5 = text_input(danci2,text5_tags)
        # text5_position = canvas.bbox(text5)
        # canvas.move(text5, 0, -(text5_position[3] - text5_position[1]) / 2)
        # text5.config(text=danci2, fg=f'{default_color}')
        # text2.config(text=danci,fg = f'{default_color}')
        root.update_idletasks()


# Wrong answer
def show_Answer2(event=None):
    global cur_word
    if count != -1:
        canvas.delete('text2')
        canvas.delete('text5')
        canvas.delete('text')
        # danci=word.中文.iloc[count]
        # text = text_input(word.English.iloc[count],text_tags,color=default_color)
        # text2=text_input(danci,text2_tags,color=error_color)
        # text2_position = canvas.bbox(text2)
        # canvas.move(text2, 0, -(text2_position[3] - text2_position[1]) / 2)
        # danci2=word.假名.iloc[count]
        # text5 = text_input(danci2,text5_tags,color=error_color)
        # text5_position = canvas.bbox(text5)
        # canvas.move(text5, 0, -(text5_position[3] - text5_position[1]) / 2)
        text_input(word[count]['English'], text_tags)
        text_input(word[count]['中文'], text2_tags, color=error_color)
        text_input(word[count]['假名'], text5_tags, color=error_color)

        if word[count]['current'] == 0:
            word[count]['总次数'] += 1
            word[count]['current'] = 1
        if word[count]['wrong'] == 0:
            word[count]['错误次数'] += 1
            word[count]['wrong'] = 1
        else:
            pass
        root.update_idletasks()


def position(event):
    global p_x, p_y, w_x, w_y
    p_x = event.x
    p_y = event.y
    w_x = event.x_root
    w_y = event.y_root


def move_app(e):
    # root.geometry(f'+{e.x_root - e.x}+{e.y_root - e.y}')
    root.geometry(f'+{e.x_root - p_x}+{e.y_root - p_y}')
    # root.geometry(f'+{root.winfo_x()+p_x}+{root.winfo_y()+p_y}')


def move_app_1(e):
    root.geometry(f'+{e.x_root - 200}+{e.y_root - 213}')


def find(event=None):
    canvas.delete('text')
    try:
        text1.place_forget()
    except:
        pass
    text.place(relx=0.005, rely=0.1, anchor='nw')
    text.focus_set()


def test(event=None):
    try:
        text.place_forget()
    except:
        pass
    if count < 0:
        show_Answer()
    else:
        canvas.delete('text3')
        canvas.delete('text2')
        canvas.delete('text5')
        canvas.delete('text')
        canvas.delete('text4')
        # text.delete('1.0', 'end')
        # danci = word.English.iloc[count]
        # danci1 = word.中文.iloc[count]
        # danci2=word.假名.iloc[count]
        # tongyi = word.词性.iloc[count]
        text_input(word[count]['English'], text_tags)
        text_input(word[count]['词性'], text4_tags)
        # text.insert('end',danci)
        # text_input(danci,text_tags)
        # text4.config(text=tongyi)
        # text_input(tongyi,text4_tags)
        text3 = text_input(str(count + 1) + ":" + str(arr), text3_tags, color='purple')
        text3_position = canvas.bbox(text3)
        canvas.move(text3, (text3_position[2] - text3_position[0]) / 2, 0)
        root.update_idletasks()
    text1.place(relx=0.005, rely=0.8, anchor='nw')
    text1.focus_set()


def exit_test(event=None):
    canvas.focus_set()
    try:
        text1.place_forget()
    except:
        pass


'''def show_Answer4():
    global count
    if count<=0:
        return;
    count -= 1
    danci=str(English[count])
    danci1 = str(Chinese[count])
    tongyi=str(same[count])
    danci2=str(kana[count])
    text5.config(text=danci2, fg=f'{default_color}')
    text.config(text=danci)
    text4.config(text=tongyi)
    text2.config(text=danci1,fg = f'{default_color}')
    text3.config(text=str(count + 1) + ":" + str(arr))
    root.update_idletasks()'''


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

# Select words or grammar
def selection():
    if messagebox.askokcancel("Selection", "Do you want to memorize words?"):
        return "Words.csv"
    else:
        return "Grammar.csv"

count = -1
root = Tk()
root.iconbitmap('kaki.ico')


root.title('给劳资背单词')
root.config(bg='grey15')
root.attributes('-transparentcolor', 'grey15')
root.overrideredirect(True)

img = Image.open('erika.jpg')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# window_width=int(screen_width/6.4)
# window_height=int(screen_height/6.4)
window_height = int(168.75)

window_width = int(img.size[0]/img.size[1]*window_height)
# window_height = int(225 - 61.25)
# word=pd.read_csv("List.csv", encoding='utf-8')
# word[['错误次数','总次数']]=word[['错误次数','总次数']].fillna(0)
img=img.resize((int(window_width*6.4),int(window_height*6.4)), Image.ANTIALIAS)



canvas = Canvas(root, bg='grey15', width=window_width, height=window_height, bd=0, highlightthickness=0)
img = add_corners(img, 150).resize((window_width, window_height), Image.ANTIALIAS)

img = ImageTk.PhotoImage(img)

# root.image=img
# background_label = Label(root, image=img)
# background_label.place(x=0, y=0, relwidth=1, relheight=1)
canvas.pack()


file_name=selection()

with open(file_name, newline='', encoding='utf-8-sig') as csvfile:
    word = list(DictReader(csvfile))
arr = len(word)
# Define order
order = list(range(arr))
random.shuffle(order)
# Unordered list
word = [word[i] for i in order]
# Japenese:order
word_index = {}
# Set of Japenese
word_set = set()
for i in range(0, arr):
    word_index[word[i]['English']] = i
    word_set.add(word[i]['English'])
    word[i]['current'] = 0
    word[i]['wrong'] = 0
    word[i]['总次数'] = int(word[i]['总次数'].strip() or 0)
    word[i]['错误次数'] = int(word[i]['错误次数'].strip() or 0)
    word[i]['正确率'] = 0
# kana=list(word.假名)
# English=list(word.English)
# Chinese=list(word.中文)
# Frequecy =list(word.错误次数)
# arr=len(English)
# arr=len(word.English)
# Overall = list(word.总次数)
# same=list(word.词性)
# word=word.sample(frac=1).reset_index(drop=True)
# c = list(zip(English, Chinese, Frequecy,Overall,same,kana))
# random.shuffle(c)
# English[:], Chinese[:],Frequecy[:] ,Overall[:],same[:],kana[:]= zip(*c)



default_color = 'black'
error_color = 'red'
# Change color
try:
    with open('Color.txt', encoding='utf-8') as f:
        color_1, color_2 = f.read().split(",")
        try:
            root.config(bg=color_1)
            default_color = color_1
        except:
            pass
        try:
            root.config(bg=color_1)
            error_color = color_2
        except:
            pass
except:
    pass
# 词汇
text_tags = [
    (1, window_height / 10),
    ('', 14, 'bold'),
    'text',
    'nw'
]
# 词性
text4_tags = [
    (1, window_height / 4 + 3),
    ('', 10),
    'text4',
    'nw'
]
# 中文
text2_tags = [
    (1, window_height / 10 * 6 - 5),
    ('', 12),
    'text2',
    'nw'
]
# 词数
text3_tags = [
    (window_width / 2, window_height - 12),
    ('', 8),
    'text3',
    'ne'
]
# 假名
text5_tags = [
    (1, window_height / 10 * 4),
    ('', 14, 'bold'),
    'text5',
    'nw'
]



text = Text(root, width=10, bg='grey100', height=1, font=('', 14, 'bold'), bd=0,
            borderwidth=0)  # 30的意思是30个平均字符的宽度，height设置为两行
text.tag_add("center", "1.0", "end")
text.bind("<Return>", search)
text.bind("<BackSpace>", delete)
text.bind("<Delete>", shanchu)
text.pack()

text1 = Text(root, width=20, height=1, font=('', 10), bd=0, borderwidth=0)  # 30的意思是30个平均字符的宽度，height设置为两行
text1.tag_add("center", "1.0", "end")
text1.bind("<Return>", spelling_test)
text1.bind("<BackSpace>", delete)
text1.bind("<Delete>", shanchu)


def text_tab(event=None):
    if count != arr - 1:
        correct = word[count]['假名']
        verbal = text1.get("1.0", 'end')
        verbal = verbal.strip('\n')
        if verbal != correct:
            if word[count]['current']==0:
                if word[count]['wrong'] == 0:
                    word[count]['错误次数'] += 1
                    word[count]['wrong'] = 1
                word[count]['总次数'] += 1
                word[count]['current'] = 1
            else:
                pass
        show_Answer()
    return 'break'


text1.bind("<Tab>", text_tab)
text1.bind("<Shift-Tab>",processWheel)
text1.bind("<Control-e>", exit_test)
text1.pack(expand=True)

# #词性
# text4 = Label(root, font=('',8),borderwidth=0)  # 30的意思是30个平均字符的宽度，height设置为两行
# text4.pack()
#
# # 中文
# text2 = Label(root,font=('',10),wraplength=1,borderwidth=0)  # 30的意思是30个平均字符的宽度，height设置为两行
# text2.pack()
#
# #假名
# text5 = Label(root,  font=('',12),wraplength=1,borderwidth=0)  # 30的意思是30个平均字符的宽度，height设置为两行
# text5.pack()


# 词数
# text3=Label(root, text=arr,borderwidth=0)
# text3.pack()
# text3.config( fg='Purple')
# text3.place(relx=0.5, rely=1.0,anchor='s')
# text3.bind("<B1-Motion>",move_app_1)
'''B1= tkinter.Button(root,text="下一个",command=show_Answer,relief=RIDGE,width=5,height=1)
#B2= tkinter.Button(root,text="知道",command=show_Answer1,relief=RIDGE,width=5, height=1 )
#B3= tkinter.Button(root,text="不知道",command=show_Answer2,relief=RIDGE,width=5, height=1 )
#B4=tkinter.Button(root,text="上一个",command=show_Answer4,relief=RIDGE,width=5,height=1)

#B1.pack()

#B1.bind("<Button-3>",show_Answer1())

#B2.pack()
#B3.pack()
#B3.pack()

#B1.place(x=90,y=160)
#B2.place(x=90,y=184)
#B3.place(x=45,y=184)
#B4.place(x=45,y=160)'''

root.withdraw()  # hide window
root.resizable(False, False)
root.bind("<MouseWheel>", processWheel)
# root.bind("<Button-2>",show_Answer1)
root.bind("<Button-3>", show_Answer2)
# add some widgets to the root window...
root.update_idletasks()
root.deiconify()  # now window size was calculated
root.withdraw()  # hide window again

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))


def change_setting(event=None):
    global default_color, error_color
    change_setting_0.place(relx=0.2, rely=0.1, anchor='nw')
    change_setting_1.insert('end', default_color)
    change_setting_1.focus_set()
    change_setting_3.insert('end', error_color)
    change_setting_1.place(relx=0.2, rely=0.3, anchor='nw')
    change_setting_2.place(relx=0.2, rely=0.5, anchor='nw')
    change_setting_3.place(relx=0.2, rely=0.7, anchor='nw')
    change_setting_4.place(relx=0.6, rely=0.7, anchor='nw')
    canvas.delete('text3')
    canvas.delete('text2')
    canvas.delete('text')
    canvas.delete('text4')
    canvas.delete('text5')


def setting_exit(event=None):
    global default_color, error_color
    change_setting_0.place_forget()
    change_setting_1.place_forget()
    change_setting_2.place_forget()
    change_setting_3.place_forget()
    change_setting_4.place_forget()
    try:
        Label(bg=change_setting_1.get("1.0", 'end-1c'))
        default_color = change_setting_1.get("1.0", 'end-1c')
        change_setting_1.configure(fg=default_color)
    except:
        pass
    try:
        Label(bg=change_setting_3.get("1.0", 'end-1c'))
        error_color = change_setting_3.get("1.0", 'end-1c')
        change_setting_3.configure(fg=error_color)
    except:
        pass
    change_setting_1.delete('1.0', 'end')
    change_setting_3.delete('1.0', 'end')
    with open('Color.txt', 'w', encoding='utf-8') as f:
        f.write(f'{default_color},{error_color}')
    global count
    if count <= arr - 1:
        if count < arr - 1:
            count += 1
            if word[count]['current'] == 0:
                word[count]['总次数'] += 1
                word[count]['current'] = 1

        text_input(word[count]['English'], text_tags)
        text_input(word[count]['词性'], text4_tags)
        # text4.config(text=tongyi,fg=f'{default_color}')
        text3 = text_input(str(count + 1) + ":" + str(arr), text3_tags, color='purple')
        text3_position = canvas.bbox(text3)
        canvas.move(text3, (text3_position[2] - text3_position[0]) / 2, 0)
        root.update_idletasks()
    canvas.focus_set()
    return 'break'


change_setting_0 = Label(font=("", 14), text="Change Default Color")
change_setting_1 = Text(root, width=10, bg='grey100', height=1, font=('', 12), bd=0, borderwidth=0)
change_setting_2 = Label(font=("", 14), text="Change Error Color")
change_setting_3 = Text(root, width=10, bg='grey100', height=1, font=('', 12), bd=0, borderwidth=0)
change_setting_3.configure(fg=error_color)
change_setting_4 = Button(root, text='Confirm', command=setting_exit)


def switch_down(Event=None):
    change_setting_3.focus_set()
    return 'break'


def switch_up(Event=None):
    change_setting_1.focus_set()
    return 'break'
def crop_picture(Event=None):
    root.destroy()
    def crop(Event=None):
        root=Tk()
        root.iconbitmap('kaki.ico')
        root.title('Crop background picture')
        root.overrideredirect(True)
        img=Image.open('erika.jpg')
        canvas = Canvas(root, width=int(img.size[0] / img.size[1] * window_height), height=int(168.75), bd=0, highlightthickness=0)
        img=img.resize((int(img.size[0] / img.size[1] * window_height), int(168.75)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        myimage = canvas.create_image(0, 0, image=img, anchor='nw')

        canvas.pack()
        def destroy(Event=None):
            root.destroy()
        root.bind('<Control-w>',destroy)
        root.after(1, lambda: canvas.focus_force())
        root.mainloop()
    crop()

change_setting_1.bind('<Tab>', switch_down)
change_setting_1.bind('<Return>', setting_exit)
change_setting_3.bind('<Return>', setting_exit)
change_setting_3.bind('<Tab>', switch_up)
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
root.deiconify()
root.attributes("-alpha", 0.98)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind('<Escape>', on_closing)
root.bind('<Control-w>', on_closing)
root.bind('<Control-q>', test)
root.bind('<Control-f>', find)
root.bind('<Control-s>', change_setting)
root.bind('<Control-c>', crop_picture)
root.lift()
root.call("wm", "attributes", ".", "-topmost", "true")

# put the image on canvas because canvas supports transparent bg
myimage = canvas.create_image(0, 0, image=img, anchor='nw')
canvas.tag_bind(myimage, '<ButtonRelease-1>', show_Answer1)
canvas.bind('<KeyRelease-Up>', processWheel)

canvas.bind("<KeyRelease-Left>", show_me)
canvas.bind("<KeyRelease-Right>", show_Answer2)
canvas.bind('<KeyRelease-Down>', show_Answer)
canvas.tag_bind(myimage, '<Button-1>', position)
canvas.tag_bind(myimage, '<B1-Motion>', move_app)
# canvas.tag_bind(myimage,"<ButtonPress-1>",start_move)
# canvas.tag_bind(myimage,"<ButtonRelease-1>", stop_move)
root.after(1, lambda: canvas.focus_force())
root.mainloop()
