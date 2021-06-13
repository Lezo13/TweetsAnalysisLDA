import csv
import os
import threading
import time
from tkinter import *
import sys
import json
from tkinter import tix
from tkinter.messagebox import askquestion
from tkinter.tix import Balloon

import Pmw
import numpy
import numpy as np
from dateutil.parser import *

from PIL import Image, ImageTk
from tkcalendar import DateEntry

from output import Output
from components.Calendar_Dialog import *
from constants import TwitterKeys, Settings
from models.TweetData import Tweet
import tweepy
import itertools
import pandas as pd

pathDir = os.getcwd()

# Define Settings Variables
user_target = Settings.user_target
tweet_count = Settings.tweet_count
include_retweet = Settings.contain_retweet
tweet_date_from = '* NOT SET *'
tweet_date_to = '* NOT SET *'

# Global Variables
tweet_data = None
display_count = 200
fr = None
view_output_window = None

# User Interface Setting
root = None
bgcolor = "#BDCCCC"
inner_color = "#A7B7C0"
done = True


def spin_cursor():
    sys.stdout.write('Loading: ')
    while True:
        for cursor in '|/-\\':
            sys.stdout.write(cursor)
            sys.stdout.flush()
            time.sleep(0.1) # adjust this to change the speed
            sys.stdout.write('\b')
            if done:
                return


def load_image(path, dimensions):
    load = Image.open(path).resize(dimensions, Image.ANTIALIAS)
    final_img = ImageTk.PhotoImage(load)

    return final_img


