import sys
import pickle
import logging

import decimal
from decimal import Decimal, setcontext, BasicContext
from datetime import datetime

from bank import Bank
from customexceptions import OverdrawError, TransactionSequenceError, TransactionLimitError

# Macros for TransactionLimitError limit_type
DAILY = "daily"
MONTHLY = "monthly"

# formatting for logging
FORMAT = '%(asctime)s|%(levelname)s|%(message)s'
    
# context with ROUND_HALF_UP
setcontext(BasicContext)

class BankCLI:
    """Driver class for a command-line REPL interface to the Bank application"""

    def __init__(self):
        self._bank = Bank()

        # establishes relationship to Accounts
        self._selected_account = None

        self._choices = {
            "1": self._open_account,
            "2": self._summary,
            "3": self._select,
            "4": self._add_transaction,
            "5": self._list_transactions,
            "6": self._monthly_triggers,
            "7": self._save,
            "8": self._load,
            "9": self._quit,
        }

    def _display_menu(self):
        print(f"""--------------------------------
Currently selected account: {self._selected_account}
Enter command
1: open account
2: summary
3: select account
4: add transaction
5: list transactions
6: interest and fees
7: save
8: load
9: quit""")

    def run(self):
        """Display the menu and respond to choices."""

        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            # expecting a digit 1-9
            if action:
                action()
            else:
                # not officially part of spec since we don't give invalid options
                print("{0} is not a valid choice".format(choice))

    def _summary(self):
        # dependency on Account objects
        for x in self._bank.show_accounts():
            print(x)

    def _load(self):
        # log debug for loading bank
        logging.debug("Loaded from bank.pickle")
        with open("bank.pickle", "rb") as f:
            self._bank = pickle.load(f)
        # clearing the selected account so it doesn't get out of sync with the new account objects loaded from the pickle file
        self._selected_account = None

    def _save(self):
        # log debug for saving bank
        logging.debug("Saved to bank.pickle")
        with open("bank.pickle", "wb") as f:
            pickle.dump(self._bank, f)

    def _quit(self):
        sys.exit(0)

    def _add_transaction(self):
        # set default values for variables to check if transaction is acceptable
        valid_amount = False
        valid_date = False
        while valid_amount == False:
            # keep requesting for amount until user gives acceptable amount
            amount = input("Amount?\n>")
            try:
                amount = Decimal(amount) # convert to Decimal
                valid_amount = True # sets validity of amount to True
            except decimal.InvalidOperation:
                print("Please try again with a valid dollar amount.")
        while valid_date == False:
            # keep requesting for date until user gives acceptable date
            date = input("Date? (YYYY-MM-DD)\n>")
            try:
                date = datetime.strptime(date, "%Y-%m-%d").date() # convert to date
                valid_date = True # sets validity of date to True
            except ValueError:
                print("Please try again with a valid date in the format YYYY-MM-DD.")
        try:          
            self._selected_account.add_transaction(amount, date)
        except AttributeError:
            # handles attribute error where an account is not selected yet
            print("This command requires that you first select an account.")
        except OverdrawError:
            # handles a value error when the transaction makes the account balance zero
            print("This transaction could not be completed due to an insufficient account balance.")
        except TransactionSequenceError as error:
            # handles error when the input transaction is not in chronological order
            print("New transactions must be from", error.latest_date , "onward.")
        except TransactionLimitError as error:
            # handles error when the transaction limit is exceeded and determines what type of limit it is
            if error.type == MONTHLY:
                print("This transaction could not be completed because this account already has 5 transactions in this month.")
            if error.type == DAILY:
                print("This transaction could not be completed because this account already has 2 transactions in this day.")

    def _open_account(self):
        acct_type = input("Type of account? (checking/savings)\n>")
        self._bank.add_account(acct_type)

    def _select(self):
        num = int(input("Enter account number\n>"))
        self._selected_account = self._bank.get_account(num)

    def _monthly_triggers(self):
        # log a transaction for interest and fees
        logging.debug("Triggered interest and fees")
        try:
            self._selected_account.assess_interest_and_fees()
        except OverdrawError:
            # handles a value error when there is not enough balance to do an interest and fees transaction
            print("This transaction could not be completed due to an insufficient account balance.")
        except TransactionSequenceError as error:
            # handles an error when user requests interest and fees transaction for the second time in a month
            print("Cannot apply interest and fees again in the month of " + error.latest_date + ".")

    def _list_transactions(self):
        for t in self._selected_account.get_transactions():
            print(t)

try:
    if __name__ == "__main__":
        #configures log
        logging.basicConfig(filename='bank.log', format=FORMAT, datefmt= '%Y-%m-%d %H:%M:%S' ,level=logging.DEBUG)
        BankCLI().run()
except Exception as error:
    # handles non-system errors that weren't already handled
    print("Sorry! Something unexpected happened. Check the logs or contact the developer for assistance.")
    # logs the error
    logging.error(type(error).__name__ + ": " + str(error)) 
    exit()
