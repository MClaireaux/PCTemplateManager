from tkinter import *
from mystyle import HoverButton, MyLabel, add_canvas
import pandas as pd
from tkinter import messagebox
from file_manager import FileManager
import math

BACKGROUND = "#333333"
DARK = "#111111"
MID = "#666666"
LIGHT = "#dbd8e3"
FONT_NAME = "Courier"


class BuildEditor:
    def __init__(self, root, file_name):
        self.root = Toplevel(root)
        self.root.geometry("2200x1200")
        self.root.title("Build editor")
        self.root.config(padx=50, pady=25, bg=BACKGROUND)

        self.root.file_name = file_name
        self.root.inventory = FileManager()

        try:
            self.root.build_file = pd.read_csv(f'.\data\Build.csv', keep_default_na=False)
            self.root.draft_file = pd.read_csv(f'.\data\Draft.csv', keep_default_na=False)
        except FileNotFoundError:
            self.root.draft_file = pd.DataFrame(columns=['Type', 'Name', 'Price', 'Build', 'Suggested_price'])
            self.root.build_file = pd.DataFrame(columns=['Type', 'Name',
                                                         'Price_bought', 'Price_sold',
                                                         'Build', 'Final_Price'])

        self.root.draft = Draft(master=self.root)
        self.root.draft.grid(column=0, row=2, padx=(80, 40), pady=(10, 5), sticky='nswe')
        self.root.build = Build(master=self.root)
        self.root.build.grid(column=1, row=2, padx=(10, 20), pady=(10, 5), sticky='nswe')
        self.root.header = Header(master=self.root)
        self.root.header.grid(column=0, row=1, padx=(40, 20), pady=(20, 20), columnspan=3, sticky='W')

        self.root.grid_columnconfigure((0, 1, 2), weight=1)


class Header(Frame):
    def __init__(self, **kw):
        super().__init__(bg=BACKGROUND, **kw)

        self.label_name = MyLabel("Name: ", master=self)
        self.entry_name = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=25)

        if self.master.file_name is not None:
            self.entry_name.insert(0, self.master.file_name)

        self.save_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_save_sleep.png",
                                       img_enter="./images/Button_save_hover.png", bg=BACKGROUND,
                                       highlightthickness=0, activebackground=BACKGROUND)
        self.save_button.config(command=self.save_new_build)

        self.label_name.grid(column=0, row=0, pady=(5, 15), padx=(50, 1), sticky='we')
        self.entry_name.grid(column=1, row=0, pady=(5, 15), padx=(1, 10), sticky='we')
        self.save_button.grid(column=2, row=0, pady=(5, 15), padx=(5, 0), sticky='wn')

        self.grid_columnconfigure(2, minsize=100)

    def save_new_build(self):

        if len(self.master.draft_file['Build']) < 0:
            build_list = []
        else:
            build_list = list(self.master.draft_file['Build'].unique())

        if self.entry_name.get() == 0:
            messagebox.showinfo(title="Oops", message="Please, enter a name for your file")
        elif self.entry_name.get() in build_list and self.entry_name.get() != self.master.file_name:
            messagebox.showinfo(title="Oops", message="This name is already taken")
        else:
            if self.entry_name.get() == self.master.file_name:
                self.master.draft_file = self.master.draft_file[
                    self.master.draft_file['Build'] != self.master.file_name
                ]
                self.master.build_file = self.master.build_file[
                    self.master.build_file['Build'] != self.master.file_name
                ]

            for key in self.master.draft.draft_entries:
                self.master.draft_file = self.master.draft_file.append({
                                                'Type': self.master.draft.draft_entries[key]["Type"],
                                                'Name': self.master.draft.draft_entries[key]["Name"].get(),
                                                'Price': self.master.draft.draft_entries[key]["Price"].get(),
                                                'Build': self.entry_name.get(),
                                                'Suggested_price': self.master.draft.entry_suggested_price.get(),
                                                }, ignore_index=True)

            for row in self.master.build.optionlist:
                self.master.build_file = self.master.build_file.append({
                                                'Type': row.variable_type.get(),
                                                'Name': row.variable_name.get(),
                                                'Price_bought': row.bought_price.get(),
                                                'Price_sold': row.sold_price.get(),
                                                'Build': self.entry_name.get(),
                                                'Final_Price': self.master.build.entry_final_price.get()
                                                }, ignore_index=True)


            self.master.draft_file.to_csv(f"./data/Draft.csv", index=False)
            self.master.build_file.to_csv(f"./data/Build.csv", index=False)

            messagebox.showinfo(title="Success", message="Your file has been saved successfully")

        self.master.master.load_file_names()
        self.master.master.display_files()


