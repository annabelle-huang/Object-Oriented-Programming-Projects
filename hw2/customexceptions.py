class OverdrawError(Exception):
    "Custom error class for when transaction makes balance negative"
    pass

class TransactionSequenceError(Exception):
    "Custom error class for when the transaction is not in chronological order"
    def __init__(self, latest_date):
        self.latest_date = latest_date

class TransactionLimitError(Exception):
    "Custome error class for when the transaction exceeds daily and monthly account limits on SavingsAccounts"
    def __init__(self, limit_type):
        self.type = limit_type
        
    