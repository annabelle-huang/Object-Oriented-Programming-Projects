# Operating System: MacOS
# Name: Annabelle Huang
# Professor: Tim Barron
# Class: CPSC 327

import tkinter as tk
from tkinter import ttk
import sys
from tkmacosx import Button
import tkcalendar

from tkinter import messagebox, NW, NE, DISABLED, NORMAL, W
import logging
from decimal import Decimal, setcontext, BasicContext
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from bank import Bank
from transactions import Base
from exceptions import OverdrawError, TransactionLimitError, TransactionSequenceError
from account_button import AccountButton

SAVINGS = "savings"
CHECKING = "checking"


setcontext(BasicContext)

logging.basicConfig(filename='bank.log', level=logging.DEBUG,
                    format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class BankGUI:
    "GUI for class Bank"
    def __str__(self):
        return "BankGUI"
        
    def __init__(self):
        "initializer for BankGUI: creates main window, frames that holds buttons and other widgets"
        self._session = Session()
        self._bank = self._session.query(Bank).first()
        logging.debug("Loaded from bank.db")
        if not self._bank:
            self._bank = Bank()
            self._session.add(self._bank)
            self._session.commit()
            logging.debug("Saved to bank.db")
        
        self._window = tk.Tk()
        self._window.report_callback_exception = self.handle_exception
        self._window.title("THE BEST BANK")
        self._window.geometry("725x600")
        
        # options frame that contains buttons to create an account, 
        # add transaction, and trigger interest and fees
        self._options_frame = tk.Frame(self._window) 
        # frame for additional options once open account and add transaction buttons are pressed
        self._lower_options_frame = tk.Frame(self._options_frame) 
        self._open_account_button = Button(self._options_frame, text="Open Account", # button to open new account
                  command=lambda:self._open_account(), bg="#4ebfac")
        self._add_transaction_button = Button(self._options_frame, text="Add Transactions", # button to add transaction (to selected account)
                  command=lambda:self._add_transaction(), bg="#4ebfac")
        self._interest_button = Button(self._options_frame, text="Interest and Fees", #button to trigger interest and fees (on selected account)
                  command=lambda:self._monthly_triggers(), bg="#4ebfac")
        
        # changes the colors of option frame buttons when mouse hovers over it
        self._open_account_button.bind("<Enter>", func=lambda e: self._open_account_button.config(
        bg="#6effe7"))
        self._open_account_button.bind("<Leave>", func=lambda e: self._open_account_button.config(
        bg="#4ebfac"))
        self._add_transaction_button.bind("<Enter>", func=lambda e: self._add_transaction_button.config(
        bg="#6effe7"))
        self._add_transaction_button.bind("<Leave>", func=lambda e: self._add_transaction_button.config(
        bg="#4ebfac"))
        self._interest_button.bind("<Enter>", func=lambda e: self._interest_button.config(
        bg="#6effe7"))
        self._interest_button.bind("<Leave>", func=lambda e: self._interest_button.config(
        bg="#4ebfac"))
        
        # grid and formatting of the options frame buttons
        self._open_account_button.grid(row=1, column=1, ipadx=10, ipady=10, padx=30) 
        self._add_transaction_button.grid(row=1, column=2, ipadx=10, ipady=10, padx=30)
        self._interest_button.grid(row=1, column=3, ipadx=10, ipady=10, padx=30)
        
        self._transactions_list_frame = tk.Frame(self._window) # frame for transactions list
        self._acct_list_frame = tk.Frame(self._window) # frame for list of accounts
        self._acct_list_frame.grid(row=1, column=1, columnspan=1, sticky=NE)
        
        self._options_frame.grid(row=0, column=1, columnspan=2, padx=30, pady=20) # grid for options frame
        self._lower_options_frame.grid(row=2, column=1, columnspan=2) # grid for lower options, which in
        
        self._selected_account = None
        
        self._transactions_list_frame.grid(row=1, column=2, columnspan=1, sticky=NW) # grid for transaction list frame
        self._acct_button_list = [] # list of created account buttons
        
        # shows all the accounts in list, assign _select command to each account button
        for x in self._bank.show_accounts():
            _acct_button = tk.Radiobutton(self._acct_list_frame, text=x, 
                                    value=x.account_number, 
                                    command=lambda a=x: 
                                    self._select(a, self._transactions_list_frame))
            _acct_button.pack(anchor=W)
            self._acct_button_list.append(_acct_button)
            
        self._window.mainloop()
    
    def _select(self, acct, tlf):
        "method to select the account"
        self._selected_account = acct
        AccountButton(self._acct_list_frame, tlf, acct, 
                      self._bank, self._acct_button_list, False,
                      self).select(acct, tlf)
        
    def _destroy_lower(self):
        "clears the lower options frame widgets"
        self._lower_options_frame.destroy()
        self._lower_options_frame = tk.Frame(self._options_frame)
        self._lower_options_frame.grid(row=2, column=1, columnspan=2)
                
    def _open_account(self): 
        "Open new account and append an AccountButton to end of account list"
        
        self._destroy_lower()
        # re-enable the account list buttons for user to choose
        for radio_button in self._acct_button_list:
                radio_button.config(state = NORMAL)
        
        # create open account account type selection dropdown widget
        acct_type_selected = tk.StringVar(self._lower_options_frame)
        acct_type_selected.set("select account type") # default open account selection value
        self._acct_type = tk.OptionMenu(self._lower_options_frame, acct_type_selected, "savings", "checking")
        self._acct_type.grid(row=2, column=1, pady=20)
        
        # confirm type of account selected to open account
        def confirm():
            if acct_type_selected.get() == SAVINGS: # create savings account
                self._bank.add_account(SAVINGS, self._session)
                AccountButton(self._acct_list_frame, self._transactions_list_frame, 
                                self._bank.show_accounts()[-1], self._bank, self._acct_button_list, True, self)
            elif acct_type_selected.get() == CHECKING: # create checking account
                self._bank.add_account(CHECKING, self._session)
                AccountButton(self._acct_list_frame, self._transactions_list_frame, 
                        self._bank.show_accounts()[-1], self._bank, self._acct_button_list, True, self)
            self._destroy_lower() # clear the lower frame widgets
            
        # create confirm and cancel button widgets for opening an account
        self._confirm_button = tk.Button(self._lower_options_frame, text="Confirm", command=lambda:confirm())
        self._cancel_button = tk.Button(self._lower_options_frame, text="Cancel", command=lambda:self._destroy_lower())
        self._confirm_button.grid(row=2, column=2, pady=20)
        self._cancel_button.grid(row=2, column=3, pady=20)
         
        
    def _is_valid(self, P): 
        "Checks if the input dollar amount is valid"
        counter = 0
        for i, x in enumerate(P):
            if len(P) != 0:
                # Enable enter button as long as user has inputted some decimal for amount entry
                # since validator already checks for invalid characters and does not let user input it
                self._enter_button.config(state = NORMAL) 
                if x == ".":
                    counter = counter + 1
                    if counter > 1:
                        return False
                elif x == "-" and i != 0:
                    return False
                elif x.isdecimal() == False and x != "-":
                    return False
        return True
                     
    def _add_transaction(self):
        "Add transaction to selected account"
        # warns user to select an account before adding a 
        # transaction as long long there is no currently selected account
        if self._selected_account is None: 
            messagebox.showwarning(title=None, message="This command requires that you first select an account.")
        else:
            # once an account is selected and user requests add transaction
            # disable all other account buttons to prevent mixup
            for radio_button in self._acct_button_list:
                radio_button.config(state = DISABLED)

            def cancel():
                "Clears the lower options frame widgets and re-enables the account buttons for selection"
                self._destroy_lower()
                for radio_button in self._acct_button_list:
                    radio_button.config(state = NORMAL)
            
            self._destroy_lower()
            
            # creates labels for add transaction buttons
            amount_label = tk.Label(self._lower_options_frame, text="Amount: ")
            date_label = tk.Label(self._lower_options_frame, text="Date: ")
            is_valid = self._lower_options_frame.register(self._is_valid)
            self._amount_entry = tk.Entry(self._lower_options_frame, validate='all', validatecommand=(is_valid, '%P'))
            
            # 3rd party styling
            style = ttk.Style(self._lower_options_frame)
            style.theme_use('clam')
            
            # date picker calendar for date of transaction and calendar styling
            cal = tkcalendar.Calendar(self._lower_options_frame, selectmode = 'day',
                                    date_pattern="yyyy-mm-dd", showweeknumbers=False, 
                                    foreground='black', weekendforeground="black",
                                    selectbackground="#c95f8d", background="#ffdbed")
            cal.grid(row=3, column=1, pady=10, columnspan=1)
            
            # grid for lower frame options buttons and grid
            cancel_button = tk.Button(self._lower_options_frame, text="Cancel", command=lambda :  cancel())
            amount_label.grid(row=2, column=0, pady=10)
            date_label.grid(row=3, column=0)
            self._amount_entry.grid(row=2, column=1)
            cancel_button.grid(row=2, column=3)
            self._enter_button = tk.Button(self._lower_options_frame, text="Enter", command=lambda : enter())
            self._enter_button.config(state = DISABLED, disabledforeground="#292929")
            self._enter_button.grid(row=2, column=2)
                
            def enter():
                "Try to add transaction to selected account once the enter button is clicked"
                try:
                    self._selected_account.add_transaction(Decimal(self._amount_entry.get()), 
                                                        datetime.strptime(cal.get_date(), 
                                                            "%Y-%m-%d").date(), self._session)
                    AccountButton(self._acct_list_frame, self._transactions_list_frame,
                                self._selected_account, self._bank, self._acct_button_list, False, self).select(
                                    self._selected_account, self._transactions_list_frame)
                    # returns to original menu state by clearing lower frame options and 
                    # enabling account buttons after successful transaction
                    cancel() 
                except TransactionSequenceError as ex:
                    messagebox.showwarning(title=None, message=
                                        f"New transactions must be from {ex.latest_date} onward.")
                except ValueError:
                    messagebox.showwarning(title=None, message=
                                        "Please try again with a valid date in the format YYYY-MM-DD.")
                except OverdrawError:
                    messagebox.showwarning(title=None, message=
                        "This transaction could not be completed due to an insufficient account balance.")
                except TransactionLimitError as ex:
                    messagebox.showwarning(title=None, message=f"This transaction could not be completed because this account already has {ex.limit} transactions in this {ex.limit_type}.")

    def _monthly_triggers(self):
        "Method is called when user requests for a interest and fees transaction on selected account"
        try:
            # tries append interest and fees transaction(s) 
            self._selected_account.assess_interest_and_fees(self._session)
            AccountButton(self._acct_list_frame, self._transactions_list_frame, 
                          self._selected_account, self._bank, self._acct_button_list, False, self).select(self._selected_account, 
                        self._transactions_list_frame)
            logging.debug("Triggered interest and fees")
            logging.debug("Saved to bank.db")
        except AttributeError:
            messagebox.showwarning(title=None,message=
                "This command requires that you first select an account.")
        except TransactionSequenceError as e:
            messagebox.showwarning(title=None, message=
                f"Cannot apply interest and fees again in the month of {e.latest_date.strftime('%B')}.")
        except ValueError:
            messagebox.showwarning(title=None,message=
                "This transaction could not be completed due to an insufficient account balance.")
        
    def set_selected_account(self, s):
        "Sets the selected account to be equal to given parameter"
        self._selected_account = s
        
    def get_selected_account(self):
        "Return the currently selected account"
        return self._selected_account 
    
    def get_acct_list_frame(self):
        "Return the account list frame"
        return self._acct_list_frame
    
    def handle_exception(exception, value, traceback):
        "defines a callback function that handles exceptions"
        messagebox.showwarning("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
        logging.error(f"{exception.__name__}: {repr(value)}")
        sys.exit(0)
    
if __name__ == "__main__":
    # connect to the database
    try:
        engine = create_engine(f"sqlite:///bank.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        BankGUI()
    except Exception as e:
        print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
        logging.error(str(e.__class__.__name__) + ": " + repr(str(e)))
        sys.exit(0)
