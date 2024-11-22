from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
from datetime import date, datetime, timedelta
from tkcalendar import Calendar
from enum import Enum
from typing import TypedDict
from pathlib import Path
import random


class App:
    class MealType(Enum):
        BREAKFAST = 0
        DINNER = 1

    class ReceiptsInfoAttributes(TypedDict):
        date: "date"
        receiptTotal: float
        mealType: int

    class FinalReportAttributes(TypedDict):
        breakfastTotal: float
        dinnerTotal: float

    def __init__(self, root) -> None:
        self.root: "Tk" = root
        self.root.title("Expense Automate")

        # self.style = ttk.Style()
        # self.style.configure(
        #     "Blue.TFrame", background="blue", borderwidth=5, relief="raised"
        # )

        self.mainframe = ttk.Frame(self.root, width=600, height=600, padding=50)
        self.mainframe.grid()

        self.root.update_idletasks()  # If this isn't done, Receipts' Entry widget is not focussed lol
        self.listOfReceiptPaths = self.getListOfReceiptPaths()
        self.SelectDates()

    def SelectDates(self) -> None:
        self.clearMainframe()
        self.receiptDates: list["date"] = []

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
        calenderStartFinishDates: list["date"] = []

        def calenderNextSelectionFunction():
            if len(calenderStartFinishDates) == 0:
                calenderStartFinishDates.append(calender.selection_get())
                expenseLabelText.set("Pick the final date of expenses")

            elif len(calenderStartFinishDates) == 1:
                calenderStartFinishDates.append(calender.selection_get())
                self.receiptDates = [
                    calenderStartFinishDates[0] + timedelta(days=x)
                    for x in range(
                        (
                            calenderStartFinishDates[1]
                            + timedelta(days=1)
                            - calenderStartFinishDates[0]
                        ).days
                    )
                ]
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
        self.receiptsInformation: dict[str, App.ReceiptsInfoAttributes] = {
            receiptPath: {} for receiptPath in self.listOfReceiptPaths
        }
        _pageNumber = 0
        _totalPages = len(self.listOfReceiptPaths)

        ####
        # Create widgets
        ####
        ReceiptsFrame = ttk.Frame(self.mainframe, width=600, height=600)

        # List of images and a single label to display all of them
        dictOfReceiptImages = {}
        for index, rpath in enumerate(self.listOfReceiptPaths):
            dictOfReceiptImages[index] = PhotoImage(file=rpath)
        imageLabel = ttk.Label(ReceiptsFrame, image=dictOfReceiptImages[0])

        # Listbox for dates
        datesVar = StringVar(value=[str(x) for x in self.receiptDates])
        datesListbox = Listbox(ReceiptsFrame, listvariable=datesVar)

        # Radio button for meal type
        mealTypeVar = IntVar()
        breakfastRadioButton = ttk.Radiobutton(
            ReceiptsFrame,
            text="Breakfast",
            variable=mealTypeVar,
            value=App.MealType.BREAKFAST.value,
        )
        dinnerRadioButton = ttk.Radiobutton(
            ReceiptsFrame,
            text="Dinner",
            variable=mealTypeVar,
            value=App.MealType.DINNER.value,
        )
        # Entry for receipt total
        receiptTotalVar = StringVar()
        receiptTotalEntry = ttk.Entry(ReceiptsFrame, textvariable=receiptTotalVar)

        # TODO Errors if there's only 1 picture
        # Next button
        def nextPageFunction():
            nonlocal _pageNumber
            if _pageNumber >= (_totalPages - 1):
                self.receiptsInformation[self.listOfReceiptPaths[_pageNumber]] = {
                    "date": self.receiptDates[datesListbox.curselection()[0]],
                    "receiptTotal": float(receiptTotalEntry.get()),
                    "mealType": mealTypeVar.get(),
                }
                self.Confirmation()
                return
            self.receiptsInformation[self.listOfReceiptPaths[_pageNumber]] = {
                "date": self.receiptDates[datesListbox.curselection()[0]],
                "receiptTotal": float(receiptTotalEntry.get()),
                "mealType": mealTypeVar.get(),
            }
            _pageNumber += 1
            imageLabel["image"] = dictOfReceiptImages[_pageNumber]

        nextButton = ttk.Button(ReceiptsFrame, text="Next", command=nextPageFunction)

        # Previous button
        def previousPageFunction():
            nonlocal _pageNumber
            if _pageNumber <= 0:
                return  # page is the first
            _pageNumber -= 1
            imageLabel["image"] = dictOfReceiptImages[_pageNumber]

        previousButton = ttk.Button(
            ReceiptsFrame, text="Previous", command=previousPageFunction
        )

        ####
        # Grid all the widgets
        ####
        ReceiptsFrame.grid()
        imageLabel.grid(column=0, row=0, columnspan=4)
        breakfastRadioButton.grid(column=0, row=1)
        dinnerRadioButton.grid(column=1, row=1)
        datesListbox.grid(column=2, row=1)
        receiptTotalEntry.grid(column=3, row=1)
        previousButton.grid(column=0, row=2)
        nextButton.grid(column=3, row=2)

    def Confirmation(self):
        self.clearMainframe()

        ####
        # Create widgets
        ####
        ConfirmationFrame = ttk.Frame(self.mainframe)

        confirmationLabel = ttk.Label(
            ConfirmationFrame,
            text="Confirm the entered details are correct. This will generate an expenses report along with renaming the receipt pictures to reflect their receipt total",
        )

        def confirmButtonFunction() -> None:
            self.writeExpenseReport(
                self.generateExpenseReport(self.receiptsInformation, self.receiptDates)
            )
            self.renameReceiptPictures(self.receiptsInformation)
            self.root.destroy()

        confirmButton = ttk.Button(
            ConfirmationFrame, text="Confirm", command=confirmButtonFunction
        )

        def goBackButtonFunction() -> None:
            self.Receipts()

        goBackButton = ttk.Button(
            ConfirmationFrame, text="Go back", command=goBackButtonFunction
        )

        ####
        # Grid all the widgets
        ####
        ConfirmationFrame.grid()
        confirmationLabel.grid(row=0, column=0, columnspan=2)
        goBackButton.grid(row=1, column=0)
        confirmButton.grid(row=1, column=1)

    @staticmethod
    def generateExpenseReport(
        receiptsInfo: dict[str, ReceiptsInfoAttributes], receiptDates: list["date"]
    ) -> dict["date", FinalReportAttributes]:
        finalReport: dict["date", App.FinalReportAttributes] = {
            eachDate: {"breakfastTotal": 0, "dinnerTotal": 0}
            for eachDate in receiptDates
        }

        for eachReceiptInfo in receiptsInfo:
            if receiptsInfo[eachReceiptInfo]["mealType"] == 0:  # Breakfast
                finalReport[receiptsInfo[eachReceiptInfo]["date"]][
                    "breakfastTotal"
                ] += receiptsInfo[eachReceiptInfo]["receiptTotal"]
            else:  # Dinner
                finalReport[receiptsInfo[eachReceiptInfo]["date"]][
                    "dinnerTotal"
                ] += receiptsInfo[eachReceiptInfo]["receiptTotal"]

        return finalReport

    @staticmethod
    def writeExpenseReport(finalReport: dict["date", FinalReportAttributes]) -> None:
        with open("report.txt", "w") as f:
            for eachDict in finalReport:
                print(f"{eachDict}, {finalReport[eachDict]}", file=f)

    @staticmethod
    def renameReceiptPictures(receiptsInfo: dict[str, ReceiptsInfoAttributes]) -> None:
        for eachReceiptPath in receiptsInfo:
            p = Path(eachReceiptPath)
            p.rename(
                p.with_stem(
                    f"{receiptsInfo[eachReceiptPath]['date']}_£{receiptsInfo[eachReceiptPath]['receiptTotal']}_{random.randint(1000,9999)}"
                )
            )

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
