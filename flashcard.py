# TODO
# 1. Add play audio button
# 2. Toggle audio speed
# 3. Switch audio (original, alt, alt2)

#coding:utf-8
from datetime import datetime
import json

# TKinter imports
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Pygame mixer for playing audio
from pygame import mixer

import sys, os, random

global deck, data
deck = ""
data = []


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def play_audio(arg=0):

    global voice, n, lang

    if (voice == 1):
        selectedAudio = ""
    if (voice == 2):
        selectedAudio = "_alt"
    if (voice == 3):
        selectedAudio = "_alt2"

    # update audio file path
    audio_path = ''.join([
        "assets/decks/", deck, "/audio/", lang, "/",
        str(n), selectedAudio, ".mp3"
    ])
    # if audio exists, play
    if (os.path.isfile(resource_path(audio_path)) is True):
        mixer.music.load(audio_path)
        # play Chinese audio
        mixer.music.play()


def changeLang():

    global lang

    # switch language (audio)
    if (lang == "zh"):
        lang = "en"
        toggleLang.config(text="English")
    elif (lang == "en"):
        lang = "zh"
        toggleLang.config(text="中文")
    # default Chinese audio
    else:
        lang = "zh"
        toggleLang.config(text="中文")


# get card info from json
def getCard(nav='n'):

    global n, cn, py, wt, div, en, c_num, nav_prev, nav_next, voice, total

    # next card
    if (nav == 'n'):
        if ((n + 1) > total):
            n = 1
        else:
            n = n + 1
    # previous card
    elif (nav == 'p'):
        if ((n - 1) <= 0):
            n = total
        else:
            n = n - 1
    # random card from deck
    elif (nav == 'r'):
        n = random.randint(1, total)
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

    # update n / total
    card_number_full = "".join([str(card_number), "/", str(total)])
    c_num.config(text=card_number_full)

    play_audio()


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


# on search box update
def callback(sv):
    # remove non-numeric chars from input
    query = ''.join(c for c in sv.get() if c.isdigit())
    # print (query)
    # go to card
    getCard(query)


def quitApp(arg=0):
    root.destroy()
    exit()


# initialise pygame mixer
mixer.init()

# configure Tkinter window
root = Tk()
# This is the section of code which creates the main window
root.geometry('1080x720')
# Prevent Window resize
root.resizable(False, False)
root.configure(background='#f7f3d2')
# window title
windowTitle = "Dave's Chinese Flashcards"
root.title(windowTitle)

# used to store deck names
deck_list = []

# loop through dir names in decks folder
start = resource_path('assets/decks/')
for item in os.listdir(start):
    if os.path.isdir(os.path.join(start, item)):
        # add folder names to list
        deck_list.append(item)

# create select list with deck names
choice = StringVar(root)
choice.set(deck_list[0])  # default value

w = OptionMenu(root, choice, *deck_list)
w.config(font='Helvetica 20 bold', width=20)
w.place(relx=0.38, rely=0.3)


