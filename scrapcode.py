import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Parent widget
Receipts = ttk.Frame(root)
Receipts.pack()

# StringVar for Entry
receiptTotalVar = tk.StringVar()

# Entry widget
receiptTotalEntry = ttk.Entry(Receipts, textvariable=receiptTotalVar, state=tk.NORMAL)
receiptTotalEntry.pack()

# Run the application
root.mainloop()
