from os import listdir
import pandas as pd
from tkinter import messagebox

class FileManager:
    def __init__(self):
        self.inventory = self.load_inventory()
        self.type_list = list(self.inventory["Type"].unique())

    def load_file(self, file_name):
        if file_name is not None:
            imported_data = pd.read_csv(f"./data/{file_name}", keep_default_na=False)
            return imported_data
        else:
            return None


    def load_inventory(self):
        raw_inv = pd.read_csv("./raw/Inventory.csv")

        raw_inv['ID'] = raw_inv['ID'].astype(float)
        raw_inv['ID'] = raw_inv['ID'].astype(str)
        raw_inv['Name'] = raw_inv['Name'].astype(str)

        parts_available = raw_inv[raw_inv["Status"] == "In"].copy()

        for index, values in parts_available["ID"].items():
            parts_available["ID"].loc[[index]] = values.replace('.0', ' - ')

        parts_available["IDName"] = ""
        parts_available["IDName"] = parts_available['ID'] + parts_available['Name']

        inventory = parts_available[['Type', 'IDName', 'Paid Price']]

        return inventory
