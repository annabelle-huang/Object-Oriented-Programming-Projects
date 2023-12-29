class Transaction:
    def __init__(self, date, amount, manual):
        "instantiates transaction object"
        self._date = date
        self._amount = amount
        self._manual = manual

    def get_date(self):
        return self._date
    def get_amount(self):
        return self._amount
    def get_manual(self):
        return self._manual
    
    date = property(get_date)
    amount = property(get_amount)
    manual = property(get_manual)
