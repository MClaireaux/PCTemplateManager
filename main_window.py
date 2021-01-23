from tkinter import *
from mystyle import HoverButton, MyLabel
from build_editor import BuildEditor
from inventory_editor import InventoryWindow
import datetime
from accounting import AccountingWindow
import pandas as pd

BACKGROUND = "#333333"
DARK = "#111111"
MID = "#666666"
LIGHT = "#dbd8e3"
FONT_NAME = "Courier"



class MainWindow(Frame):
    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.root = root
        self.root.config(padx=0, pady=20, bg=BACKGROUND, width = 900)

        self.logo_canvas = self.add_canvas(root, w=316, h=316, img="./images/logo.png")
        self.logo_canvas.grid(row=0, column=0, pady=(25, 50), padx=(50, 25))

        self.file_display = FilesDisplay(master=self.root)

        self.file_display.grid(column=1, row=0)


    def add_canvas(self, root, img, w, h):
        canvas = Canvas(root, width=w, height=h, bg=BACKGROUND, highlightthickness=0)
        canvas_img = PhotoImage(file=img)
        canvas.create_image(w / 2, h / 2, image=canvas_img)
        canvas.theimage = canvas_img
        return canvas


class FilesDisplay(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND, **kw)

        self.display_files()


    def display_files(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.photo_finance = PhotoImage(file = "./images/button_finance.png")
        self.button_finance = Button(self, borderwidth=0,
                                     image=self.photo_finance,
                                     bg = BACKGROUND, activebackground=BACKGROUND,
                                     command=lambda: AccountingWindow(root = self))
        self.button_finance.grid(row=0, column=0, pady=(10, 50), padx=15, sticky = 'we')

        self.photo_inv = PhotoImage(file = "./images/button_inventory.png")
        self.button_inv = Button(self, borderwidth=0,
                                     image=self.photo_inv,
                                     bg = BACKGROUND, activebackground=BACKGROUND,
                                     command=lambda: InventoryWindow(root = self))
        self.button_inv.grid(row=0, column=1, pady=(10, 50), padx=15, sticky = 'we')


        self.load_file_names()

        if hasattr(self, "add_button"):
            self.add_button.destroy()

        if len(self.files_in_dir) > 0:
            for file in self.files_in_dir:
                label_build = Label(self,text=file, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 18))
                label_build.grid(row=self.grid_size()[1], column=0,padx=(15, 5), pady=5, sticky = 'w')
                open_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_open_sleep.png",
                                       img_enter="./images/Button_open_hover.png")
                open_button.grid(row=self.grid_size()[1]-1, column=1, padx=(5,20))

                open_button.config(
                     bg=BACKGROUND,
                     highlightthickness=0,
                     activebackground=BACKGROUND,
                     command=lambda name=file : BuildEditor(
                         file_name=name, root = self))

                self.archive_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_archive_sleep.png",
                                              img_enter="./images/Button_archive_hover.png", bg=BACKGROUND,
                                              highlightthickness=0, activebackground=BACKGROUND)
                self.archive_button.config(
                    command=lambda file=file, button=self.archive_button: self.archive_row(file, button))
                self.archive_button.grid(row=self.grid_size()[1]-1, column=2, padx=(5,20))


                self.del_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_del_sleep.png",
                                              img_enter="./images/Button_del_hover.png", bg=BACKGROUND,
                                              highlightthickness=0, activebackground=BACKGROUND)
                self.del_button.config(
                    command=lambda file=file, button=self.del_button: self.delete_row(file, button))
                self.del_button.grid(row=self.grid_size()[1]-1, column=3, padx=(5,20))


        self.add_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_add_sleep.png",
                                     img_enter="./images/Button_add_hover.png")
        self.add_button.config(bg=BACKGROUND, highlightthickness=0, activebackground=BACKGROUND,
                               command=lambda: BuildEditor(file_name=None, root=self))
        self.add_button.grid(row=self.grid_size()[1] + len(self.files_in_dir), column=0, pady=15)

        self.grid_columnconfigure(0, minsize=300)


    def delete_row(self,file, button):
        build = pd.read_csv('./data/Build.csv')
        draft = pd.read_csv('./data/Draft.csv')

        new_build = build[build['Build'] != file]
        new_draft = draft[draft['Build'] != file]

        self.files_in_dir.remove(file)

        new_build.to_csv("./data/Build.csv", index=False)
        new_draft.to_csv("./data/Draft.csv", index=False)

        self.display_files()

    def add_canvas(self, root, img, w, h):
        canvas = Canvas(root, width=w, height=h, bg=BACKGROUND, highlightthickness=0)
        canvas_img = PhotoImage(file=img)
        canvas.create_image(w / 2, h / 2, image=canvas_img)
        canvas.theimage = canvas_img
        return canvas

    def load_file_names(self):
        try:
            self.data = pd.read_csv(".\data\Draft.csv")
            self.files_in_dir = list(self.data['Build'].unique())
        except FileNotFoundError:
            self.files_in_dir = []

    def archive_row(self,file, button):
        build = pd.read_csv('./data/Build.csv')
        draft = pd.read_csv('./data/Draft.csv')

        new_build = build[build['Build'] != file]
        new_draft = draft[draft['Build'] != file]
        new_build.to_csv("./data/Build.csv", index=False)
        new_draft.to_csv("./data/Draft.csv", index=False)

        arch_build = build[build['Build'] == file]
        arch_build['Date'] = datetime.datetime.today().strftime('%d-%m-%Y')
        arch_draft = draft[draft['Build'] == file]
        arch_draft['Date'] = datetime.datetime.today().strftime('%d-%m-%Y')

        try:
            draft_archive = pd.read_csv('./data/Archive_draft.csv')
        except FileNotFoundError:
            draft_archive = pd.DataFrame(columns=['Type', 'Name', 'Price', 'Build', 'Suggested_price','Date'])
        try:
            build_archive = pd.read_csv('./data/Archive_draft.csv')
        except FileNotFoundError:
            build_archive = pd.DataFrame(columns=['Type', 'Name',
                                                         'Price_bought', 'Price_sold',
                                                         'Build', 'Final_Price', 'Date'])

        new_draft_archive = draft_archive.append(arch_draft, ignore_index=True)
        new_build_archive = build_archive.append(arch_build, ignore_index=True)

        new_draft_archive.to_csv(f"./data/Archive_draft.csv", index=False)
        new_build_archive.to_csv(f"./data/Archive_build.csv", index=False)

        self.files_in_dir.remove(file)

        self.display_files()

