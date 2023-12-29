from decimal import *
import pickle 
from bank import *
class BankCLI:
    def __main__():
        setcontext(Context(prec = 28, rounding = ROUND_HALF_UP))
        _bank = Bank()
        ci = -1
        date = ""
        while 1:
            print("--------------------------------")
            if _bank.currentAcct == "None": # if an account hasn't been selected yet
                print('Currently selected account: None')
            else:
                _bank.currentAcct = _bank.acctList[ci].type + "#" + str(_bank.acctList[ci].num).zfill(9) +",\tbalance: $" + str("{:,.2f}".format(_bank.acctList[ci].balance))
                print(f'Currently selected account: {_bank.currentAcct}')
            print('Enter command\n1: open account'
            '\n2: summary\n3: select account\n4: add transaction'
            '\n5: list transactions\n6: interest and fees\n7: save\n8: load\n9: quit')
            i = input(">")
            match i:
                case "1": # if the user selects to open account, call the openAcct() method
                    _bank.openAcct()
                case "2": # if the user selects summary, call the summary() method
                    _bank.summary()
                case "3": # if the user selects "select account", ask for input and change the current account selection
                    print("Enter account number")
                    ci = int(input(">")) - 1
                    _bank.currentAcct = _bank.acctList[ci].type + "#" + str(_bank.acctList[ci].num).zfill(9) +",\tbalance: $" + str("{:,.2f}".format(_bank.acctList[ci].balance))
                case "4": # if the user selects add transaction, ask for amount and date and call addTrans() method
                    print("Amount?")
                    amount = input(">")
                    print("Date? (YYYY-MM-DD)")
                    date = input(">")
                    if _bank.acctList[ci].type == "Checking":
                        CheckingAccount.addTrans(_bank.acctList[ci], str(date), Decimal(amount), True)
                    else:
                        SavingsAccount.addTrans(_bank.acctList[ci], str(date), Decimal(amount), True)
                case "5": # if the user selects list transactions, call the listTrans() method
                    _bank.acctList[ci].listTrans()
                case "6": # if the user selects interst and fees, set the interest transaction 
                          # date as the last date of the latest transaction and calls addInterest() method
                    date = _bank.acctList[ci].transList[-1].date
                    if _bank.acctList[ci].type == "Checking":
                        CheckingAccount.addInterest(_bank.acctList[ci], date)
                    else:
                        SavingsAccount.addInterest(_bank.acctList[ci], date)
                case "7": # if the user selects the save option, save the bank object to file
                    file = open("file.txt", "wb")
                    pickle.dump(_bank, file)
                    file.close()
                case "8": # if the user selects load, load the bank object from file
                    file = open("file.txt", "rb")
                    _bank = pickle.load(file)
                    file.close()
                    _bank.currentAcct = "None"
                case "9": # if the user selects quit, exit the program
                    exit()

BankCLI.__main__()