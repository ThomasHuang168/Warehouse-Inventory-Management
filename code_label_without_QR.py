# This file is part of pylabels, a Python library to create PDFs for printing
# labels.
# Copyright (C) 2012, 2013, 2014 Blair Bonnett
#
# pylabels is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pylabels is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# pylabels.  If not, see <http://www.gnu.org/licenses/>.

import labels
from pathlib import Path
from reportlab.graphics import shapes
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.barcode import code128, qr
from reportlab.lib.units import mm
from reportlab.lib.colors import white
from uuid import uuid4
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import pandas as pd

# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # objective of this function is to create a barcode and string underleave centered in the label
    # the width and height of the barcode labels are not ertain
    # their relationshio with text encoded is not known as well
    # aligh center of barcode with center of label maximize tolerance of printing error
    # afterthat, text should be aligned either above or below the barcode

    barcode_value = str(obj)
    # _qr = createBarcodeDrawing("QR", value=barcode_value)
    # # _qr.translate(0, 50)
    # label.add(_qr)

    # barcode128 = code128.Code128(barcode_value)
    barcode128 = createBarcodeDrawing("Code128", value=barcode_value)
    # barcode128.translate(0, _qr.height)
    label.add(barcode128)
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    _text_len_per_line = 12  # find a way to not hardcoding this
    _text_len = len(str(obj))
    _text_top = 0
    # _text_top += _qr.height
    _text_top += barcode128.height
    _text_height = 20
    _text_left = 0
    # _text_left += _qr.width
    for _line_index, (_line_start, _line_end) in enumerate(
        [
            (_i, min((_i + _text_len_per_line), _text_len))
            for _i in range(0, _text_len, _text_len_per_line)
        ]
    ):
        _Text = shapes.String(
            _text_left,
            _text_top - _line_index * _text_height,
            str(obj)[_line_start:_line_end],
            fontName="Helvetica",
            fontSize=_text_height,
        )
        # _Text.translate(_qr.width, 0)
        label.add(_Text)

    # # barcode128.drawOn(label, 1*mm, 1*mm)

    # # create qr code
    # # bar level is measure of extra bits added to improve chances of decoding
    # qrw = qr.QrCodeWidget(barcode_value, barLevel="M")
    # b = qrw.getBounds()

    # w = b[2] - b[0]
    # h = b[3] - b[1]

    # d = shapes.Drawing(w, h, transform=[70. / w, 0, 0, 70. / h, 0, 0])
    # d.add(shapes.Rect(0, 0, w, h, fillColor=white))

    # d.add(qrw)
    # label.add(d)


class code_label_gui:
    def __init__(self, master):
        self.master = master
        master.winfo_toplevel().title("generate label")

        self._close = False
        i_row = 0
        self.lbl_excel_file = ttk.Label(master, text="Path of Excel:")
        self.lbl_excel_file.grid(row=i_row, column=0)

        self.ent_excel_file = ttk.Entry(master, font=40, width=70)
        self.ent_excel_file.grid(row=i_row, column=1)

        def browsefunc_Target_Model():
            filename = filedialog.askopenfilename(
                filetypes=(("excels files", "*.xlsx"), ("All files", "*.*"))
            )
            filename = filename.replace("/", "\\\\")
            self.ent_excel_file.delete(0, END)
            self.ent_excel_file.insert(0, filename)  # add this

        self.btn_Target_Model = ttk.Button(
            master, text="Browse", command=browsefunc_Target_Model
        )
        self.btn_Target_Model.grid(row=i_row, column=2)

        i_row += 1
        self.btn_go = ttk.Button(
            master, text="get label", command=self.print_labels
        )
        self.btn_go.grid(row=i_row, column=2)

    def print_labels(self):
        # Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
        # labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
        # automatically calculated.
        # specs = labels.Specification(210, 297, 2, 6, 90, 45, corner_radius=2)
        specs = labels.Specification(
            210,
            297,
            5,
            13,
            38,
            21,
            corner_radius=2,
            left_margin=6,
            right_margin=6,
            column_gap=2,
            row_gap=0,
            top_margin=11,
            bottom_margin=13,
        )

        _df_labels = pd.read_excel(self.ent_excel_file.get(), header=None)
        list_labels = _df_labels[0].to_list()
        # "C:\Users\Admin\Desktop\Book1.xlsx"
        # Create the sheet.
        sheet = labels.Sheet(specs, draw_label, border=True)

        # numLabel = 12
        # label_file_stem = Path(self.ent_excel_file.get()).stem

        # sheet.add_labels([uuid4() for _ in range(numLabel)])
        # sheet.add_labels([f"{_i}" for _i in range(numLabel)])
        sheet.add_labels(list_labels)

        # # Add a couple of labels.
        # sheet.add_label("Hello")
        # sheet.add_label("World")

        # # We can also add each item from an iterable.
        # sheet.add_labels(range(3, 22))

        # # Note that any oversize label is automatically trimmed to prevent it messing up
        # # other labels.
        # sheet.add_label("Oversized label here")

        # Save the file and we are done.
        (
            path_labal := Path(self.ent_excel_file.get()).with_suffix(".pdf")
        ).unlink(missing_ok=True)
        sheet.save(str(path_labal))
        print(
            "{0:d} label(s) output on {1:d} page(s).".format(
                sheet.label_count, sheet.page_count
            )
        )


if __name__ == "__main__":
    master = Tk()
    app = code_label_gui(master)
    master.mainloop()
