from tkinter import *
import time
import datetime
import pandas as pd
from mystyle import HoverButton, MyLabel, add_canvas
from file_manager import FileManager
from tkinter import ttk

BACKGROUND = "#333333"
DARK = "#111111"
MID = "#666666"
LIGHT = "#dbd8e3"
FONT_NAME = "Courier"

SMALLSPACE = 5
LARGESPACE = 20
MENU_WIDTH = 27
ENTRY_WIDTH = 15
LABEL_WIDTH = 13

class InventoryWindow:
    def __init__(self, root):
        self.z = Toplevel(root)
        self.z.geometry("1000x600")
        self.z.title("Inventory editor")
        self.z.config(padx=50, pady=25, bg=BACKGROUND)

        self.inventory = pd.read_csv('./raw/Inventory.csv')

        self.first_panel = HeadPanel(master = self.z)
        self.first_panel.grid(column = 0, row = 0)

        self.first_sep_line = add_canvas(self.z, "./images/sep_line.png", 500, 10)
        self.first_sep_line.grid(column = 0, row = 1, pady=LARGESPACE)

        self.second_panel = OrderedPanel(master = self.z)
        self.second_panel.grid(column = 0, row = 2)

        self.second_sep_line = add_canvas(self.z, "./images/sep_line.png", 500, 10)
        self.second_sep_line.grid(column = 0, row = 3, pady=LARGESPACE)

        self.third_panel = SoldPanel(master = self.z)
        self.third_panel.grid(column = 0, row = 4)

        self.save_button = HoverButton(self.z, borderwidth=0, img_leave="./images/Button_save_sleep.png",
                                       img_enter="./images/Button_save_hover.png", bg=BACKGROUND,
                                       highlightthickness=0, activebackground=BACKGROUND)
        self.save_button.config(command=self.save_piece)
        self.save_button.grid(column = 0, row = 5, sticky = 'e', pady=LARGESPACE)

    def save_piece(self):
        id = len(self.inventory)+1
        name = self.first_panel.name_entry.get()
        type = self.first_panel.type_combobox. get()
     #   status =



class HeadPanel(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND,**kw)

        self.name_label = MyLabel("Name:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.name_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.name_label.grid(column = 0, row = 0, sticky = 'w', padx=SMALLSPACE, pady=LARGESPACE)
        self.name_entry.grid(column = 1, row = 0, sticky = 'w', padx=SMALLSPACE, pady=LARGESPACE)

        self.find_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_find_sleep.png",
                                          img_enter="./images/Button_find_hover.png", bg=BACKGROUND,
                                          highlightthickness=0, activebackground=BACKGROUND)
        #self.find_button.config( command= )
        self.find_button.grid(row= 0, column=3, pady=LARGESPACE)

        self.type_label = MyLabel("Type:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.type_combobox = ttk.Combobox(self, values=[""], width = MENU_WIDTH)
        self.type_label.grid(column = 0, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.type_combobox.grid(column = 1, row = 1, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.status_label = MyLabel("Status:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.status_combobox = ttk.Combobox(self, values=[""], width = MENU_WIDTH)
        self.status_label.grid(column = 0, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.status_combobox.grid(column = 1, row = 2, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.origin_label = MyLabel("Origin:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.origin_combobox = ttk.Combobox(self, values=[""], width = MENU_WIDTH)
        self.origin_label.grid(column = 2, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.origin_combobox.grid(column = 3, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.ordernb_label = MyLabel("Order number:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.ordernb_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.ordernb_label.grid(column = 2, row = 2, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.ordernb_entry.grid(column = 3, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)



class OrderedPanel(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND,**kw)

        self.d_ordered_label = MyLabel("Date ordered:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.d_ordered_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.d_ordered_entry.insert(0,"dd.mm.yyy")
        self.d_ordered_label.grid(column = 0, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.d_ordered_entry.grid(column = 1, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.v = IntVar()
        self.ny_radio = Radiobutton(self, text="Ny", padx=2, variable=self.v, value=1)
        self.ny_radio.config(bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), activebackground=BACKGROUND,
                             activeforeground=LIGHT, selectcolor= DARK)
        self.brukt_radio = Radiobutton(self, text="Brukt", padx=2, variable=self.v, value=2)
        self.brukt_radio.config(bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), activebackground=BACKGROUND,
                                activeforeground=LIGHT, selectcolor= DARK)

        self.ny_radio.grid(column = 2, row = 0, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.brukt_radio.grid(column = 2, row = 0, sticky = 'e', padx=SMALLSPACE, pady=SMALLSPACE)

        self.retail_price_label = MyLabel("Retail price:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.retail_price_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.retail_price_label.grid(column = 0, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.retail_price_entry.grid(column = 1, row = 1, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.paid_price_label = MyLabel("Paid price:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.paid_price_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.paid_price_label.grid(column = 2, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.paid_price_entry.grid(column = 3, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.payment_label = MyLabel("Payment:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.payment_combobox = ttk.Combobox(self, values=[""], width = MENU_WIDTH)
        self.payment_label.grid(column = 0, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.payment_combobox.grid(column = 1, row = 2, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.date_paid_label = MyLabel("Date paid:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.date_paid_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.date_paid_entry.insert(0,"dd.mm.yyy")
        self.date_paid_label.grid(column = 2, row = 2, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.date_paid_entry.grid(column = 3, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

class SoldPanel(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND,**kw)

        self.build_name_label = MyLabel("Build name:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.build_name_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.build_name_label.grid(column = 0, row = 0, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.build_name_entry.grid(column = 1, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.d_sold_label = MyLabel("Date ordered:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.d_sold_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.d_sold_entry.insert(0,"dd.mm.yyy")
        self.d_sold_label.grid(column = 0, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.d_sold_entry.grid(column = 1, row = 1, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.price_sold_label = MyLabel("Build name:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.price_sold_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.price_sold_label.grid(column = 2, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.price_sold_entry.grid(column = 3, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
