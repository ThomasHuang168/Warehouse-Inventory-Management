# This GUI is to add book into the database
# people need to specify the location first
# and then other fields are enable and allow user to type in
# and then specifc the book global ID and book's ISBN
# the system will look for metadata of the book and display to the user
# even if nothing is found, fields are still shown to the user in GUI
# User will check if it is correct and decide if he/she will continue to next book
# A button "Next" is available to allow user moving to next book
# all fields except location are emptied
#
"""Add Book GUI
"""

__version__ = "0.1"
__author__ = "Huang Hing Pang"

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# import subprocess

# https://stackoverflow.com/a/67934061
import logging
import os
import time
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
import json
import isbnlib
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import pandas as pd

from pathlib import Path

info = logging.getLogger(__name__).info


class add_book_gui:
    def __init__(self, master) -> None:
        self.master = master
        master.winfo_toplevel().title("Add Book")
        self.proc = None
        self.__close = False
        i_row = 0

        # Location ID
        self.lbl_Location = ttk.Label(master, text="Location")
        self.lbl_Location.grid(row=i_row, column=0)

        self.ent_Location = ttk.Entry(master, font=40, width=70)
        self.ent_Location.grid(row=i_row, column=1)

        i_row += 1
        # Book ID
        self.lbl_BookID = ttk.Label(master, text="Book ID")
        self.lbl_BookID.grid(row=i_row, column=0)

        self.ent_BookID = ttk.Entry(master, font=40, width=70)
        self.ent_BookID.grid(row=i_row, column=1)

        i_row += 1
        # ISBN
        self.lbl_ISBN = ttk.Label(master, text="ISBN")
        self.lbl_ISBN.grid(row=i_row, column=0)

        self.ent_ISBN = ttk.Entry(master, font=40, width=70)
        self.ent_ISBN.grid(row=i_row, column=1)

        # Search Button
        self.btn_Search = ttk.Button(
            master, text="Search ISBN", command=self.browsefunc_search
        )
        self.btn_Search.grid(row=i_row, column=2)

        i_row += 1
        # Display Book Meta
        self.lbl_Meta = ttk.Label(master, text="Meta")
        self.lbl_Meta.grid(row=i_row, column=0)

        self.frame_Meta = Frame(master)
        self.frame_Meta.grid(row=i_row, column=1)

        self.txt_Meta = Text(self.frame_Meta, state="normal", wrap="word")
        self.Scrollbar_Meta = Scrollbar(
            self.frame_Meta, orient="vertical", command=self.txt_Meta.yview
        )
        self.txt_Meta.configure(yscrollcommand=self.Scrollbar_Meta.set)
        self.Scrollbar_Meta.pack(side="right", fill="y")
        self.txt_Meta.pack(side="left", fill="both", expand=True)

        # Save Button
        self.btn_Save = ttk.Button(
            master, text="Save", command=self.browsefunc_save
        )
        self.btn_Save.grid(row=i_row, column=2)

    def browsefunc_search(self):
        # try to show the list of meta
        _meta: dict[str, str] = {
            "Location": self.ent_Location.get(),
            "ID": self.ent_BookID.get(),
            "ISBN-13": "",
            "Title": "",
            "Authors": "",
            "Publisher": "",
            "Year": "",
            "Language": "",
        }
        try:
            _meta.update(isbnlib.meta(self.ent_ISBN.get()))
        except:
            pass
        self.txt_Meta.delete("1.0", END)
        self.txt_Meta.insert(END, dump(_meta, Dumper=Dumper))

    def browsefunc_save(self):
        dict_row: dict[str] = load(
            self.txt_Meta.get("1.0", END), Loader=Loader
        )
        target_path: Path = Path(r"C:\Users\Public\Downloads\book.csv")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if not target_path.exists():
            with target_path.open("w") as fw:
                fw.write(f'{", ".join(dict_row.keys())}\n')
        dict_row["Authors"] = "|||".join(dict_row["Authors"])
        with target_path.open("a") as fa:
            fa.write(f'{", ".join(dict_row.values())}\n')
        self.txt_Meta.delete("1.0", END)

    # def read_output(self):
    #     pass

    # def show_stdout(self):
    #     pass

    def stop(self):
        """Stop subprocess and quit GUI."""
        if self.__close:
            return  # avoid killing subprocess more than once
        self.__close = True

        info("stopping")
        self.master.destroy()  # exit GUI
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    master = Tk()
    app = add_book_gui(master)
    master.protocol(
        "WM_DELETE_WINDOW", app.stop
    )  # exit subprocess if GUI is closed
    master.mainloop()
    info("exited")
