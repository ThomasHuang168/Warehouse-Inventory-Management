# from tkinter import *
# from tkinter import ttk
# from io import StringIO
# from tkinter.tix import ComboBox
# import pandas as pd
# import os
# import logging
# #from tkinter import messagebox


# database_csv_path = r"testing/guid.csv"
# database_csv_cols_2_default = {"guid": None, "name": "", "loc": "", "remark": ""} #None means no default is allow
# if not os.path.exists(database_csv_path):
#     pd.DataFrame(columns=database_csv_cols_2_default.keys()).to_csv(database_csv_path, index=False)

# _database = pd.read_csv(database_csv_path)
# #creating root window
# root = Tk()

# #function_definitions
# def callback():
#     text = textEditor.get(0.1,END)
#     print(text)

# #defining text editor
# textEditor = Text(root, width=43, height=10)
# textEditor.pack()

# _t = Text(root)
# _t.pack()

# #button 1
# button1 = Button(root, text="Display Text1", command = callback )
# button1.pack()
# button1.pack(pady=12)
# #button 1
# button2 = Button(root, text="Display Text2", command = callback )
# button2.pack()


# _values= ["add Box", "Search", "Print Labels"]
# _c = ttk.Combobox(root, values=_values)
# _c.pack()

# # root.geometry('350x218')
# root.title("PythonLobby")
# root.mainloop()
"""Point Matching GUI
"""

__version__ = "0.1"
__author__ = "Tim Davis, Huang Hing Pang"

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

info = logging.getLogger(__name__).info


