from tkinter import *

import Pmw
from PIL import Image, ImageTk
from output_wordcloud import OutputWordCloud


# Global variables
root = None

# User Interface Setting
bgcolor = "#BDCCCC"


def load_image(path, dimensions):
    load = Image.open(path).resize(dimensions, Image.ANTIALIAS)
    final_img = ImageTk.PhotoImage(load)

    return final_img


def output_gui():
    inner_color = 'white'
    border_color = "#A7B7C0"

    def view():
        window = OutputWordCloud()
        window.start_gui()

    global root
    root = Toplevel()
    # Main Content
    output_lbl = Label(root, text="OUTPUT", fg="#700700", bg=bgcolor)
    output_lbl.config(font='Tahoma 14 bold')
    output_lbl.place(x=60, y=15)

    topic1_frame = Frame(root, height=26, width=26, bg=border_color)
    topic1_frame.place(x=30, y=80)
    topic1 = Label(topic1_frame, text="TOPIC 1", bg=inner_color, fg='black', height=20, width=20, anchor='n')
    topic1.config(font='Tahoma 12 bold')
    topic1.pack(fill=BOTH, expand="yes", padx=5, pady=5)

    topic2_frame = Frame(root, height=26, width=26, bg=border_color)
    topic2_frame.place(x=260, y=80)
    topic2 = Label(topic2_frame, text="TOPIC 2", bg=inner_color, fg='black', height=20, width=20, anchor='n')
    topic2.config(font='Tahoma 12 bold')
    topic2.pack(fill=BOTH, expand="yes", padx=5, pady=5)

    topic3_frame = Frame(root, height=26, width=26, bg=border_color)
    topic3_frame.place(x=490, y=80)
    topic3 = Label(topic3_frame, text="TOPIC 3", bg=inner_color, fg='black', height=20, width=20, anchor='n')
    topic3.config(font='Tahoma 12 bold')
    topic3.pack(fill=BOTH, expand="yes", padx=5, pady=5)

    topic3_frame = Frame(root, height=26, width=26, bg=border_color)
    topic3_frame.place(x=720, y=80)
    topic3 = Label(topic3_frame, text="OTHERS", bg=inner_color, fg='black', height=20, width=20, anchor='n')
    topic3.config(font='Tahoma 12 bold')
    topic3.pack(fill=BOTH, expand="yes", padx=5, pady=5)

    button_color = "#00A0ED"
    button_view = Button(root, text="VIEW", borderwidth=5, bg=button_color,
                             height=2, width=20, command=view)
    button_view.config(font='Helvetica 11 bold')
    button_view.place(x=380, y=500)

    # Button's Tool tip message
    btn_view_message = "Displays the output from the WordCloud"
    # bind tool tip to button
    tip_view = Pmw.Balloon(root)
    tip_view.bind(button_view, btn_view_message)

    # Menu Bar
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command= exit_window)

    menubar.add_cascade(label="File", menu=filemenu)
    # Main Frame
    icon_img = load_image("images/icon.png", (200, 200))
    root.title('(OUTPUT) Tweet Analysis with LDA')
    root.iconphoto(True, icon_img)
    root.geometry("970x600")
    root.resizable(False, False)
    root.configure(background=bgcolor, menu=menubar)
    root.protocol('WM_DELETE_WINDOW', exit_window)
    root.mainloop()


def exit_window():
    global root
    root.destroy()
    root = None


class Output:

    @staticmethod
    def start_gui():
        if root is None:
            output_gui()
