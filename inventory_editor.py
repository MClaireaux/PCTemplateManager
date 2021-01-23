from tkinter import *
import time
import datetime
import pandas as pd
from mystyle import HoverButton, MyLabel, add_canvas
from file_manager import FileManager
from tkinter import ttk
from tkinter import messagebox

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
        self.z.geometry("900x800")
        self.z.title("Inventory editor")
        self.z.config(padx=50, pady=25, bg=BACKGROUND)

        try:
            self.z.inventory = pd.read_csv('./data/Inventory.csv', keep_default_na=False)
        except FileNotFoundError:
            self.z.inventory = pd.read_csv('./raw/Inventory.csv', keep_default_na=False)

        self.z.first_panel = HeadPanel(master = self.z)
        self.z.first_panel.grid(column = 0, row = 0,columnspan = 2)

        self.z.first_sep_line = add_canvas(self.z, "./images/sep_line.png", 500, 10)
        self.z.first_sep_line.grid(column = 0, row = 1, pady=LARGESPACE,columnspan = 2)

        self.z.second_panel = OrderedPanel(master = self.z)
        self.z.second_panel.grid(column = 0, row = 2,columnspan = 2)

        self.z.second_sep_line = add_canvas(self.z, "./images/sep_line.png", 500, 10)
        self.z.second_sep_line.grid(column = 0, row = 3, pady=LARGESPACE,columnspan = 2)

        self.z.third_panel = SoldPanel(master = self.z)
        self.z.third_panel.grid(column = 0, row = 4,columnspan = 2)

        self.z.third_sep_line = add_canvas(self.z, "./images/sep_line.png", 500, 10)
        self.z.third_sep_line.grid(column=0, row=5, pady=LARGESPACE,columnspan = 2)

        self.z.note_label = MyLabel("Notes:", master=self.z, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='e')
        self.z.note_entry = Entry(self.z, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15))
        self.z.note_label.grid(column = 0, row = 6, sticky = 'e', padx=SMALLSPACE, pady=LARGESPACE)
        self.z.note_entry.grid(column = 1, row = 6, sticky = 'we', padx=SMALLSPACE, pady=LARGESPACE)

        self.z.save_button = HoverButton(self.z, borderwidth=0, img_leave="./images/Button_save_sleep.png",
                                       img_enter="./images/Button_save_hover.png", bg=BACKGROUND,
                                       highlightthickness=0, activebackground=BACKGROUND)
        self.z.save_button.config(command= self.save_piece)
        self.z.save_button.grid(column = 0, row = 7, sticky = 'e', pady=LARGESPACE)

        self.z.update_button = HoverButton(self.z, borderwidth=0, img_leave="./images/Button_update_sleep.png",
                                       img_enter="./images/Button_update_hover.png", bg=BACKGROUND,
                                       highlightthickness=0, activebackground=BACKGROUND)
        self.z.update_button.config(command= self.update_piece)
        self.z.update_button.grid(column = 1, row = 7, sticky = 'e', pady=LARGESPACE)


    def save_piece(self):

        new_row = {}
        for col in list(self.z.inventory.columns):
            new_row[col]=""

        new_row['ID'] = len(self.z.inventory)+1

        if self.z.first_panel.name_entry.get() == "":
            messagebox.showinfo(title='Oops', message="You have to enter the piece name")
        elif self.z.second_panel.v.get() == "":
            messagebox.showinfo(title="Oops", message="Select a Ny/Brukt state")
        elif self.z.second_panel.v.get() == "":
            messagebox.showinfo(title="Oops", message="Select a paid/unpaid option")
        elif self.z.first_panel.status_combobox.get() == "":
            messagebox.showinfo(title="Oops", message="You have to enter the status of the piece")
        elif self.z.second_panel.d_ordered_entry.get() == "":
            messagebox.showinfo(title="Oops", message="Enter a date ordered")
        elif self.z.first_panel.origin_combobox.get() == "":
            messagebox.showinfo(title="Oops", message="Enter the origin of the piece")
        elif self.z.first_panel.type_combobox.get() == "":
            messagebox.showinfo(title="Oops", message="Choose a type for the piece")
        elif self.z.second_panel.paid_price_entry.get() == "":
            messagebox.showinfo(title="Oops", message="Enter the price paid")
        else:
            new_row['Name'] = self.z.first_panel.name_entry.get()
            new_row['Type'] = self.z.first_panel.type_combobox.get()
            new_row['State'] = self.z.second_panel.v.get()
            new_row['Origin'] = self.z.first_panel.origin_combobox.get()
            new_row['Retail Price'] = self.z.second_panel.retail_price_entry.get()
            new_row['Paid Price'] = self.z.second_panel.paid_price_entry.get()

            if self.z.second_panel.d_ordered_entry.get() == 'dd.mm.yyyy':
                new_row['Date ordered'] = ""
            else:
                new_row['Date ordered'] = self.z.second_panel.d_ordered_entry.get()

            new_row['Order number'] = self.z.first_panel.ordernb_entry.get()
            new_row['Date received'] = self.z.second_panel.d_received_entry.get()
            new_row['Date paid'] = self.z.second_panel.date_paid_entry.get()
            new_row['Returnable'] = ""
            new_row['Status'] = self.z.first_panel.status_combobox.get()
            new_row['Paid'] = self.z.second_panel.pay_var.get()
            new_row['Paymethod'] = self.z.second_panel.payment_combobox.get()
            new_row['Selling price'] = self.z.third_panel.price_sold_entry.get()
            new_row['Date sold'] = self.z.third_panel.d_sold_entry.get()
            new_row['PC build'] = self.z.third_panel.build_name_entry.get()
            new_row['Note'] = self.z.note_entry.get()

            self.z.inventory = self.z.inventory.append(new_row, ignore_index = True)
            self.z.inventory.to_csv("./data/Inventory.csv", index=False)
            messagebox.showinfo(title="Success", message="Your piece has been saved successfully!")

    def update_piece(self):

        if self.z.first_panel.name_ID in self.z.inventory['ID']:
            ID = self.z.first_panel.name_ID
            row_to_update = self.z.inventory[self.z.inventory['ID']==ID]

            if self.z.first_panel.name_entry.get() == "":
                messagebox.showinfo(title='Oops', message="You have to enter the piece name")
            elif self.z.second_panel.v.get() == "":
                messagebox.showinfo(title="Oops", message="Select a Ny/Brukt state")
            elif self.z.second_panel.v.get() == "":
                messagebox.showinfo(title="Oops", message="Select a paid/unpaid option")
            elif self.z.first_panel.status_combobox.get() == "":
                messagebox.showinfo(title="Oops", message="You have to enter the status of the piece")
            elif self.z.second_panel.d_ordered_entry.get() == "":
                messagebox.showinfo(title="Oops", message="Enter a date ordered")
            elif self.z.first_panel.origin_combobox.get() == "":
                messagebox.showinfo(title="Oops", message="Enter the origin of the piece")
            elif self.z.first_panel.type_combobox.get() == "":
                messagebox.showinfo(title="Oops", message="Choose a type for the piece")
            elif self.z.second_panel.paid_price_entry.get() == "":
                messagebox.showinfo(title="Oops", message="Enter the price paid")
            else:
                row_to_update['Name'] = self.z.first_panel.name_entry.get()
                row_to_update['Type'] = self.z.first_panel.type_combobox.get()
                row_to_update['State'] = self.z.second_panel.v.get()
                row_to_update['Origin'] = self.z.first_panel.origin_combobox.get()
                row_to_update['Retail Price'] = self.z.second_panel.retail_price_entry.get()
                row_to_update['Paid Price'] = self.z.second_panel.paid_price_entry.get()
                row_to_update['Date ordered'] = self.z.second_panel.d_ordered_entry.get()
                row_to_update['Order number'] = self.z.first_panel.ordernb_entry.get()
                row_to_update['Date received'] = self.z.second_panel.d_received_entry.get()
                row_to_update['Date paid'] = self.z.second_panel.date_paid_entry.get()
                row_to_update['Returnable'] = ""
                row_to_update['Status'] = self.z.first_panel.status_combobox.get()
                row_to_update['Paid'] = self.z.second_panel.pay_var.get()
                row_to_update['Paymethod'] = self.z.second_panel.payment_combobox.get()
                row_to_update['Selling price'] = self.z.third_panel.price_sold_entry.get()
                row_to_update['Date sold'] = self.z.third_panel.d_sold_entry.get()
                row_to_update['PC build'] = self.z.third_panel.build_name_entry.get()
                row_to_update['Note'] = self.z.note_entry.get()

            self.z.inventory[self.z.inventory['ID'] == ID] = row_to_update

            print(ID)
            print(self.z.inventory[self.z.inventory['ID'] == ID])
            print(row_to_update)
            print(self.z.inventory)

            self.z.inventory.to_csv("./data/Inventory.csv", index=False)
            messagebox.showinfo(title="Success", message="Your piece has been updated successfully!")

