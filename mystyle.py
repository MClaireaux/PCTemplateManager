from tkinter import *

BACKGROUND = "#333333"
DARK = "#111111"
MID = "#666666"
LIGHT = "#dbd8e3"
FONT_NAME = "Courier"


def add_canvas(root, img, w, h):
    canvas = Canvas(root, width=w, height=h, bg=BACKGROUND, highlightthickness=0)
    canvas_img = PhotoImage(file=img)
    canvas.create_image(w / 2, h / 2, image=canvas_img)
    canvas.theimage = canvas_img
    return canvas

class HoverButton(Button):

    def __init__(self, root, img_enter, img_leave, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.img = PhotoImage(file=img_enter)
        self.img2 = PhotoImage(file=img_leave)

        self['image'] = self.img2

        self.bind('<Enter>', self.enter)
        self.bind('<Leave>', self.leave)

    def enter(self, event):
        self.config(image=self.img)

    def leave(self, event):
        self.config(image=self.img2)

class MyLabel(Label):
    def __init__(self, text, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15, "italic"), **kw):
        super().__init__(**kw)
        self['text'] = text
        self['bg'] = bg
        self['fg'] = fg
        self['font'] = font