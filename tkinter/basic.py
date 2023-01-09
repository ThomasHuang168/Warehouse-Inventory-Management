from tkinter import *
from tkinter import ttk
from io import StringIO
from tkinter.tix import ComboBox
import pandas as pd
import os
import logging

# from tkinter import messagebox


database_csv_path = r"testing/guid.csv"
database_csv_cols_2_default = {
    "guid": None,
    "name": "",
    "loc": "",
    "remark": "",
}  # None means no default is allow
if not os.path.exists(database_csv_path):
    pd.DataFrame(columns=database_csv_cols_2_default.keys()).to_csv(
        database_csv_path, index=False
    )

_database = pd.read_csv(database_csv_path)
# creating root window
root = Tk()

# function_definitions
def callback():
    text = textEditor.get(0.1, END)
    print(text)


# defining text editor
textEditor = Text(root, width=43, height=10)
textEditor.pack()

_t = Text(root)
_t.pack()

# button 1
button1 = Button(root, text="Display Text1", command=callback)
button1.pack()
button1.pack(pady=12)
# button 1
button2 = Button(root, text="Display Text2", command=callback)
button2.pack()


_values = ["add Box", "Search", "Print Labels"]
_c = ttk.Combobox(root, values=_values)
_c.pack()

# root.geometry('350x218')
root.title("PythonLobby")
root.mainloop()
