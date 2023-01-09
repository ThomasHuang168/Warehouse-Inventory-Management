import re
import tkinter as tk
from tkinter import ttk
from typing import Union
import pandas as pd


class Model:
    """
    sqlite models
    create empty table if path is None
    decorate sql syntax with function call
    """

    def __init__(self, email):
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        """
        Validate the email
        :param value:
        :return:
        """
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(pattern, value):
            self.__email = value
        else:
            raise ValueError(f"Invalid email address: {value}")

    def save(self):
        """
        Save the email into a file
        :return:
        """
        with open("emails.txt", "a") as f:
            f.write(self.email + "\n")


class View(ttk.Frame):
    """
    use notebook and frame to manage add_box, search_book, generate_guid

    add_box:
    entry to take box guid
    text to take books' guid and isbn id
    button to save information

    search_book:
    entry to take book or box guid
    button to triiger search and display result
    text to display result and save updates
    button to trigger save result
    button to abort changes (back)

    generate_guid:
    entry to specify number of labels to be printed
    button to trigger the pdf generation and create entry to table
    """

    def __init__(self, parent):
        super().__init__(parent)

        # create widgets
        # create notebook
        notebook = ttk.Notebook(self)
        notebook.pack(pady=10, expand=True)

        frame_srh_book = ttk.Frame(notebook)
        frame_srh_book.pack(fill="both", expand=True)
        notebook.add(frame_srh_book, text="Search Book")

        frame_add_box = ttk.Frame(notebook)
        frame_add_box.pack(fill="both", expand=True)
        notebook.add(frame_add_box, text="Add Box")

        frame_add_guid = ttk.Frame(notebook)
        frame_add_guid.pack(fill="both", expand=True)
        notebook.add(frame_add_guid, text="Labels")

        # label
        self.label = ttk.Label(frame_srh_book, text="Email:")
        self.label.grid(row=1, column=0)

        # email entry
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(
            frame_srh_book, textvariable=self.email_var, width=30
        )
        self.email_entry.grid(row=1, column=1, sticky=tk.NSEW)

        # save button
        self.save_button = ttk.Button(
            frame_srh_book, text="Save", command=self.save_button_clicked
        )
        self.save_button.grid(row=1, column=3, padx=10)

        # message
        self.message_label = ttk.Label(
            frame_srh_book, text="", foreground="red"
        )
        self.message_label.grid(row=2, column=1, sticky=tk.W)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """
        self.controller = controller

    def save_button_clicked(self):
        """
        Handle button click event
        :return:
        """
        if self.controller:
            self.controller.save(self.email_var.get())

    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """
        self.message_label["text"] = message
        self.message_label["foreground"] = "red"
        self.message_label.after(3000, self.hide_message)
        self.email_entry["foreground"] = "red"

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label["text"] = message
        self.message_label["foreground"] = "green"
        self.message_label.after(3000, self.hide_message)

        # reset the form
        self.email_entry["foreground"] = "black"
        self.email_var.set("")

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label["text"] = ""


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def save(self, email):
        """
        Save the email
        :param email:
        :return:
        """
        try:

            # save the model
            self.model.email = email
            self.model.save()

            # show a success message
            self.view.show_success(f"The email {email} saved!")

        except ValueError as error:
            # show an error message
            self.view.show_error(error)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter MVC Demo")

        # create a model
        model = Model("hello@pythontutorial.net")

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == "__main__":
    app = App()
    app.mainloop()
