#!/usr/bin/env python3

from tkinter import *
from tkhtmlview import HTMLLabel, RenderHTML
from tkinter import filedialog
import tkinter.font as tkFont

# opcje

dark_value = True
pinned = False


complete = True
start_brackets = ["quotedbl","apostrophe","parenleft","less","bracketleft","braceleft"]
end_brackets = ["\"","'",")",">","]","}"]

darkbg = "#002b36"
darktext = "#839496"
darkselect = "#073642"
darkcursor="#93a1a1"
lightbg = "#fdf6e3"
lighttext = "#657b83"
lightselect = "#eee8d5"
lightcursor="#586e75"

htmltemplate = """
<h1> Witam w nowym edytorze tekstu </h1>
<h2> Na początek mały wstęp do edytora: </h2>
<div style="color:blue"> wciśnij klawisze (control) i (w) , żeby zobaczyć zawartość edytora jako stronę HTML </div>
<div style="color:cyan; background-color:black"> wciśnij klawisze (control) i (s) , żeby zapisać plik </div>
<div style="color:green"> wciśnij klawisze (control) i (o) żeby otworzyć istniejący plik </div>
<div style="color:yellow;background-color:black;"> klawisze ctrl+ , - , a , v, c, x, ... również działają </div>
<code style="color:green;background-color:black"> >$ ciekawostka - część kodu źródłowego tego edytora tekstu została napisana... \ 
w tymże edytorze tekstu :) _ </code> <br>
<i>notka - możliwość uruchomienia aplikacji ze skrótu w bashu... po prostu ./edytor_html.py . kompatybilne z folderami typu /bin/ ... </i>
<div>informacje o autorze: <img src="pinky-kde.gif"></img></div>
<ul>
<li> <a href="github.com/hacknorris-aka-penguin"> github </a> </li>
<li> <a href="mstdn.social/@hacknorris"> mastodon </a> </li>
<li> <a href="codeberg.org/hacknorris"> codeberg </a> </li>
</ul>
"""

helpcontents = """
    Lista skrótów klawiszowych:
    CTRL + w = podgląd pliku HTML
    CTRL + s = zapisz
    CTRL + o = otwórz
    CTRL + a = zaznacz wszystko
    CTRL + / = otwórz to okno pomocy
    CTRL + m = zmień motyw
    CTRL + + = powiększ
    CTRL + - = pomniejsz
    CTRL + t = przypnij edytro
    CTRL + * = ???
    ---------
    Tagi wspierane przez podgląd HTML:
    <h1> , <h2> , <h3> , <h4> , <h5> , <h6> ,
    <a href=""> , <img src=""> ,
    <b> , <em> , <i> , <mark> , <strong> , <u> ,
    <code> , <div> , <p> , <pre> , <span> ,
    <li> , <ol> , <ul> ,
    <table> , <tr> , <th> , <td> ,
    <br>
    ---------
    Opcje w kodzie źródłowym:
    zmienna "htmltemplate" - zawiera domyślną zawartość edytora
    zmienna "helpcontents" - zawiera zawartość tekstową tego okna (użyteczne przy modyfikowaniu aplikacji)
    zawartość "klawiszowce" - lista skrótów klawiszowych
    zawartość zmiennych między "darkbg" i "lightselect" - kolory motywów edytora (domyślnie - solarized)
    zmienna "switch_value" - ustawienie domyślnego motywu (normalnie powinien być ciemny ;p )
"""

# okna

def select_all(event):
    editor.tag_add(SEL, "1.0", END)
    editor.mark_set(INSERT, "1.0")
    editor.see(INSERT)
    return 'break'

def Save_Window(*args):
    filename = filedialog.asksaveasfilename(filetypes=[("All Files","*.*")], defaultextension = "*.html")
    if filename:
      with open(filename, "w", -1, "utf-8") as file:
        file.write(editor.get("0.0",END))

def Wiev_Window(*args):
    Second_Window = Toplevel()
    Second_Window.title("podgląd")
    entry1 = IntVar()
    html_label = HTMLLabel(Second_Window, html=editor.get("0.0",END))
    html_label.pack(fill="both", expand=True)
    html_label.fit_height()

def Open_Window(*args):
    openedfile = filedialog.askopenfile()
    editor.delete("0.0",END)
    editor.insert("0.0", openedfile.read())
	
def Help_Window(*args):
    Helper_Thing = Toplevel()
    Helper_Thing.title("pomoc")
    Label(Helper_Thing, text=helpcontents).pack()

def toggle(*args):
    global dark_value
    if dark_value == True:
        editor.config(background=darkbg , foreground=darktext , selectforeground=darktext, selectbackground=darkselect, insertbackground=darkcursor)
        dark_value = False
    else:
        editor.config(background=lightbg , foreground=lighttext , selectforeground=lighttext, selectbackground=lightselect, insertbackground=lightcursor)
        dark_value = True

def bigger(*args):
    editor.cur_fontsz = tkFont.Font( font=editor.cget('font') ).configure()['size']
    editor.cur_fontsz += 1
    editor.config( font=( editor.cget('font') , editor.cur_fontsz ) )

def smaller(*args):
    editor.cur_fontsz = tkFont.Font( font=editor.cget('font') ).configure()['size']
    editor.cur_fontsz -= 1
    editor.config( font=( editor.cget('font') , editor.cur_fontsz ))

def pinner(*args):
    global pinned
    if pinned == False:
        root.attributes('-topmost',True)
        pinned = True
    else:
        root.attributes('-topmost',False)
        pinned = False

def dang(*args):
    dangs = Toplevel()
    dangs.overrideredirect(True)
    dangs.attributes('-topmost', True)
    dmode = Label(dangs, text="Developer Mode").pack()

"""
global checker
checker=false
def increment:
    if checker = true:
        defsize = tkFont.Font(font='TkDefaultFont').configure()['size']
        editor.config(font=defsize+1)
        checker = true
    else:
        size = editor.cget("size")
        editor.configure(size=size+1)
"""

# główny kod

root = Tk()
root.title("edytor")
root.resizable(width=False, height=False)
global checker
checker=0
frame = Frame(root)
font = tkFont.Font()
editor = Text(frame, background=darkbg, foreground=darktext, selectforeground=darktext, selectbackground=darkselect, insertbackground=darkcursor, padx=0, pady=0, font=font)
editor.pack(expand=YES, fill=BOTH,side=TOP)
editor.insert('1.0', htmltemplate)
yscrollbar=Scrollbar(root, orient=VERTICAL, command=editor.yview)
yscrollbar.pack(side=RIGHT, fill=Y)
editor["yscrollcommand"]=yscrollbar.set
info = Label(root, text='wciśnij " CTRL + / " dla menu pomocy').pack(fill = BOTH,side = BOTTOM)

# klawiszowce

root.bind('<Control-s>', Save_Window)
root.bind('<Control-w>', Wiev_Window)
root.bind('<Control-o>', Open_Window)
root.bind('<Control-a>', select_all)
root.bind('<Control-slash>', Help_Window)
root.bind('<Control-m>', toggle)
root.bind('<Control-plus>',bigger)
root.bind('<Control-minus>',smaller)
root.bind('<Control-t>',pinner)
root.bind('<Control-KP_Multiply>',dang)


if complete == True:
    def append(self, evt=None):
         for i, j in enumerate(start_brackets):
             if self.keysym == start_brackets[i] :
                 editor.insert("insert", end_brackets[i])
    root.bind("<Key>", append )

# # # # #

frame.pack()

root.mainloop()

