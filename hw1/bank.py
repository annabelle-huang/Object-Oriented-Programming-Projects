from account import *
class Bank:
    def __init__(self):
        "instantiating bank object"
        self.numAccts = 0
        self.acctList = []
        self.currentAcct = "None"

    def openAcct(self):
        "appends an account object to the bank object's list of accounts"
        print("Type of account? (checking/savings)")
        it = input(">")
        if it == "checking":
            acct = Account(len(self.acctList) + 1, "Checking")
            self.acctList.append(acct)
        elif it == "savings":
            acct = Account(len(self.acctList) + 1, "Savings") 
            self.acctList.append(acct)

    def summary(self):
        "prints a summary of the existing accounts in the bank object's list of accounts"
        for x in self.acctList:
            f = "${:,.2f}".format(x.balance)
            if x.type == "Checking":
                print("Checking#" + str(x.num).zfill(9) + "," + f"\tbalance: {f}")
            elif x.type == "Savings":
                print("Savings#" + str(x.num).zfill(9) + "," + f"\tbalance: {f}")
            
