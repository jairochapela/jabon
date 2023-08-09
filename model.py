from csv import DictReader

class EuroExchangeRate:

    rates = {'EUR': 1}

    def __init__(self, currency, rate):
        self.currency = currency
        self.rate = rate
        EuroExchangeRate.rates[currency] = self

    @staticmethod
    def get_rate(currency):
        if not currency in EuroExchangeRate.rates:
            raise ValueError("Invalid currency code %s" % currency)
        return EuroExchangeRate.rates[currency]
    
    @staticmethod
    def get_currencies():
        return EuroExchangeRate.rates.keys()
    
    @staticmethod
    def load_from_csv(file):
        with open(file, 'r') as f:
            reader = DictReader(f)
            for row in reader:
                for currency, rate in row.items():
                    currency = currency.strip()
                    if currency and currency != 'Date':
                        EuroExchangeRate.rates[currency] = float(rate)


# if __name__ == '__main__':
#     EuroExchangeRate.load_from_csv('eurofxref.csv')
#     print (EuroExchangeRate.get_rate('USD'))
#     print (EuroExchangeRate.get_rate('GBP'))
#     print (EuroExchangeRate.get_currencies())