def select_deck():

    print("value is:" + choice.get())
    # remove title/select deck screen
    choiceBtn.destroy()
    w.destroy()
    title.destroy()

    # set deck
    global deck
    deck = choice.get()

    # global labels
    global n, cn, py, wt, div, en, c_num, nav_prev, nav_next, lang, voice, total, data, toggleLang

    # default audio voice
    voice = 1

    # which audio should be played
    lang = 'zh'  # en -> English, zh -> Chinese

    # Card number
    n = 1

    # Opening JSON file
    # replace encoding errors
    db_path = ''.join(['assets/decks/', deck, '/db.json'])
    f = open((resource_path(db_path)), encoding="utf8", errors="replace")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    total = len((data[1]["data"]))

    zh = (data[1]["data"][0]["zh"]).strip()
    pinyin = (data[1]["data"][0]["pinyin"]).strip()
    word_type = (data[1]["data"][0]["type"]).strip()
    english = (data[1]["data"][0]["en"]).strip()
    card_number = (data[1]["data"][0]["id"]).strip()
    card_number_full = "".join([str(card_number), "/", str(total)])

    prevArrow = "  <<  "
    nextArrow = "  >>  "

    # update audio file path
    audio_path = ''.join(
        ["assets/decks/", deck, "/audio/", lang, "/", card_number, ".mp3"])

    # if audio exists, play
    if (os.path.isfile(resource_path(audio_path)) is True):
        mixer.music.load(audio_path)
        # play Chinese audio
        mixer.music.play()

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
    en.pack(expand=YES, fill='both')

    # card number
    c_num = tk.Label(root,
                     text=card_number_full,
                     fg="white",
                     bg="#7314C0",
                     font="Helvetica 15 bold")
    c_num.pack()
    # place bottom-center
    c_num.place(relx=0.5, rely=0.94, anchor=CENTER)

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
    searchLabel = Label(text="card",
                        fg="white",
                        bg="#7314C0",
                        font="Helvetica 18 bold")
    searchLabel.place(relx=0.88, rely=0.01)
    search = Entry(textvariable=sv, bd=5, width=3, font="Helvetica 18 bold")
    search.place(relx=1.0, rely=0.0, anchor=NE)

    # language audio toggle
    toggleLang = tk.Button(text="中文",
                           width=15,
                           relief="raised",
                           fg="#7314C0",
                           font="Helvetica 18 bold",
                           command=changeLang)
    toggleLang.place(relx=0.0, rely=0.0, anchor=NW)

    # global var
    global voiceToggle, voiceStr

    voiceStr = "".join(["voice: ", str(voice)])
    # Choose Audio Voice
    voiceToggle = tk.Button(text=voiceStr,
                            width=15,
                            relief="raised",
                            fg="#7314C0",
                            font="Helvetica 18 bold",
                            command=selectVoice)
    voiceToggle.place(relx=0.0, rely=0.04, anchor=NW)

    # Play Audio button
    audioBtn = tk.Label(
        root,
        text=
        'Press 1 to switch between audio language\n\nPress 2 to change' \
            ' audio voice\n\nPress spacebar to play audio\n\nUse the' \
                ' arrow keys on your keyboard\n\n' \
                ' to navigate the deck\nPress R for random card',
        fg="white",
        bg="#7314C0",
        width=35,
        padx="5",
        pady="5",
        font="Helvetica 9 bold",
        anchor=W)
    # position next to top-left buttons
    audioBtn.place(x=0, y=115, anchor=W)

    # selected deck label
    current_deck = tk.Label(root,
                            text=(''.join(["Deck: ", deck])),
                            fg="white",
                            bg="#7314C0",
                            font="Helvetica 13 italic",
                            anchor=CENTER)
    current_deck.place(relx=0.88, rely=0.08)

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
    ''' Key bindings '''

    # bind esc to quit
    root.bind('<Escape>', quitApp)

    # bind spacebar to play audio
    root.bind('<space>', play_audio)

    # 1 changes audio language
    root.bind('1', lambda x: changeLang())

    # 2 changes TTS Voice
    root.bind('2', lambda x: selectVoice())

    # nav on click
    nav_next.bind('<Button-1>', lambda x: getCard())
    nav_prev.bind('<Button-1>', lambda x: getCard('p'))
    # nav on arrow keys
    root.bind('<Right>', lambda x: getCard())
    root.bind('<Left>', lambda x: getCard('p'))

    # play audio on click
    audioBtn.bind('<Button-1>', play_audio)

    # bind 'r' to random card
    root.bind('<r>', lambda x: getCard('r'))


# Title
title = tk.Label(root,
                 text="Dave's Flashcards",
                 font="Helvetica 30 bold",
                 bg="#f7f3d2",
                 anchor=N)
title.place(relx=0.38, rely=0.1)

# copyright label
currentYear = datetime.now().year
copy = "".join(["David Mumford - ", str(currentYear)])
author = tk.Label(root,
                  text=copy,
                  fg="white",
                  bg="#7314C0",
                  font="Helvetica 15 bold")
# position next to top-left buttons
author.place(relx=0.5, rely=1.0, anchor=S)

# Select deck button
choiceBtn = Button(root,
                   text="Open Deck",
                   command=select_deck,
                   fg="white",
                   highlightbackground="#7314C0",
                   padx="5",
                   pady="5",
                   width=15,
                   font="Helvetica 30 bold")
choiceBtn.place(relx=0.38, rely=0.4)
root.mainloop()
