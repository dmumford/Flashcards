# TODO
# 1. Add play audio button
# 2. Toggle audio speed
# 3. Switch audio (original, alt, alt2)

import json

# TKinter imports
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Pygame mixer for playing audio
from pygame import mixer

# initialise pygame mixer
mixer.init()

# global labels
global n, cn, py, wt, div, en, c_num, nav_prev, nav_next, lang, voice

# default audio voice
voice = 1

# which audio should be played
lang = 'zh'  # en -> English, zh -> Chinese

# Card number
n = 1

# Opening JSON file
f = open('db.json')

# returns JSON object as
# a dictionary
data = json.load(f)


# get card info from json
def getCard(nav='n'):

    global n, cn, py, wt, div, en, c_num, nav_prev, nav_next, voice

    # next card
    if (nav == 'n'):
        n = n + 1
    # previous card
    elif (nav == 'p'):
        n = n - 1
    # user specified card
    else:
        n = int(nav)

    # take into account index 0
    cNum = n - 1

    # get new values
    zh = (data[1]["data"][cNum]["zh"]).strip()
    pinyin = (data[1]["data"][cNum]["pinyin"]).strip()
    word_type = (data[1]["data"][cNum]["type"]).strip()
    english = (data[1]["data"][cNum]["en"]).strip()
    card_number = (data[1]["data"][cNum]["id"]).strip()

    # update window with new values
    cn.config(text=zh)
    py.config(text=pinyin)
    wt.config(text=word_type)
    en.config(text=english)
    c_num.config(text=card_number)

    play_audio()


def play_audio(arg=0):

    global voice, n, lang

    if (voice == 1):
        selectedAudio = ""
    if (voice == 2):
        selectedAudio = "_alt"
    if (voice == 3):
        selectedAudio = "_alt2"

    # update audio file path
    audio_path = ''.join(
        ["audio/", lang, "/", str(n), selectedAudio, ".mp3"])
    mixer.music.load(audio_path)
    # play Chinese audio
    mixer.music.play()


zh = (data[1]["data"][0]["zh"]).strip()
pinyin = (data[1]["data"][0]["pinyin"]).strip()
word_type = (data[1]["data"][0]["type"]).strip()
english = (data[1]["data"][0]["en"]).strip()
card_number = (data[1]["data"][0]["id"]).strip()

prevArrow = "  «  "
nextArrow = "  »  "

# update audio file path
audio_path = ''.join(["audio/", lang, "/", card_number, ".mp3"])
mixer.music.load(audio_path)
# play Chinese audio
mixer.music.play()

root = Tk()

# This is the section of code which creates the main window
root.geometry('700x600')
root.configure(background='#f7f3d2')
root.title('TLT Flashcards')

# Chinese Character
cn = tk.Label(
    root,
    text=zh,
    # fg="light green",
    bg="#f7f3d2",
    pady=10,
    font="Helvetica 70 bold")
cn.pack()

# Pinyin
py = tk.Label(
    root,
    text=pinyin,
    fg="#44168a",
    bg="#f7f3d2",
    # pady=10,
    font="Helvetica 50")
py.pack()

# Word Type
wt = tk.Label(root,
              text=word_type,
              fg="grey",
              bg="#f7f3d2",
              pady=20,
              font="Helvetica 30 italic")
wt.pack()

# Divide line
div = tk.Label(root,
               text="________________________________________",
               fg="darkgrey",
               bg="#f7f3d2",
               font="Helvetica 30")
div.pack()

# show English word
en = Label(root,
           text=english,
           fg="#314282",
           bg="#f7f3d2",
           pady=25,
           font="Helvetica 30")
en.pack(expand=YES, fill=BOTH)

# card number
c_num = tk.Label(root,
                 text=card_number,
                 fg="white",
                 bg="#7314C0",
                 font="Helvetica 20 bold")
c_num.pack()
# place bottom-center
c_num.place(relx=0.5, rely=0.95, anchor=CENTER)

# Navigation arrows
# previous arrow
nav_prev = tk.Label(root,
                    text=prevArrow,
                    fg="white",
                    bg="#7314C0",
                    font="Helvetica 40 bold")
# position left
nav_prev.pack(side=LEFT)

# next arrow
nav_next = tk.Label(root,
                    text=nextArrow,
                    fg="white",
                    bg="#7314C0",
                    font="Helvetica 40 bold")
# position left
nav_next.pack(side=tk.RIGHT)

# Card search box
sv = StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
searchLabel = Label(text="card", fg="white", bg="#7314C0")
searchLabel.place(relx=0.88, rely=0.01)
search = Entry(textvariable=sv, bd=5, width=3)
search.place(relx=1.0, rely=0.0, anchor=NE)


# on search box update
def callback(sv):
    # remove non-numeric chars from input
    query = ''.join(c for c in sv.get() if c.isdigit())
    # print (query)
    # go to card
    getCard(query)


# nav on click
nav_next.bind('<Button-1>', lambda x: getCard())
nav_prev.bind('<Button-1>', lambda x: getCard('p'))
# nav on arrow keys
root.bind('<Right>', lambda x: getCard())
root.bind('<Left>', lambda x: getCard('p'))


def changeLang():

    global lang

    # switch language (audio)
    if (lang == "zh"):
        lang = "en"
        toggleLang.config(text="audio: English")
    elif (lang == "en"):
        lang = "zh"
        toggleLang.config(text="audio: 中文")
    # default Chinese audio
    else:
        lang = "zh"
        toggleLang.config(text="audio: 中文")


# language audio toggle
toggleLang = tk.Button(text="audio: 中文",
                       width=15,
                       relief="raised",
                       fg="#7314C0",
                       font="Helvetica 10 bold",
                       command=changeLang)
toggleLang.place(relx=0.0, rely=0.0, anchor=NW)

# global var
global voiceToggle, voiceStr


# switch audio voice on click
def selectVoice():

    global voice, voiceStr
    # construct voiceToggle text
    voiceStr = "".join(["voice: ", str(voice)])

    if (voice < 3):
        voice = voice + 1
    else:
        voice = 1

    # update voiceToggle text
    voiceToggle.config(text=voiceStr)


voiceStr = "".join(["voice: ", str(voice)])
# Choose Audio Voice
voiceToggle = tk.Button(text=voiceStr,
                        width=15,
                        relief="raised",
                        fg="#7314C0",
                        font="Helvetica 10 bold",
                        command=selectVoice)
voiceToggle.place(relx=0.0, rely=0.03, anchor=NW)

# Play Audio button
audioBtn = tk.Label(root,
                    text="▶",
                    fg="white",
                    bg="#7314C0",
                    font="Helvetica 25 bold")
# position next to top-left buttons
audioBtn.place(relx=0.12, rely=0.03, anchor=W)
# play audio on click
audioBtn.bind('<Button-1>', play_audio)

# global speedToggle

# def audioSpeed():
#    print('audioSpeed clicked')

# audio speed toggle
# speedToggle = tk.Button(
#                       text="speed: slow",
#                       width=15,
#                       relief="raised",
#                       fg="#7314C0",
#                       font="Helvetica 10 bold",
#                       command=audioSpeed)
# speedToggle.place(relx=0.0, rely=0.03, anchor=NW)

root.mainloop()
