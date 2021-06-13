import json
import os
import parser
from tkinter import *

import tkcalendar as ttkcalendar
from tkinter import simpledialog as tkSimpleDialog, messagebox

from PIL import Image, ImageTk

# UI setting
from dateutil.parser import parse

bg_color = 'gray'

# Global variable
tweet_date_from = '* NOT SET *' # Variable load
tweet_date_to = '* NOT SET *' # Variable load

pathDir = os.getcwd()
date_from_save = None
date_to_save = None
root = None


def load_image(path, dimensions):
    load = Image.open(path).resize(dimensions, Image.ANTIALIAS)
    final_img = ImageTk.PhotoImage(load)

    return final_img


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

    global date_from_save
    date_from_save = tweet_date_from
    global date_to_save
    date_to_save = tweet_date_to


def display_ui():
    loadTweetDates()

    global root
    root = Toplevel()
    root.wm_title("CalendarDialog Demo")

    def date_click(obj, mode):

        cd = CalendarDialog(root)
        obj.config(state=NORMAL)
        value = cd.result

        if mode == 'from':
            global date_from_save
            date_from_save = value
        elif mode == 'to':
            global date_to_save
            date_to_save = value

        if value is None:
            value = ' '

        obj.delete(1.0, END)
        obj.insert(1.0, value, 'tag-center')
        obj.config(state=DISABLED)

    def save():
        global date_from_save
        global date_to_save
        final_datefrom = date_from_save
        final_dateto = date_to_save

        # If string then convert to date
        if isinstance(final_datefrom, str):
            final_datefrom = parse(final_datefrom).date()
        if isinstance(final_dateto, str):
            final_dateto = parse(final_dateto).date()

        if date_from_save is None or date_to_save is None:
            messagebox.showerror("ERROR", "Missing date!", icon='error')
            root.update()
            root.deiconify()
        elif final_datefrom > final_dateto:
            messagebox.showerror("ERROR", "Invalid date range!")
            root.update()
            root.deiconify()
        else:
            obj_json = {
                "tweet_dateFrom": str(date_from_save),
                "tweet_dateTo": str(date_to_save)
            }

            dirName = 'properties/'
            fileName = 'GeneralSettings.json'
            fullJsonPath = dirName + fileName

            with open(fullJsonPath, 'w') as f:
                json.dump(obj_json, f)

            f.close()
            close()

    def close():
        exit_window()

    from_lbl = Label(root,text="FROM", background=bg_color)
    from_lbl.config(font='Helvetica 10 bold')
    from_lbl.place(x=95,y=0)
    from_textbox = Text(root, height=2, width=16)
    from_textbox.tag_configure('tag-center', justify='center')
    from_textbox.insert(1.0, tweet_date_from, 'tag-center')
    from_textbox.config(state=DISABLED)
    from_textbox.place(x=50, y=20)
    icon_from = load_image(pathDir + '\\images\\calendar_from.png', (35,36))
    global date_from_save
    global date_to_save
    button_from = Button(root, text="Click me to see a calendar!", borderwidth=0, background=bg_color,
                         image=icon_from, height=30, width=25, command=lambda: date_click(from_textbox, 'from'))
    button_from.place(x=20,y=23)
    to_lbl = Label(root,text="TO", background=bg_color)
    to_lbl.config(font='Helvetica 10 bold')
    to_lbl.place(x=300,y=0)
    to_textbox = Text(root, height=2, width=16)
    to_textbox.tag_configure('tag-center', justify='center')
    to_textbox.insert(1.0, tweet_date_to, 'tag-center')
    to_textbox.config(state=DISABLED)
    to_textbox.place(x=250, y=20)
    icon_to = load_image(pathDir + '\\images\\calendar_to.png', (25,26))
    button_to = Button(root, borderwidth=0, background=bg_color,
                       image=icon_to, height=30, width=25, command=lambda: date_click(to_textbox, 'to'))
    button_to.place(x=220,y=23)

    button_save = Button(root, text="Save", borderwidth=3, height=2, width=17, command=lambda: save())
    button_save.configure(font=('Sans', '11', 'bold'), background='#216096', foreground='#eeeeff')
    button_save.place(x=20,y=80)
    button_cancel = Button(root, text="Cancel", borderwidth=3, height=2, width=17, command=lambda: close())
    button_cancel.configure(font=('Sans', '11', 'bold'), background='#660e0e', foreground='#eeeeff')
    button_cancel.place(x=220, y=80)

    root.update()
    root.title('Select Date Range')
    root.geometry("400x150")
    root.resizable(False, False)
    root.configure(background=bg_color)
    root.protocol('WM_DELETE_WINDOW', exit_window)
    root.mainloop()


def exit_window():
    global root
    root.destroy()
    root = None


class CalendarDialog(tkSimpleDialog.Dialog):
    """Dialog box that displays a calendar and returns the selected date"""
    def body(self, master):
        self.calendar = ttkcalendar.Calendar(master)
        self.calendar.pack()

    def apply(self):
        self.result = self.calendar.selection_get()


class CalendarWindow:
    @staticmethod
    def start_gui():
        if root is None:
            display_ui()