class Draft(Frame):
    def __init__(self, **kw):
        super().__init__(**kw, bg=BACKGROUND)

        self.file = self.master.draft_file[self.master.draft_file['Build'] == self.master.file_name]

        self.piece_list = ["GPU", "CPU", "CPU fan", "Motherboard", "RAM", "SSD", "HDD",
                           "PSU", "Case", "WiFi Card", "SATA kabler"]
        self.option_piece_list = ["Keyboard +\nMouse", "Mouse mat", "Cooler +", "GPU +", "m.2SSD",
                                  "RGB", "Fans", "Bluetooth"]
        self.draft_entries = {}
        self.price_entry_list = []

        self.header = add_canvas(self, "./images/logo_draft.png", 500, 64)
        self.header.grid(column=1, row=0, padx=5, pady=(0, 20), columnspan=3)
        self.sep_line = add_canvas(self, "./images/sep_line.png", 500, 10)
        self.name_label = MyLabel("Name", master=self)
        self.price_label = MyLabel("Price", master=self)
        self.name_label.grid(column=2, row=1, padx=5, pady=(5, 20))
        self.price_label.grid(column=3, row=1, padx=5, pady=(5, 20))

        self.display_entries(self, self.piece_list)

        self.sep_line.grid(column=1, row=self.grid_size()[1], pady=(15, 10), padx=5, columnspan=3)

        self.display_entries(self, self.option_piece_list)

        self.label_calculated_price = MyLabel("Total price:", master=self, font=(FONT_NAME, 15))
        self.entry_calculated_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15))
        self.label_calculated_price.grid(column=2, row=self.grid_size()[1], pady=(30, 5), padx=5, sticky="E")
        self.entry_calculated_price.grid(column=3, row=self.grid_size()[1] - 1, pady=(30, 5), padx=5)

        self.label_suggested_price = MyLabel("Suggested price:", master=self, font=(FONT_NAME, 15))
        self.entry_suggested_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15))
        self.label_suggested_price.grid(column=2, row=self.grid_size()[1], pady=5, padx=5, sticky="E")
        self.entry_suggested_price.grid(column=3, row=self.grid_size()[1] - 1, pady=5, padx=5)

        if len(self.file) > 0:
            sugg_price_text = str(self.file["Suggested_price"].unique()[0])
            self.entry_suggested_price.insert(0, sugg_price_text)


        self.update_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_update_sleep.png",
                                         img_enter="./images/Button_update_hover.png", bg=BACKGROUND,
                                         highlightthickness=0, activebackground=BACKGROUND)
        self.update_button.config(command=self.update_price)
        self.update_button.grid(column=1, row=self.grid_size()[1] - 2, pady=(5, 5), sticky="e")

    def display_entries(self, root, piece_list):
        for piece in piece_list:
            row_nb = root.grid_size()[1]
            new_label = MyLabel(piece, master=root)
            new_name_entry = Entry(root, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=20)
            new_price_entry = Entry(root, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=10)

            if len(self.file) > 0:
                new_name_text = self.file["Name"][self.file['Type'] == piece].values[0]
                new_price_text = self.file["Price"][self.file['Type'] == piece].values[0]

                new_name_entry.insert(0, new_name_text)
                new_price_entry.insert(0, new_price_text)

            new_label.grid(row=row_nb, column=1, pady=3, padx=(50, 5), sticky='w')
            new_price_entry.grid(row=row_nb, column=3, pady=3, padx=5, sticky='we')
            new_name_entry.grid(row=row_nb, column=2, pady=3, padx=5)

            self.price_entry_list += [new_price_entry]

            self.draft_entries[piece] = {
                "Type": piece,
                "Name": new_name_entry,
                "Price": new_price_entry
            }

    def update_price(self):
        price_sum = 0
        for price_entry in self.price_entry_list:
            try:
                if price_entry.get() != "":
                    price_sum += float(price_entry.get())
            except TypeError:
                messagebox.showinfo(title="Oops", message="Please, only enter numbers in the price column")
        self.entry_calculated_price.delete(0, END)
        self.entry_calculated_price.insert(0, price_sum)


