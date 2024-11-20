from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import date, datetime

from tkcalendar import Calendar


class App:
    def __init__(self, root) -> None:
        self.root: "Tk" = root
        self.root.title("Expense Helper")

        # self.style = ttk.Style()
        # self.style.configure(
        #     "Blue.TFrame", background="blue", borderwidth=5, relief="raised"
        # )

        self.mainframe = ttk.Frame(self.root, width=600, height=600, padding=50)
        self.mainframe.grid()

        self.listOfReceiptPaths = self.getListOfReceiptPaths()
        self.SelectDates()

    def SelectDates(self) -> None:
        self.clearMainframe()

        self.receiptDates = []

        ####
        # Create widgets
        ####
        SelectDates = ttk.Frame(self.mainframe, width=600, height=600)

        today = date.today()
        calender = Calendar(
            SelectDates,
            selectmode="day",
            year=today.year,
            month=today.month,
            day=today.day,
        )

        expenseLabelText = StringVar()
        expenseLabelText.set("Pick the starting date of expenses")

        expenseLabel = ttk.Label(SelectDates, textvariable=expenseLabelText)

        def calenderNextSelectionFunction():
            if len(self.receiptDates) == 0:
                self.receiptDates.append(calender.selection_get())
                expenseLabelText.set("Pick the final date of expenses")

            elif len(self.receiptDates) == 1:
                self.receiptDates.append(calender.selection_get())
                self.Receipts()

        calenderNextSelection = ttk.Button(
            SelectDates, text="Next", command=calenderNextSelectionFunction
        )

        ####
        # Grid all the widgets
        ####
        SelectDates.grid()
        calender.grid()
        expenseLabel.grid()
        calenderNextSelection.grid()

    def Receipts(self):
        self.clearMainframe()

        ####
        # Create widgets
        ####
        Receipts = ttk.Frame(self.mainframe, width=600, height=600)

        for r in self.listOfReceiptPaths:
            pass
        pass

    @staticmethod
    def getListOfReceiptPaths() -> list:
        receiptDirectory = filedialog.askdirectory()
        fileList = os.listdir(receiptDirectory)
        listOfReceiptPaths = []
        validFormats = [".png", ".jpg", ".jpeg"]
        for file in fileList:
            if os.path.splitext(file)[1] in validFormats:
                listOfReceiptPaths.append(os.path.abspath(file))

        return listOfReceiptPaths

    def clearMainframe(self) -> None:
        for c in self.mainframe.winfo_children():
            c.destroy()


root = Tk()
App(root)
root.mainloop()
