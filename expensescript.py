from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import traceback
from PIL import Image, ImageTk
import os
from datetime import date, timedelta
from tkcalendar import Calendar
from enum import Enum
from typing import TypedDict
from pathlib import Path
import json


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
        windowIcon = PhotoImage(
            file="E:\\Coding\\expenseautomate\\awthemes-10.4.0\\expenseautomatelogo.png"
        )
        self.root.iconphoto(False, windowIcon)
        self.root.title("Expense Automate")
        self.root.tk.call("lappend", "auto_path", "./awthemes-10.4.0")
        self.root.tk.call("package", "require", "awdark")
        self.root.report_callback_exception = self.report_callback_exception

        self.s = ttk.Style()
        self.s.theme_use("awdark")

        self.mainframe = ttk.Frame(self.root, width=1000, height=800, padding=50)
        self.mainframe.grid()
        self.mainframe.grid_propagate(False)
        self.mainframe.grid_anchor("center")

        self.root.update_idletasks()  # If this isn't done, Receipts' Entry widget is not focussed lol
        self.listOfReceiptPaths = self.getListOfReceiptPaths()
        if not (self.listOfReceiptPaths):
            messagebox.showerror(
                "Error", "The selected directory does not contain supported image types"
            )
            self.root.destroy()
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

        def calenderNextButtonFunction():
            if len(calenderStartFinishDates) == 0:
                calenderStartFinishDates.append(calender.selection_get())
                expenseLabelText.set("Pick the final date of expenses")

            elif len(calenderStartFinishDates) == 1:
                if (
                    calender.selection_get() < calenderStartFinishDates[0]
                ):  # Second date is not valid
                    messagebox.showerror(
                        title="Expense Automate",
                        message=f"Please select a second date that proceeds {App.getStrDate(calenderStartFinishDates[0])}",
                    )
                    return

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

        calenderNextButton = ttk.Button(
            SelectDates, text="Next", command=calenderNextButtonFunction
        )

        def calenderBackButtonFunction():
            self.SelectDates()

        calenderBackButton = ttk.Button(
            SelectDates, text="Back", command=calenderBackButtonFunction
        )

        ####
        # Grid all the widgets
        ####
        SelectDates.grid()
        calender.grid(row=0, column=0, columnspan=2)
        expenseLabel.grid(row=1, column=0, columnspan=2)
        calenderBackButton.grid(row=2, column=0)
        calenderNextButton.grid(row=2, column=1)

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
        ReceiptsFrame = ttk.Frame(self.mainframe, width=600, height=600, padding=50)

        # List of images and a single label to display all of them
        dictOfReceiptImages = {}
        for index, rpath in enumerate(self.listOfReceiptPaths):
            dictOfReceiptImages[index] = ImageTk.PhotoImage(
                Image.open(fp=rpath).resize((600, 600))
            )

        imageLabel = ttk.Label(ReceiptsFrame, image=dictOfReceiptImages[0])

        DatesListboxLabelFrame = ttk.LabelFrame(
            ReceiptsFrame, text="Choose receipt date", padding=10
        )

        # Listbox for dates
        datesVar = StringVar(value=[str(x) for x in self.receiptDates])
        datesListbox = Listbox(DatesListboxLabelFrame, listvariable=datesVar, height=5)

        # Label Frame for radio buttons
        ReceiptsRadioButtonLabelFrame = ttk.LabelFrame(
            ReceiptsFrame, text="Choose receipt type", padding=10
        )

        # Radio button for meal type
        mealTypeVar = IntVar()
        breakfastRadioButton = ttk.Radiobutton(
            ReceiptsRadioButtonLabelFrame,
            text="Breakfast",
            variable=mealTypeVar,
            value=App.MealType.BREAKFAST.value,
        )
        dinnerRadioButton = ttk.Radiobutton(
            ReceiptsRadioButtonLabelFrame,
            text="Dinner",
            variable=mealTypeVar,
            value=App.MealType.DINNER.value,
        )

        # Label Frame for entry
        ReceiptsEntryLabelFrame = ttk.LabelFrame(
            ReceiptsFrame, text="Enter receipt total", padding=10
        )

        # Entry for receipt total
        receiptTotalVar = StringVar()
        receiptTotalEntry = ttk.Entry(
            ReceiptsEntryLabelFrame, textvariable=receiptTotalVar
        )

        # Next button
        def nextPageFunction():
            nonlocal _pageNumber
            try:
                datesListbox.curselection()[0]
            except IndexError:
                messagebox.showerror(
                    title="Expense Automate", message="Please select a date"
                )
                return

            try:
                assert float(receiptTotalEntry.get())
                assert float(receiptTotalEntry.get()) != 0
            except (ValueError, AssertionError):
                messagebox.showerror(
                    title="Expense Automate",
                    message="Please enter a valid receipt total",
                )
                return

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

        def backToSelectDatesFunction():
            self.SelectDates()

        backToSelectDatesButton = ttk.Button(
            ReceiptsFrame,
            text="Select dates",
            command=backToSelectDatesFunction,
        )

        bsLabel = ttk.Label(ReceiptsFrame, text="Input details")

        ####
        # Grid all the widgets
        ####
        ReceiptsFrame.grid()
        backToSelectDatesButton.grid(row=0, column=0)
        bsLabel.grid(row=0, column=4)

        imageLabel.grid(row=1, column=1, columnspan=3)

        ReceiptsRadioButtonLabelFrame.grid(row=2, column=1)
        breakfastRadioButton.grid()
        dinnerRadioButton.grid()

        DatesListboxLabelFrame.grid(row=2, column=2)
        datesListbox.grid()

        ReceiptsEntryLabelFrame.grid(column=3, row=2)
        receiptTotalEntry.grid(column=0, row=1)

        previousButton.grid(column=1, row=3)
        nextButton.grid(column=3, row=3)

    def Confirmation(self):
        self.clearMainframe()
        _finalReport: dict["date", App.FinalReportAttributes] = (
            self.generateExpenseReport(self.receiptsInformation, self.receiptDates)
        )
        _finalReportString = ""
        for eachDict in _finalReport:
            _finalReportString += (
                str(eachDict)
                + " had a breakfast total of £"
                + str(_finalReport[eachDict]["breakfastTotal"])
                + " and a dinner total of £"
                + str(_finalReport[eachDict]["dinnerTotal"])
                + "\n"
            )

        ####
        # Create widgets
        ####
        ConfirmationFrame = ttk.Frame(self.mainframe)

        confirmationLabel = ttk.Label(
            ConfirmationFrame,
            text="Confirm the entered details are correct. This will generate an expenses report along with renaming the receipt pictures to reflect their receipt total",
        )

        reportPrintedLabel = ttk.Label(ConfirmationFrame, text=f"{_finalReportString}")

        def writeToFileButtonFunction() -> None:
            self.writeExpenseReport(_finalReport)
            self.renameReceiptPictures(self.receiptsInformation)
            self.root.destroy()

        writeToFileButton = ttk.Button(
            ConfirmationFrame, text="Write to file", command=writeToFileButtonFunction
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
        reportPrintedLabel.grid(row=1, column=0, columnspan=2)
        goBackButton.grid(row=2, column=0)
        writeToFileButton.grid(row=2, column=1)

    @staticmethod
    def generateExpenseReport(
        receiptsInfo: dict[str, ReceiptsInfoAttributes], receiptDates: list["date"]
    ) -> dict[str, FinalReportAttributes]:

        finalReport: dict[str, App.FinalReportAttributes] = {
            App.getStrDate(eachDate): {
                "breakfastTotal": 0,
                "dinnerTotal": 0,
            }
            for eachDate in receiptDates
        }

        for eachReceiptInfo in receiptsInfo:
            if receiptsInfo[eachReceiptInfo]["mealType"] == 0:  # Breakfast
                finalReport[App.getStrDate(receiptsInfo[eachReceiptInfo]["date"])][
                    "breakfastTotal"
                ] += receiptsInfo[eachReceiptInfo]["receiptTotal"]
            else:  # Dinner
                finalReport[App.getStrDate(receiptsInfo[eachReceiptInfo]["date"])][
                    "dinnerTotal"
                ] += receiptsInfo[eachReceiptInfo]["receiptTotal"]

        return finalReport

    @staticmethod
    def writeExpenseReport(finalReport: dict["date", FinalReportAttributes]) -> None:
        with open("report.json", "w") as f:
            print(json.dumps(finalReport, indent=4), file=f)

    @staticmethod
    def renameReceiptPictures(receiptsInfo: dict[str, ReceiptsInfoAttributes]) -> None:
        counter = 1
        for eachReceiptPath in receiptsInfo:
            p = Path(eachReceiptPath)
            p.rename(
                p.with_stem(
                    f"{receiptsInfo[eachReceiptPath]['date']}_£{receiptsInfo[eachReceiptPath]['receiptTotal']:.2f}_{counter:04}"
                )
            )
            counter += 1

    @staticmethod
    def getListOfReceiptPaths() -> list:  # TODO Assumes there's images in the dir
        receiptDirectory = filedialog.askdirectory()
        fileList = os.listdir(receiptDirectory)
        listOfReceiptPaths = []
        validFormats = [".png", ".jpg", ".jpeg"]
        for file in fileList:
            if os.path.splitext(file)[1] in validFormats:
                listOfReceiptPaths.append(receiptDirectory + "/" + file)

        return listOfReceiptPaths

    @staticmethod
    def getStrDate(eachDate: "date") -> str:
        return f"{eachDate.day}/{eachDate.month}/{eachDate.year}"

    def report_callback_exception(self, *args):
        error = traceback.format_exception(*args)
        messagebox.showerror("Exception", error)

    def clearMainframe(self) -> None:
        for c in self.mainframe.winfo_children():
            c.destroy()


root = Tk()
App(root)
root.mainloop()
