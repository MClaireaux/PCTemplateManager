from tkinter import *
import time
import datetime
import pandas as pd
from mystyle import HoverButton, MyLabel, add_canvas
from file_manager import FileManager

BACKGROUND = "#333333"
DARK = "#111111"
MID = "#666666"
LIGHT = "#dbd8e3"
FONT_NAME = "Courier"


class AccountingWindow:
    def __init__(self, root):
        self.z = Toplevel(root)
        self.z.geometry("600x600")
        self.z.title("Accounting")
        self.z.config(padx=50, pady=25, bg=BACKGROUND)

        try:
            self.inventory = pd.read_csv('./data/Inventory.csv', keep_default_na=False)
        except FileNotFoundError:
            self.inventory = pd.read_csv('./raw/Inventory.csv', keep_default_na=False)

        self.margin = MarginDetails(master=self.z, inventory=self.inventory)

        self.exposure = Exposure(master=self.z, inventory=self.inventory)

        self.sep_line = add_canvas(self.z, "./images/sep_line.png", 500, 10)

        self.exposure.grid(column=1, row=1, pady=10, columnspan=1, sticky='w')
        self.sep_line.grid(column=1, row=2, pady=10, columnspan=1)
        self.margin.grid(column=1, row=3, pady=10, columnspan=1, sticky='w')

        self.z.grid_columnconfigure(1, minsize=400)


class Exposure(Frame):
    def __init__(self, inventory, **kw):
        super().__init__(bg=BACKGROUND, **kw)

        self.nok_in = inventory["Paid Price"][inventory["Status"] == "In"].sum()
        self.nok_ordered = inventory["Paid Price"][inventory["Status"] == "Ordered"].sum()

        self.label_ordered = MyLabel(text=f"Amount ordered: ", master=self)
        self.label_amount_ordered = MyLabel(text=f"{self.nok_ordered} nok", font=(FONT_NAME, 15), master=self)

        self.label_in = MyLabel(text=f"Amount in inventory: ", master=self)
        self.label_amount_in = MyLabel(text=f"{self.nok_in} nok", font=(FONT_NAME, 15), master=self)

        self.label_exposure = MyLabel(text=f"Total exposure: ", master=self)
        self.label_amount_exposure = MyLabel(text=f"{self.nok_in + self.nok_ordered} nok", font=(FONT_NAME, 15),
                                             master=self)

        self.label_ordered.grid(column=1, row=1, sticky="w", columnspan=1)
        self.label_amount_ordered.grid(column=2, row=1, sticky="w", columnspan=1)

        self.label_in.grid(column=1, row=2, sticky="w", columnspan=1)
        self.label_amount_in.grid(column=2, row=2, sticky="w", columnspan=1)

        self.label_exposure.grid(column=1, row=3, sticky="w", columnspan=1)
        self.label_amount_exposure.grid(column=2, row=3, sticky="w", columnspan=1)

        self.grid_columnconfigure(1, minsize=270)


class MarginDetails(Frame):
    def __init__(self, inventory, **kw):
        super().__init__(bg=BACKGROUND, **kw)

        self.nok_sold = inventory["Selling price"][inventory["Status"] == "Sold"].sum()
        self.margin = self.nok_sold - inventory["Paid Price"][inventory["Status"] == "Sold"].sum()
        self.details = []

        self.label_sold = MyLabel(text=f"Amount sold: ", master=self)
        self.label_amount_sold = MyLabel(text=f"{self.nok_sold} nok", master=self, font=(FONT_NAME, 15))

        self.label_margin = MyLabel(text=f"Margin: ", master=self)
        self.label_amount_margin = MyLabel(text=f"{self.margin} nok", master=self, font=(FONT_NAME, 15))

        self.button_down = HoverButton(self, borderwidth=0, img_leave="./images/Button_down_sleep.png",
                                       img_enter="./images/Button_down_hover.png", bg=BACKGROUND,
                                       activebackground=BACKGROUND,
                                       command=lambda: self.get_margin_details(inventory))

        self.label_sold.grid(column=1, row=1, sticky="w", columnspan=1)
        self.label_amount_sold.grid(column=2, row=1, sticky="w", columnspan=1)

        self.label_margin.grid(column=1, row=2, sticky="w", columnspan=1, pady=(2, 15))
        self.label_amount_margin.grid(column=2, row=2, sticky="w", columnspan=1, pady=(2, 15))
        self.button_down.grid(column=3, row=2, sticky="w", columnspan=1, padx=10, pady=(2, 15))

        self.grid_columnconfigure(1, minsize=270)

    def get_margin_details(self, inventory):
        build_list = [x for x in list(inventory["PC build"].unique()) if str(x) != 'nan']
        row_nb = 3

        for build in build_list:
            build_tab = inventory[inventory["PC build"] == build]
            build_margin = build_tab["Selling price"].sum() - build_tab["Paid Price"].sum()

            self.label_build = MyLabel(text=f"{build}: ", master=self)
            self.label_build_margin = MyLabel(text=f"{build_margin} nok", master=self, font=(FONT_NAME, 15))
            self.label_build.grid(column=1, row=row_nb, sticky="w", columnspan=1, padx=20)
            self.label_build_margin.grid(column=2, row=row_nb, sticky="w", columnspan=2, padx=25)
            self.details.append({
                'name': self.label_build,
                'margin': self.label_build_margin
            })
            row_nb += 1

        self.button_down.destroy()

        self.button_up = HoverButton(self, borderwidth=0, img_leave="./images/Button_up_sleep.png",
                                     img_enter="./images/Button_up_hover.png", bg=BACKGROUND,
                                     activebackground=BACKGROUND,
                                     command=lambda: self.hide_margin(inventory))

        self.button_up.grid(column=3, row=2, sticky="w", columnspan=1, padx=10)

    def hide_margin(self, inventory):
        for build in self.details:
            build['name'].destroy()
            build['margin'].destroy()

        self.button_up.destroy()
        self.button_down = HoverButton(self, borderwidth=0, img_leave="./images/Button_down_sleep.png",
                                       img_enter="./images/Button_down_hover.png", bg=BACKGROUND,
                                       activebackground=BACKGROUND,
                                       command=lambda: self.get_margin_details(inventory))
        self.button_down.grid(column=3, row=2, sticky="w", columnspan=1, padx=10)