class point_matching_gui:
    def __init__(self, master):
        self.master = master
        master.winfo_toplevel().title("Point Matching")
        self.proc = None
        self.__close = False
        i_row = 0

        # Model
        self.lbl_Model = ttk.Label(master, text="Model")
        self.lbl_Model.grid(row=i_row, column=0)

        self.ent_Model = ttk.Entry(master, font=40, width=70)
        self.ent_Model.grid(row=i_row, column=1)

        def browsefunc_Model():
            filename = filedialog.askopenfilename(
                filetypes=(("csv files", "*.csv"), ("All files", "*.*"))
            )
            filename = filename.replace("/", "\\\\")
            self.ent_Model.delete(0, END)
            self.ent_Model.insert(0, filename)  # add this

        self.btn_Model = ttk.Button(
            master, text="Browse", command=browsefunc_Model
        )
        self.btn_Model.grid(row=i_row, column=2)

        self.com_Model = ttk.Combobox(
            master,
            values=("m", "mm"),
            state="readonly",
        )
        self.com_Model.current(1)
        self.com_Model.grid(row=i_row, column=3)

        i_row += 1
        # Survey
        self.lbl_Survey = ttk.Label(master, text="Survey")
        self.lbl_Survey.grid(row=i_row, column=0)

        self.ent_Survey = ttk.Entry(master, font=40, width=70)
        self.ent_Survey.grid(row=i_row, column=1)

        def browsefunc_Survey():
            filename = filedialog.askopenfilename(
                filetypes=(("csv files", "*.csv"), ("All files", "*.*"))
            )
            filename = filename.replace("/", "\\\\")
            self.ent_Survey.delete(0, END)
            self.ent_Survey.insert(0, filename)  # add this

        self.btn_Survey = ttk.Button(
            master, text="Browse", command=browsefunc_Survey
        )
        self.btn_Survey.grid(row=i_row, column=2)

        self.com_Survey = ttk.Combobox(
            master,
            values=("m", "mm"),
            state="readonly",
        )
        self.com_Survey.current(1)
        self.com_Survey.grid(row=i_row, column=3)

        i_row += 1
        # XY Tolerance
        self.lbl_XY_Tolerance = ttk.Label(master, text="X/Y Tolerance")
        self.lbl_XY_Tolerance.grid(row=i_row, column=0)

        self.str_XY_Tolerance = StringVar()
        self.str_XY_Tolerance.initialize("1000")
        self.ent_XY_Tolerance = Entry(
            master, textvariable=self.str_XY_Tolerance
        )
        self.ent_XY_Tolerance.grid(row=i_row, column=1)

        i_row += 1
        # XYZ Tolerance
        self.lbl_XYZ_Tolerance = ttk.Label(master, text="X/Y/Z Tolerance")
        self.lbl_XYZ_Tolerance.grid(row=i_row, column=0)

        self.str_XYZ_Tolerance = StringVar()
        self.str_XYZ_Tolerance.initialize("1000")
        self.ent_XYZ_Tolerance = Entry(
            master, textvariable=self.str_XYZ_Tolerance
        )
        self.ent_XYZ_Tolerance.grid(row=i_row, column=1)

        i_row += 1
        # log
        self.lbl_Log = ttk.Label(master, text="Log")
        self.lbl_Log.grid(row=i_row, column=0)

        self.frame_Log = Frame(master)
        self.frame_Log.grid(row=i_row, column=1)

        self.txt_Log = Text(self.frame_Log, state="normal", wrap="word")
        self.Scrollbar_Log = Scrollbar(
            self.frame_Log, orient="vertical", command=self.txt_Log.yview
        )
        self.txt_Log.configure(yscrollcommand=self.Scrollbar_Log.set)
        self.Scrollbar_Log.pack(side="right", fill="y")
        self.txt_Log.pack(side="left", fill="both", expand=True)

        self.btn_go = ttk.Button(master, text="Go", command=self.browsefunc_go)
        self.btn_go.grid(row=i_row, column=3)

        # Create a buffer for the stdout
        self.stdout_data = ""
        # Create a new thread that will read stdout and write the data to
        # `self.stdout_buffer`
        thread = Thread(
            target=self.read_output,
            # args=(self.proc.stdout,)
        )
        thread.start()

        # A tkinter loop that will show `self.stdout_data` on the screen
        self.show_stdout()

    def browsefunc_go(self):
        if None == self.proc:
            #
            pass
        else:
            self.proc.terminate()

            # kill subprocess if it hasn't exited after a countdown
            def kill_after(countdown):
                if self.proc.poll() is None:  # subprocess hasn't exited yet
                    countdown -= 1
                    if countdown < 0:  # do kill
                        info("killing")
                        self.proc.kill()  # more likely to kill on *nix
                    else:
                        self.master.after(1000, kill_after, countdown)
                        return  # continue countdown in a second

                # self.proc.stdout.close()  # close fd
                self.proc.wait()  # wait for the subprocess' exit

            kill_after(countdown=5)
            self.stdout_data = ""

        cmd = [
            "HPC_IFC_POINT_MATCHING.exe",
            "-s",
            self.ent_Survey.get(),
            "-su",
            self.com_Survey.get(),
            "-m",
            self.ent_Model.get(),
            "-mu",
            self.com_Model.get(),
            "-t",
            self.ent_XY_Tolerance.get(),
            "-mt",
            self.ent_XYZ_Tolerance.get(),
            "-o",
            os.path.join(
                os.path.dirname(self.ent_Model.get()),
                "point_matching_output.csv",
            ),
        ]

        self.stdout_data = f'CMD: {" ".join(cmd)}'
        self.proc = Popen(cmd, stdout=PIPE, stderr=STDOUT)

    def read_output(self):
        """Read subprocess' output and store it in `self.stdout_data`."""
        while True:
            if self.__close:  # clean up
                info("eof")
                return None
            if None == self.proc or None == self.proc.stdout:
                time.sleep(0.005)
                continue
            data = os.read(self.proc.stdout.fileno(), 1 << 20)
            if None != self.proc.stderr and str == type(data):
                data += os.read(self.proc.stderr.fileno(), 1 << 20)
            # masters uses: "\r\n" instead of "\n" for new lines.
            data = data.replace(b"\r\n", b"\n")
            if data:
                info("got: %r", data)
                self.stdout_data += data.decode()
                pass

    def show_stdout(self):
        """Read `self.stdout_data` and put the data in the GUI."""
        if len(self.stdout_data):
            self.txt_Log["state"] = "normal"
            # self.txt_Log.set(self.stdout_data.strip("\n"))
            self.txt_Log.insert(END, self.stdout_data)
            self.txt_Log.see("end")
            self.stdout_data = ""
            self.txt_Log["state"] = "disabled"
        self.master.after(100, self.show_stdout)

    def stop(self):
        """Stop subprocess and quit GUI."""
        if self.__close:
            return  # avoid killing subprocess more than once
        self.__close = True

        info("stopping")
        self.master.destroy()  # exit GUI
        if None != self.proc:
            self.proc.terminate()  # tell the subprocess to exit

            # kill subprocess if it hasn't exited after a countdown
            def kill_after(countdown):
                if self.proc.poll() is None:  # subprocess hasn't exited yet
                    countdown -= 1
                    if countdown < 0:  # do kill
                        info("killing")
                        self.proc.kill()  # more likely to kill on *nix
                    else:
                        self.master.after(1000, kill_after, countdown)
                        return  # continue countdown in a second

                self.proc.stdout.close()  # close fd
                self.proc.wait()  # wait for the subprocess' exit

            kill_after(countdown=5)


# # https://stackoverflow.com/a/8960839
#     def validate(
#         self,
#         action,
#         index,
#         value_if_allowed,
#         prior_value,
#         text,
#         validation_type,
#         trigger_type,
#         widget_name,
#     ):
#         pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    master = Tk()
    app = point_matching_gui(master)
    master.protocol(
        "WM_DELETE_WINDOW", app.stop
    )  # exit subprocess if GUI is closed
    master.mainloop()
    info("exited")