class HeadPanel(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND,**kw)

        self.origin_list = ["Komplett", "NetOnNet", "ProShop", "Multicom", "Dustin Home", "Elkjøp"]

        self.name_label = MyLabel("Name:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.name_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH*2)
        self.name_label.grid(column = 0, row = 0, sticky = 'w', padx=SMALLSPACE, pady=LARGESPACE)
        self.name_entry.grid(column = 1, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE, columnspan = 2)

        self.find_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_find_sleep.png",
                                          img_enter="./images/Button_find_hover.png", bg=BACKGROUND,
                                          highlightthickness=0, activebackground=BACKGROUND)
        self.find_button.config( command= self.search_piece)
        self.find_button.grid(row= 0, column=3, pady=LARGESPACE)

        self.type_var = StringVar()
        self.type_label = MyLabel("Type:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.type_combobox = ttk.Combobox(self, values=list(self.master.inventory['Type'].unique()))
        self.type_combobox.config(width = MENU_WIDTH, textvariable = self.type_var)
        self.option_add('*TCombobox*Listbox.font', (FONT_NAME))
        self.type_label.grid(column = 0, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.type_combobox.grid(column = 1, row = 1, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.status_var= StringVar()
        self.status_label = MyLabel("Status:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.status_combobox = ttk.Combobox(self, values=list(self.master.inventory['Status'].unique()))
        self.status_combobox.config(width = MENU_WIDTH, textvariable = self.status_var)
        self.status_label.grid(column = 0, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.status_combobox.grid(column = 1, row = 2, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.origin_var= StringVar()
        self.origin_label = MyLabel("Origin:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.origin_combobox = ttk.Combobox(self, values=self.origin_list, textvariable = self.origin_var)
        self.origin_combobox.config(width = MENU_WIDTH)
        self.origin_label.grid(column = 2, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.origin_combobox.grid(column = 3, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)


        self.ordernb_label = MyLabel("Order number:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.ordernb_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.ordernb_label.grid(column = 2, row = 2, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.ordernb_entry.grid(column = 3, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

    def search_piece(self):

        piece_carac = {}
        piece_carac['Name'] = {'wid': self.name_entry, 'value': self.name_entry.get().lower()}
        piece_carac['Type'] = {'wid': self.type_var, 'value': self.type_var.get().lower()}
        piece_carac['Status'] = {'wid': self.status_var, 'value': self.status_var.get().lower()}
        piece_carac['Origin'] = {'wid': self.origin_var, 'value': self.origin_var.get().lower()}
        piece_carac['Order number'] = {'wid': self.ordernb_entry, 'value': str(self.ordernb_entry.get().lower())}

        piece_to_find = {key: val for key, val in piece_carac.items() if piece_carac[key]['value'] != ""}

        self.get_dat = self.master.inventory.copy()

        for key in piece_to_find:
            get_type = key
            get_value = piece_to_find[key]['value']
            self.get_dat = self.get_dat[self.get_dat[get_type].str.lower().str.contains(get_value, regex=False)]

        self.get_dat['ID'] = self.get_dat['ID'].astype(float)
        self.get_dat['ID'] = self.get_dat['ID'].astype(str)
        self.get_dat['Name'] = self.get_dat['Name'].astype(str).str.replace('  ', '')

        for index, values in self.get_dat["ID"].items():
            self.get_dat["ID"].loc[[index]] = values.replace('.0', ' - ')

        self.get_dat["IDName"] = ""
        self.get_dat["IDName"]= self.get_dat['ID'] + self.get_dat['Name']

        NameList(self)


class OrderedPanel(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND,**kw)

        self.d_ordered_label = MyLabel("Date ordered:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.d_ordered_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.d_ordered_entry.insert(0,"dd.mm.yyyy")
        self.d_ordered_label.grid(column = 0, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.d_ordered_entry.grid(column = 1, row = 0, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.d_received_label = MyLabel("Date received:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.d_received_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.d_received_entry.insert(0,"dd.mm.yyyy")
        self.d_received_label.grid(column = 2, row = 0, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.d_received_entry.grid(column = 3, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.retail_price_label = MyLabel("Retail price:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.retail_price_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.retail_price_label.grid(column = 0, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.retail_price_entry.grid(column = 1, row = 1, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.paid_price_label = MyLabel("Paid price:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.paid_price_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.paid_price_label.grid(column = 2, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.paid_price_entry.grid(column = 3, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.payment_var= StringVar()
        self.payment_label = MyLabel("Payment:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.payment_combobox = ttk.Combobox(self, values=list(self.master.inventory['Paymethod'].unique()))
        self.payment_combobox.config(width = MENU_WIDTH)
        self.payment_label.grid(column = 0, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)
        self.payment_combobox.grid(column = 1, row = 2, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.pay_var = StringVar()
        self.pay_radio = Radiobutton(self, text="Paid", padx=2, variable=self.pay_var, value="Paid")
        self.pay_radio.config(bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), activebackground=BACKGROUND,
                             activeforeground=LIGHT, selectcolor= DARK)
        self.unpay_radio = Radiobutton(self, text="Not paid", padx=2, variable=self.pay_var, value="Not paid")
        self.unpay_radio.config(bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), activebackground=BACKGROUND,
                                activeforeground=LIGHT, selectcolor= DARK)

        self.pay_radio.grid(column = 1, row = 3, sticky = 'w', padx=(SMALLSPACE, SMALLSPACE), pady=SMALLSPACE)
        self.unpay_radio.grid(column = 1, row = 3, sticky = 'e', padx=SMALLSPACE, pady=SMALLSPACE)

        self.date_paid_label = MyLabel("Date paid:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.date_paid_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.date_paid_entry.insert(0,"dd.mm.yyyy")
        self.date_paid_label.grid(column = 2, row = 2, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.date_paid_entry.grid(column = 3, row = 2, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.v = StringVar()
        self.ny_radio = Radiobutton(self, text="Ny", padx=2, variable=self.v, value="Ny")
        self.ny_radio.config(bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), activebackground=BACKGROUND,
                             activeforeground=LIGHT, selectcolor= DARK)
        self.brukt_radio = Radiobutton(self, text="Brukt", padx=2, variable=self.v, value="Brukt")
        self.brukt_radio.config(bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), activebackground=BACKGROUND,
                                activeforeground=LIGHT, selectcolor= DARK)

        self.ny_radio.grid(column = 3, row = 3, sticky = 'w', padx=(SMALLSPACE, SMALLSPACE), pady=SMALLSPACE)
        self.brukt_radio.grid(column = 3, row = 3, sticky = 'e', padx=SMALLSPACE, pady=SMALLSPACE)

        self.date_paid_entry.bind("<Button-1>", self.removeValue)
        self.d_ordered_entry.bind("<Button-1>", self.removeValue)
        self.d_received_entry.bind("<Button-1>", self.removeValue)

    def removeValue(self, event):
        event.widget.delete(0, 'end')
        event.widget.config(fg=LIGHT)

class SoldPanel(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND,**kw)

        self.build_name_label = MyLabel("Build name:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.build_name_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.build_name_label.grid(column = 0, row = 0, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.build_name_entry.grid(column = 1, row = 0, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.d_sold_label = MyLabel("Date sold:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.d_sold_entry = Entry(self, bg=BACKGROUND, fg=MID, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.d_sold_entry.insert(0,"dd.mm.yyyy")
        self.d_sold_label.grid(column = 0, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.d_sold_entry.grid(column = 1, row = 1, sticky = 'w', padx=(SMALLSPACE, LARGESPACE), pady=SMALLSPACE)

        self.price_sold_label = MyLabel("Price sold:", master=self, font=(FONT_NAME, 15), width=LABEL_WIDTH, anchor='w')
        self.price_sold_entry = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width = ENTRY_WIDTH)
        self.price_sold_label.grid(column = 2, row = 1, sticky = 'w', padx=(LARGESPACE, SMALLSPACE), pady=SMALLSPACE)
        self.price_sold_entry.grid(column = 3, row = 1, sticky = 'w', padx=SMALLSPACE, pady=SMALLSPACE)

        self.d_sold_entry.bind("<Button-1>", self.removeValue)

    def removeValue(self, event):
        event.widget.delete(0, 'end')
        event.widget.config(fg=LIGHT)

class NameList:
    def __init__(self, root):
        self.z = Toplevel(root)
        self.z.geometry("1000x400")
        self.z.title("Inventory editor")
        self.z.config(padx=50, pady=25, bg=BACKGROUND)

        self.name_list = Listbox(self.z,  font=(FONT_NAME, 15), bg=BACKGROUND, fg=LIGHT, width = 75)

        for i in range(0, len(root.get_dat)):
            self.name_list.insert(i+1, list(root.get_dat["IDName"])[i])

        self.name_list.grid(column=0,row=0, sticky = "we")
        self.name_list.bind("<<ListboxSelect>>", self.select_name)

    def select_name(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            piece_name = event.widget.get(index)
            dash_index = piece_name.find('-')-1
            self.z.master.name_ID = int(piece_name[:dash_index])

            inv_row = self.z.master.master.inventory[self.z.master.master.inventory["ID"]==self.z.master.name_ID]

            self.z.master.name_entry.delete(0, END)
            self.z.master.name_entry.insert(0, inv_row['Name'].values[0])
            self.z.master.type_var.set(inv_row['Type'].values[0])

            if inv_row['State'].values[0].strip(" ") == "Ny" or inv_row['State'].values[0].strip(" ") == "Brukt":
                self.z.master.master.second_panel.v.set(inv_row['State'].values[0].strip(" "))
            else:
                self.z.master.master.second_panel.v.set(None)

            self.z.master.origin_var.set(inv_row['Origin'].values[0])
            self.z.master.master.second_panel.retail_price_entry.delete(0, END)
            self.z.master.master.second_panel.retail_price_entry.insert(0, inv_row['Retail Price'].values[0])
            self.z.master.master.second_panel.paid_price_entry.delete(0, END)
            self.z.master.master.second_panel.paid_price_entry.insert(0, inv_row['Paid Price'].values[0])

            self.z.master.master.second_panel.d_ordered_entry.config(fg = LIGHT)
            self.z.master.master.second_panel.d_ordered_entry.delete(0, END)
            self.z.master.master.second_panel.d_ordered_entry.insert(0, inv_row['Date ordered'].values[0])

            self.z.master.ordernb_entry.delete(0, END)
            self.z.master.ordernb_entry.insert(0, inv_row['Order number'].values[0])

            self.z.master.master.second_panel.d_received_entry.config(fg = LIGHT)
            self.z.master.master.second_panel.d_received_entry.delete(0, END)
            self.z.master.master.second_panel.d_received_entry.insert(0, inv_row['Date received'].values[0])

            self.z.master.master.second_panel.date_paid_entry.config(fg = LIGHT)
            self.z.master.master.second_panel.date_paid_entry.delete(0, END)
            self.z.master.master.second_panel.date_paid_entry.insert(0, inv_row['Date paid'].values[0])

            self.z.master.status_var.set(inv_row['Status'].values[0])

            if inv_row['Paid'].values[0].strip(" ") == "Paid" or inv_row['Paid'].values[0].strip(" ") == "Not paid":
                self.z.master.master.second_panel.pay_var.set(inv_row['Paid'].values[0].strip(" "))
            else:
                self.z.master.master.second_panel.pay_var.set(None)

            self.z.master.master.second_panel.payment_var.set(inv_row['Paymethod'].values[0])

            self.z.master.master.third_panel.price_sold_entry.delete(0, END)
            self.z.master.master.third_panel.price_sold_entry.insert(0, inv_row['Selling price'].values[0])

            self.z.master.master.third_panel.d_sold_entry.config(fg = LIGHT)
            self.z.master.master.third_panel.d_sold_entry.delete(0, END)
            self.z.master.master.third_panel.d_sold_entry.insert(0, inv_row['Date sold'].values[0])

            self.z.master.master.third_panel.build_name_entry.delete(0, END)
            self.z.master.master.third_panel.build_name_entry.insert(0, inv_row['PC build'].values[0])

            self.z.master.master.note_entry.delete(0, END)
            self.z.master.master.note_entry.insert(0, inv_row['Note'].values[0])