def getAllTweets():
    auth = tweepy.OAuthHandler(TwitterKeys.consumer_key, TwitterKeys.consumer_secret)
    auth.set_access_token(TwitterKeys.access_token_key, TwitterKeys.access_token_secret)
    api = tweepy.API(auth)

    # Spin Start Loading for console
    global done
    done = False
    spin_thread = threading.Thread(target=spin_cursor)
    spin_thread.start()

    all_tweets = []

    # Create directory for extraction
    dirName = 'data/'
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    # Query for fetching user's tweets based on date
    query = "\"from:" + user_target + " since:" + tweet_date_from + " until:" + tweet_date_to + "\""
    # Fetch Tweets
    jsonFileName = "text-query-tweets.json"
    fullPathJson = dirName + jsonFileName

    if os.path.exists(fullPathJson):
        os.remove(fullPathJson)
    os.system("snscrape --jsonl --max-results 500 twitter-search " + query + " > " + fullPathJson)

    # Tweets Data conversion to CSV
    if os.path.exists(fullPathJson):
        tweets_df = pd.read_json(dirName+'text-query-tweets.json', lines=True)

        for index, tweet in tweets_df.iterrows():
            tweet_content = Tweet()
            tweet_content.id = tweet['id']
            tweet_content.tweet_date = tweet['date']
            tweet_content.tweet_text = tweet['renderedContent']
            tweet_content.tweet_link = tweet['url']
            tweet_content.tweet_like_count = tweet['likeCount']
            tweet_content.tweet_reply_count = tweet['replyCount']
            tweet_content.tweet_retweet_count = tweet['retweetCount']
            tweet_content.tweet_quote_count = tweet['quoteCount']

            all_tweets.append(tweet_content)

        csvArchiveFileName = "tweets_archive_data.csv"
        fullPathArchiveCsv = dirName + csvArchiveFileName
        if os.path.exists(fullPathArchiveCsv):
            os.remove(fullPathArchiveCsv)
        tweets_df.to_csv(fullPathArchiveCsv)


    # CSV Generation of REAL DATA
    csvFileName = "tweets_data.csv"
    fullPathCsv = dirName + csvFileName
    if os.path.exists(fullPathCsv):
        os.remove(fullPathCsv)

    with open(fullPathCsv, 'w', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        header = ['ID', 'DATE', 'TWEET', 'LINK', 'LIKE COUNT', 'REPLY COUNT', 'RETWEET COUNT', 'QUOTE COUNT']
        writer.writerow(header)

        for tweet in all_tweets:
            row = [tweet.id, tweet.tweet_date, tweet.tweet_text, tweet.tweet_link, tweet.tweet_like_count,
                   tweet.tweet_reply_count, tweet.tweet_retweet_count, tweet.tweet_quote_count]
            writer.writerow(row)

    f.close()

    # Spin Finished Loading for console
    done = True
    spin_thread.join()
    sys.stdout.write('COMPLETE\n')

    return all_tweets


def initData():
   loadTweetDates()


def loadTweetDates():
    dirName = '\\properties\\'
    fileName = 'GeneralSettings.json'
    fullPath = pathDir + dirName + fileName

    if os.path.exists(fullPath):
        f = open(fullPath)
        data = json.load(f)
        global tweet_date_from
        tweet_date_from = data['tweet_dateFrom']
        global tweet_date_to
        tweet_date_to = data['tweet_dateTo']
        f.close()


def openDateDialog():
    window = CalendarWindow()
    window.start_gui()
    loadTweetDates()


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def main_window():
    initData()
    global root
    root = Tk()

    # Methods:
    def generate():
        loadTweetDates()
        global tweet_data
        tweet_data = getAllTweets()
        display_tweet_data()

    def clear():
        result = askquestion("Clear", "Are You Sure?", icon='warning')
        if result == 'yes':
            global fr
            clear_frame(fr)


    def display():
        window = Output()
        window.start_gui()

    def view_full():
        dirName = '\\data\\'
        fileName = 'tweets_data.csv'
        fullpath = pathDir + dirName + fileName

        if os.path.exists(fullpath):
            os.startfile(fullpath)
        else :
            messagebox.showerror("ERROR", "Missing CSV File. Generate first!", icon='error')

    # Main Content
    input_lbl = Label(root,text="INPUT TWEET", fg="#700700", bg=bgcolor)
    input_lbl.config(font='Tahoma 14 bold')
    input_lbl.place(x=80,y=55)

    button_color = "#00A0ED"


    # the button
    button_generate = Button(root, text="GENERATE", borderwidth=5, bg=button_color,
                             height=2, width=20, command=generate)
    button_generate.config(font='Helvetica 11 bold')
    button_generate.place(x=50,y=260)

    # Button's Tool tip message
    btn_generate_message = "Fetch all tweets from @" + user_target + \
                           " \nwithin the set dates. Which then \ndisplays the first 200 on the screen."
    # bind tool tip to button
    tip_generate = Pmw.Balloon(root)
    tip_generate.bind(button_generate, btn_generate_message)

    button_clear = Button(root, text="CLEAR", borderwidth=5, bg=button_color,
                          height=2, width=20, command=clear)
    button_clear.config(font='Helvetica 11 bold')
    button_clear.place(x=50, y=360)

    # Button's Tool tip message
    btn_clear_message = "Cleans up any shown data \non the canvas"
    # bind tool tip to button
    tip_clear = Pmw.Balloon(root)
    tip_clear.bind(button_clear, btn_clear_message)

    button_display = Button(root, text="DISPLAY", borderwidth=5, bg=button_color,
                            height=2, width=20, command=display)
    button_display.config(font='Helvetica 11 bold')
    button_display.place(x=50, y=460)

    # Button's Tool tip message
    btn_display_message = "Opens up the output window"
    # bind tool tip to button
    tip_display = Pmw.Balloon(root)
    tip_display.bind(button_display, btn_display_message)

    # Menu Bar
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="View Full Data (CSV)", command=lambda: view_full())
    filemenu.add_command(label="Settings", command=lambda: openDateDialog())
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=exit)

    menubar.add_cascade(label="File", menu=filemenu)

    # Main Container
    wholecontent = Frame(root, bg='#637684', borderwidth=10)
    wholecontent.place(x=300,y=40)

    wholecontent2 = Frame(root, bg='#637684', borderwidth=10)
    wholecontent2.place(x=300,y=390)

    outer_container = Frame(wholecontent, bg=inner_color)
    outer_container.pack()

    outer_container2 = Frame(wholecontent2, bg=inner_color,height=330)
    outer_container2.pack()

    content_lbl_temp = Label(outer_container, bg=inner_color, fg='#700700',
                             text="(FIRST " + str(display_count) + ") TWEETS WITHIN THE DURATION",
                             height=2, justify=LEFT, anchor="w")
    content_lbl_temp.config(font='Tahoma 11 bold')
    content_lbl_temp.pack(padx=10, fill=BOTH)
    content_lbl2_temp = Label(outer_container2, bg=inner_color, fg='#700700', text="PRE PROCESS WORDS",
                        height=2, justify=LEFT, anchor="w")
    content_lbl2_temp.config(font='Tahoma 11 bold')
    content_lbl2_temp.pack(padx=10, fill=BOTH)

    # Scrollbar
    wrapper1_temp = LabelFrame(outer_container)
    wrapper1_temp.pack(side=RIGHT, padx=10, pady=10, expand=1)
    wrapper2_temp = LabelFrame(outer_container2)
    wrapper2_temp.pack(side=RIGHT, padx=10, pady=10, expand=1)

    canvas = Canvas(wrapper1_temp, width=570)
    canvas.pack(side=LEFT, fill=BOTH, padx=10, expand=True)
    canvas2 = Canvas(wrapper2_temp, width=570)
    canvas2.pack(side=LEFT, fill=BOTH, padx=10, expand=True)




    # Items
    name = 'Inquirer'
    twitterUser = '@' + user_target + ' . '

    inquirer_img = load_image(pathDir + '\\images\\inquirer_twitter_img.jpg', (50, 50))

    def display_tweet_data():
        clear_frame(outer_container)
        clear_frame(outer_container2)

        content_lbl = Label(outer_container, bg=inner_color, fg='#700700',
                            text="(FIRST " + str(display_count) + ") TWEETS WITHIN THE DURATION",
                            height=2, justify=LEFT, anchor="w")
        content_lbl.config(font='Tahoma 11 bold')
        content_lbl.pack(padx=10, fill=BOTH)
        content_lbl2 = Label(outer_container2, bg=inner_color, fg='#700700', text="PRE PROCESS WORDS",
                             height=2, justify=LEFT, anchor="w")
        content_lbl2.config(font='Tahoma 11 bold')
        content_lbl2.pack(padx=10, fill=BOTH)

        # Scrollbar
        wrapper1 = LabelFrame(outer_container)
        wrapper1.pack(side=RIGHT, padx=10, pady=10, expand=1)
        wrapper2 = LabelFrame(outer_container2)
        wrapper2.pack(side=RIGHT, padx=10, pady=10, expand=1)

        canvas = Canvas(wrapper1, width=570)
        canvas.pack(side=LEFT, fill=BOTH, padx=10, expand=True)
        canvas2 = Canvas(wrapper2, width=570)
        canvas2.pack(side=LEFT, fill=BOTH, padx=10, expand=True)

        yscrollbar = Scrollbar(wrapper1, orient="vertical", command=canvas.yview)
        yscrollbar.pack(side=RIGHT, fill="y")
        yscrollbar2 = Scrollbar(wrapper2, orient="vertical", command=canvas2.yview)
        yscrollbar2.pack(side=RIGHT, fill="y")

        canvas.configure(yscrollcommand=yscrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas2.configure(yscrollcommand=yscrollbar2.set)
        canvas2.bind('<Configure>', lambda e: canvas2.configure(scrollregion=canvas2.bbox('all')))

        # Panel / Screen
        global fr
        fr = Frame(canvas)

        canvas.create_window((0, 0), window=fr, anchor="nw")

        global tweet_data
        for index, tweet in enumerate(tweet_data):
            if index > display_count:
                break
            rowIndex = index * 5

            date = tweet_data[index].tweet_date
            full_text = tweet_data[index].tweet_text
            imglogo = Label(fr, image=inquirer_img)
            imglogo.grid(row=rowIndex, column=0, rowspan=5)
            item_name = Label(fr, text=name)
            item_name.grid(row=rowIndex, column=1)
            item_user = Label(fr, text=twitterUser, anchor=E)
            item_user.grid(row=rowIndex, column=2)
            item_date = Label(fr, text=date)
            item_date.grid(row=rowIndex, column=3)
            item_fulltext = Label(fr, text=full_text, wraplength=510, justify=LEFT)
            item_fulltext.grid(row=rowIndex+1, column=1, columnspan=50, sticky=W)

    # Main Frame
    icon_img = load_image("images/icon.png", (200, 200))
    root.title(Settings.main_window_title)
    root.iconphoto(True, icon_img)
    root.geometry("1000x760")
    root.resizable(False, False)
    root.configure(background=bgcolor, menu=menubar)
    root.mainloop()


class Main:
    def __init__(self):
        main_window()


if __name__ == '__main__':
    Main()

