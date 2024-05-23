from PIL import Image, ImageTk, ImageDraw
import win32com.client
import os
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
def make_icon(input_name,save_name):
    # img = Image.open(input_name).crop((420,0,1500,1080)).resize((1920,1920), Image.ANTIALIAS)
    img = Image.open(input_name).resize((1920, 1920), Image.ANTIALIAS)
    window_width = 128
    window_height = 128
    img = add_corners(img, 400).resize((window_width, window_height), Image.ANTIALIAS)
    img.save(save_name,sizes=[(128,128)])

def change_icon():
    # Change icon of shortcut
    shell=win32com.client.Dispatch('WScript.Shell')
    for i in os.listdir(r'D:\OneDrive - University of Warwick\Program\Special_Icon'):
        if os.path.isfile(rf'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\{i.split(".")[0]}.lnk'):
            shortcut = shell.CreateShortcut(rf'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\{i.split(".")[0]}.lnk')
            # loc = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\Microsoft\\Internet Explorer\\Quick Launch\\User Pinned\\TaskBar\\'
            # loc = os.path.join(loc, f"{i.split('.')[0]}.lnk")
            # target = r"P:\Media\Media Player Classic\mplayerc.exe"
            # wDir = r"P:\Media\Media Player Classic"
            # icon = r"P:\Media\Media Player Classic\mplayerc.exe"
            # shell = Dispatch('WScript.Shell')
            # shortcut = shell.CreateShortCut(loc)
            # shortcut.Targetpath = target
            # shortcut.WorkingDirectory = wDir
            # shortcut.IconLocation = icon
            shortcut.IconLocation=rf'D:\OneDrive - University of Warwick\Program\Special_Icon\{i},1'
            shortcut.save()
        else:
            continue
def change_background():
    img = Image.open('erika.jpg').crop((0, 0, 1500, 1080))
    img.save('erikaa.jpg')

if __name__ == "__main__":
    make_icon(r'D:\Program\QuickDrop\1654112662178.jpg',r'D:\OneDrive - University of Warwick\Program\Special_Icon\PyCharm.ico')
    #change_icon()