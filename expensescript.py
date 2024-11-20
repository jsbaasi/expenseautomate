from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import date
from tkcalendar import Calendar

_dates = []


def getListOfReceiptPaths() -> list:
    receiptDirectory = filedialog.askdirectory()
    fileList = os.listdir(receiptDirectory)
    listOfReceiptPaths = []
    validFormats = [".png", ".jpg", ".jpeg"]
    for file in fileList:
        if os.path.splitext(file)[1] in validFormats:
            listOfReceiptPaths.append(os.path.abspath(file))

    return listOfReceiptPaths


receiptPaths = getListOfReceiptPaths()


root = Tk()
root.title("Expense Helper")
root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.geometry("600x600")

s = ttk.Style()
s.configure("Blue.TFrame", background="blue", borderwidth=5, relief="raised")

mainframe = ttk.Frame(root, padding=50, style="Blue.TFrame")

mainframe.grid(sticky="nsew")

today = date.today()
calender = Calendar(
    mainframe, selectmode="day", year=today.year, month=today.month, day=today.day
)
calender.grid(column=0, row=0)

_expenseLabelText = StringVar()
_expenseLabelText.set("Pick the starting date of expenses")

expenseLabel = ttk.Label(mainframe, textvariable=_expenseLabelText).grid(
    column=0, row=1
)


def clearPage():
    if len(_dates) == 0:
        _dates.append(calender.get_date())
        _expenseLabelText.set("Pick the end date of expenses")

    else:
        _dates.append(calender.get_date())
        widgetsToClear = mainframe.grid_slaves()
        for widget in widgetsToClear:
            widget.grid_forget()
        img = ImageTk.PhotoImage(Image.open("example1.png"))
        ttk.Label(mainframe, image=img).grid(column=0, row=0)
        ttk.Button(mainframe, text="Quit", command=root.destroy).grid(column=0, row=1)


ttk.Button(mainframe, text="Next", command=clearPage).grid(column=0, row=2)

root.mainloop()
