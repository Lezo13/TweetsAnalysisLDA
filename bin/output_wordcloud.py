from tkinter import *
from PIL import Image, ImageTk


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
    global root
    root = Toplevel()
    # Main Content
    output_lbl = Label(root, text="WORD CLOUD", fg="#700700", bg=bgcolor)
    output_lbl.config(font='Tahoma 14 bold')
    output_lbl.place(x=300, y=15)



    # Menu Bar
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=exit_window)

    menubar.add_cascade(label="File", menu=filemenu)
    # Main Frame
    icon_img = load_image("images/icon.png", (200, 200))
    root.title('(OUTPUT WORDCLOUD) Tweet Analysis with LDA')
    root.iconphoto(True, icon_img)
    root.geometry("780x400")
    root.resizable(False, False)
    root.protocol('WM_DELETE_WINDOW', exit_window)
    root.configure(background=bgcolor, menu=menubar)
    root.mainloop()


def exit_window():
    global root
    root.destroy()
    root = None


class OutputWordCloud:
    global root

    @staticmethod
    def start_gui():
        if root is None:
            output_gui()