class Build(Frame):
    def __init__(self, **kw):
        super().__init__(**kw, bg=BACKGROUND)

        self.file = self.master.build_file[self.master.build_file['Build'] == self.master.file_name].reset_index()

        self.header = add_canvas(self, "./images/logo_build.png", 1150, 64)
        self.header.grid(column=0, row=0, pady=(0, 20), columnspan=5, sticky='we')
        self.name_label = MyLabel("Name", master=self, bg=BACKGROUND)
        self.price_sold_label = MyLabel("Price sold", master=self, bg=BACKGROUND)
        self.price_bought_label = MyLabel("Price", master=self, bg=BACKGROUND)
        self.type_label = MyLabel("Type", master=self, bg=BACKGROUND)

        self.type_label.grid(column=0, row=1, padx=1, pady=(5, 20), sticky='we')
        self.name_label.grid(column=1, row=1, padx=1, pady=(5, 20), sticky='we')
        self.price_bought_label.grid(column=2, row=1, padx=1, pady=(5, 20), sticky='we')
        self.price_sold_label.grid(column=3, row=1, padx=1, pady=(5, 20), sticky='we')

        self.optionlist = []

        if len(self.file) > 0 and self.file['Type'][0] != "":
            for index, row in self.file.iterrows():
                self.add_option(
                    piece_type=row['Type'],
                    piece_name=row['Name'],
                    bought_price=row['Price_bought'],
                    sold_price=row['Price_sold'])
        else:
            self.add_option()

        self.grid_columnconfigure(0, minsize=240)
        self.grid_columnconfigure(1, minsize=550)
        self.grid_columnconfigure(2, minsize=20)
        self.grid_columnconfigure(3, minsize=20)

    def add_option(self, piece_type="", piece_name="", bought_price="", sold_price=""):
        if hasattr(self, "add_button"):
            self.add_button.destroy()
            self.copy_button.destroy()
            self.entry_estimated_price.destroy()
            self.label_calculated_price.destroy()
            self.entry_calculated_price.destroy()
            self.label_suggested_price.destroy()
            self.entry_suggested_price.destroy()
            self.label_final_price.destroy()
            self.entry_final_price.destroy()
            self.update_button.destroy()

        self.new_row = OptionMenuRow(piece_type, piece_name, bought_price, sold_price, master=self)
        self.new_row.grid(column=0, row=self.grid_size()[1] + 1, columnspan=4, sticky='w')

        self.optionlist += [self.new_row]

        rownb = self.new_row.grid_info()['row']
        self.del_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_del_sleep.png",
                                     img_enter="./images/Button_del_hover.png", bg=BACKGROUND,
                                     highlightthickness=0, activebackground=BACKGROUND)
        self.del_button.config(command= lambda row=self.new_row, button=self.del_button: self.delete_row(row, button))
        self.del_button.grid(column=4, row=rownb , sticky='w')

        self.create_footer()

    def delete_row(self, row, button):
        self.optionlist.remove(row)

        row.destroy()
        button.destroy()

    def create_footer(self):
        self.add_button = self.create_add_button()
        self.copy_button = self.create_copy_button()
        self.add_button.grid(row=self.grid_size()[1], column=0, pady=(30, 5))
        self.copy_button.grid(row=self.grid_size()[1] - 1, column=1, pady=(30, 5), sticky="w")

        self.label_calculated_price = MyLabel("Total:", master=self, font=(FONT_NAME, 15))
        self.entry_calculated_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=12)
        self.entry_estimated_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=12)

        self.label_calculated_price.grid(column=1, row=self.grid_size()[1] - 1, pady=(30, 5), padx=5, sticky="E")
        self.entry_calculated_price.grid(column=2, row=self.grid_size()[1] - 1, pady=(30, 5), padx=5)
        self.entry_estimated_price.grid(column=3, row=self.grid_size()[1] - 1, pady=(30, 5), padx=(5, 1))

        self.label_suggested_price = MyLabel("+10%:", master=self, font=(FONT_NAME, 15))
        self.entry_suggested_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=12)
        self.label_suggested_price.grid(column=1, row=self.grid_size()[1], pady=5, padx=5, sticky="E")
        self.entry_suggested_price.grid(column=2, row=self.grid_size()[1] - 1, pady=5, padx=5)

        self.label_final_price = MyLabel("Final price:", master=self, font=(FONT_NAME, 15))
        self.label_final_price.config(width=10)
        self.entry_final_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=12)
        self.label_final_price.grid(column=2, row=self.grid_size()[1], pady=5, padx=5, sticky="we")
        self.entry_final_price.grid(column=3, row=self.grid_size()[1] - 1, pady=5, padx=(5, 1))

        if len(self.file) > 0:
            final_price_text = str(self.file["Final_Price"].unique()[0])
            self.entry_final_price.insert(0, final_price_text)

        self.update_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_update_sleep.png",
                                         img_enter="./images/Button_update_hover.png", bg=BACKGROUND,
                                         highlightthickness=0, activebackground=BACKGROUND)
        self.update_button.config(command=self.update_price)
        self.update_button.grid(column=1, row=self.grid_size()[1] - 1, pady=(5, 5), padx=(0, 25), sticky="e")

    def create_add_button(self):
        add_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_add_sleep.png",
                                 img_enter="./images/Button_add_hover.png")
        add_button.config(bg=BACKGROUND, highlightthickness=0, activebackground=BACKGROUND,
                          command=self.add_option)
        return add_button

    def create_copy_button(self):
        copy_button = HoverButton(self, borderwidth=0, img_leave="./images/Button_copy_sleep.png",
                                  img_enter="./images/Button_copy_hover.png", bg=BACKGROUND,
                                  highlightthickness=0, activebackground=BACKGROUND)
        copy_button.config(command=self.copy_build)

        return copy_button

    def copy_build(self, ):
        text_to_print = ""

        for option in self.optionlist:

            type_to_copy = option.variable_type.get()
            if type_to_copy == "":
                pass
            else:
                name = option.variable_name.get()
                indx = name.find("-") + 1
                name_to_copy = name[indx:]

                line_to_print = f"{type_to_copy}: {name_to_copy}; \n"
                text_to_print += line_to_print

        self.clipboard_clear()
        self.clipboard_append(text_to_print)
        self.update()  # now it stays on the clipboard after the window is closed

    def update_price(self):
        bought_sum = 0
        sold_sum = 0

        for price_entry in self.optionlist:
            if price_entry.bought_price.get() != "":
                try:
                    bought_sum += float(price_entry.bought_price.get())
                except TypeError:
                    messagebox.showinfo(title="Oops", message="Please, only enter numbers in the price column")
            else:
                bought_sum += 0

            if price_entry.sold_price.get() != "":
                try:
                    sold_sum += float(price_entry.sold_price.get())
                except TypeError:
                    messagebox.showinfo(title="Oops", message="Please, only enter numbers in the price column")
            else:
                sold_sum += 0

        up_sum = bought_sum + ((10 / 100) * bought_sum)
        self.entry_calculated_price.delete(0, END)
        self.entry_calculated_price.insert(0, bought_sum)

        self.entry_estimated_price.delete(0, END)
        self.entry_estimated_price.insert(0, sold_sum)

        self.entry_suggested_price.delete(0, END)
        self.entry_suggested_price.insert(0, up_sum)


