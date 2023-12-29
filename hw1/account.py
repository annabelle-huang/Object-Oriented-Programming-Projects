from transactions import Transaction
from decimal import *
class Account:
    def __init__(self, num, type):
        "instantiating account object"
        self._num = num
        self._type = type
        self._balance = 0
        self.transList = []

    def get_num(self):
        return self._num
    def get_type(self):
        return self._type
    def get_balance(self):
        return self._balance
    
    def set_balance(self, x):
        self._balance = x
    
    num = property(get_num)
    type = property(get_type)
    balance = property(get_balance, set_balance)

    def addTrans(self, date, amount, manual):
        "appends a Transaction object to the transaction list of the self object"
        self.transList.append(Transaction(date, amount, manual))

    def listTrans(self):
        "lists the list of transactions in sorted string order"
        self.transList.sort(key=lambda t: t.date)
        for x in self.transList:
            print(x.date + ", $" + str("{:,.2f}".format(x.amount)))

class CheckingAccount(Account):
    def addTrans(self, date, amount, manual): 
        "overrides the addTrans method from parent class and"
        "checks for checking account withdrawal restrictions"
        if self._balance + amount >= 0:
            self._balance = self._balance + amount
            self.transList.append(Transaction(date, amount, manual))
        else:
            if self._balance < self._balance + amount:
                self._balance = self._balance + amount
                self.transList.append(Transaction(date, amount, manual))

    def addInterest(self, date):
        "calculates interest and determines the transaction's date"
        "and appends the interest transaction to the transaction list of the self object"
        interest = self._balance * Decimal(0.0008)
        if list(date)[5] == "0": # determines the date of the interest transaction
            m = list(date)[6]
            if m == "4" or m == "6" or m == "9":
                feesDate = "30"
            elif m != "2":
                feesDate = "31"
            else:
                y = int(date[0:4])
                if (y % 4 == 0 and y % 100 == 0 and y % 100 == 0) or (y % 4 == 0 and y % 100 != 0):
                    feesDate = "29"
                else:
                    feesDate = "28"
        else:
            if int(date[5:7]) == 11:
                feesDate = "30"
            else:
                feesDate = "31"
        self.addTrans(date[0:4] + '-' + date[5:7] + '-' + feesDate, interest, False)
        if self._balance < 100:
            self.addTrans(date[0:4] + '-' + date[5:7] + '-' + feesDate, - Decimal(5.44), False)
            self._balance = self._balance + interest - Decimal(5.44)
        else: 
            self._balance = self._balance + interest 
            
class SavingsAccount(Account):
    def addTrans(self, date, amount, manual): 
        "overrides the addTrans method from parent class and"
        "checks for savings account withdrawal limits"
        dateNum = 0
        monthNum = 0
        for x in self.transList:
            if x.manual: 
                if date == x.date: # twice a day
                    dateNum = dateNum + 1
                if date[5:7] == x.date[5:7]:
                    monthNum = monthNum + 1
        if dateNum < 2 and monthNum < 5:
            self.transList.append(Transaction(date, amount, manual))
            self._balance = self._balance + amount

    def addInterest(self, date):
        "calculates interest and determines the transaction's date"
        "and appends the interest transaction to the transaction list of the self object"
        interest = self._balance * Decimal(0.0041)
        if list(date)[5] == "0":  # determines the date of the interest transaction
            m = list(date)[6]
            if m == "4" or m == "6" or m == "9":
                feesDate = "30"
            elif m != "2":
                feesDate = "31"
            else:
                y = int(date[0:4])
                if (y % 4 == 0 and y % 100 == 0 and y % 100 == 0) or (y % 4 == 0 and y % 100 != 0):
                    feesDate = "29"
                else:
                    feesDate = "28"
        else:
            if int(date[5:7]) == 11:
                feesDate = "30"
            else:
                feesDate = "31"
        self.addTrans(date[0:4] + '-' + date[5:7] + '-' + feesDate, interest, False)
        self._balance = self._balance + interest 