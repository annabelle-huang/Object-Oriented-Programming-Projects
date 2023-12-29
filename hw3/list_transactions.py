import tkinter as tk

class ListTransactions(tk.Frame):
    def __str__(self):
        return "ListTransactions"
    
    def __init__(self, parent, acct, **kwargs):
        super().__init__(parent, **kwargs) 
        if acct is not None:
            self._acct = acct
            
        self._list = tk.Listbox()
        
        self._list_transactions()
        
    def _list_transactions(self):
        for i, t in enumerate(self.master.get_transactions()):
            self._list.insert(i, t)