class OptionMenuRow(Frame):
    def __init__(self, piece_type, piece_name, bought_price, sold_price, **kw):
        super().__init__(**kw, bg=BACKGROUND)

        self.inventory = self.master.master.inventory
        self.bought_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=12)
        self.sold_price = Entry(self, bg=BACKGROUND, fg=LIGHT, font=(FONT_NAME, 15), width=12)
        self.bought_price.insert(0, bought_price)
        self.sold_price.insert(0, sold_price)

        self.variable_type = StringVar(self)
        self.variable_name = StringVar(self)

        self.variable_type.trace('w', self.update_options)
        self.variable_name.trace("w", self.on_option_change)

        self.optionmenu_type = OptionMenu(self, self.variable_type, *self.inventory.type_list)
        self.optionmenu_type.config(highlightthickness=0, font=(FONT_NAME, 13),anchor='w', width = 10)
        self.optionmenu_type['menu'].config(font=(FONT_NAME, 13))

        self.optionmenu_name = OptionMenu(self, self.variable_name, '')
        self.optionmenu_name.config(highlightthickness=0, font=(FONT_NAME, 13), width=30,anchor='w')
        self.optionmenu_name['menu'].config(font=(FONT_NAME, 13))

        if piece_type != "":
            self.variable_type.set(piece_type)
            self.variable_name.set(piece_name)

        self.optionmenu_type.grid(row=0, column=0, pady=5, padx=5, sticky='we')
        self.optionmenu_name.grid(row=0, column=1, pady=5, padx=5, sticky='we')

        self.bought_price.grid(row=0, column=2, pady=5, padx=5, sticky='we')
        self.sold_price.grid(row=0, column=3, pady=5, padx=5, sticky='we')


        self.grid_columnconfigure(0, minsize=250)
        self.grid_columnconfigure(1, minsize=550)
        self.grid_columnconfigure(2, minsize=80)
        self.grid_columnconfigure(3, minsize=50)

    def update_options(self, *args):
        selected_type = self.variable_type.get()
        piece_dic = self.inventory.inventory.to_dict(orient="records")

        selected_names = [piece_set["IDName"] for piece_set in piece_dic if piece_set["Type"] == selected_type and
                            piece_set["IDName"] not in list(self.master.master.build_file["Name"])]

        self.variable_name.set("")

        menu = self.optionmenu_name['menu']
        menu.delete(0, 'end')

        for piece_name in selected_names:
            menu.add_command(label=piece_name, command=lambda nation=piece_name: self.variable_name.set(nation))

    def on_option_change(self, *args):
        selected_name = self.variable_name.get()
        piece_dic = self.inventory.inventory.to_dict(orient="records")

        newprice = [piece["Paid Price"] for piece in piece_dic if piece["IDName"] == selected_name]

        self.bought_price.delete(0, "end")
        self.bought_price.insert(0, newprice)

