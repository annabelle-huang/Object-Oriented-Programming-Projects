import tkinter as tk
from tkinter import RIGHT, Y, W

class AccountButton(tk.Frame):
    "Class for creating an account button"
    def __init__(self, acct_list_frame, tlf, acct, bank, acct_button_list, new, gui, **kwargs):
        super().__init__(acct_list_frame, **kwargs) 
        if acct is not None:
            self._acct = acct
        if bank is not None:
            self._bank = bank
        self._gui = gui
        if new:
            self._button = tk.Radiobutton(self._gui.get_acct_list_frame(), text=acct, 
                                            value=self._acct.account_number, 
                                            command=lambda: self.select(acct, tlf))
            self._button.pack(anchor=W)
            acct_button_list.append(self._button) # append account button to list of buttons
    
    def select(self, acct, tlf):
        "select account and display updated transaction list"
        self._gui.set_selected_account(acct) 
        for widget in tlf.winfo_children(): # only display the listbox of the selected account
            widget.pack_forget()
        
        # display transaction list label
        self._list_label = tk.Label(tlf, text="Transaction list: ")
        self._list_label.pack()
        # create scrollbar for transaction list
        scrollbar = tk.Scrollbar(tlf)
        scrollbar.pack(side=RIGHT, fill=Y)
        # create transaction list
        self._list = tk.Listbox(tlf, height=7, width=20, yscrollcommand = scrollbar.set)
        self._list.pack()
        
        # checks whether a transaction is positive or negative and color codes the transaction
        l = acct.get_transactions()
        for i, x in enumerate(l):
            self._list.insert(i+1, x)
            if len(l) != 0:
                if x.get_amt() < 0:
                    self._list.itemconfig(i,bg= "red")
                else:
                    self._list.itemconfig(i, bg="green")
        self._list.pack()
        
    