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
        _pageNumber = 0
        _totalPages = len(self.listOfReceiptPaths)
        ####
        # Create widgets
        ####
        Receipts = ttk.Frame(self.mainframe, width=600, height=600)

        # List of images and a single label to display all of them
        dictOfReceiptImages = {}

        for index, rpath in enumerate(self.listOfReceiptPaths):
            dictOfReceiptImages[index] = PhotoImage(file=rpath)

        imageLabel = ttk.Label(Receipts, image=dictOfReceiptImages[0])

        # Next button
        def nextPageFunction():
            nonlocal _pageNumber
            if _pageNumber >= (_totalPages - 1):
                return  # Page is the last
            _pageNumber += 1
            imageLabel["image"] = dictOfReceiptImages[_pageNumber]

        nextButton = ttk.Button(Receipts, text="Next", command=nextPageFunction)

        # Previous button
        def previousPageFunction():
            nonlocal _pageNumber
            if _pageNumber <= 0:
                return  # page is the first
            _pageNumber -= 1
            imageLabel["image"] = dictOfReceiptImages[_pageNumber]

        previousButton = ttk.Button(
            Receipts, text="Previous", command=previousPageFunction
        )

        ####
        # Grid all the widgets
        ####
        Receipts.grid()
        imageLabel.grid(column=0, row=0, columnspan=2, rowspan=2)
        previousButton.grid(column=0, row=1)
        nextButton.grid(column=1, row=1)

    @staticmethod
    def getListOfReceiptPaths() -> list:  # TODO Assumes there's images in the dir
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
