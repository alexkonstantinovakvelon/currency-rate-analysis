class CurrencyCodes:
    __USD = 'R01235'
    __EUR = 'R01239'
    __GBP = 'R01035'
    __CHF = 'R01375'

    @staticmethod
    def get_code(currency_name: str) -> str:
        if currency_name == 'USD':
            return CurrencyCodes.__USD
        if currency_name == 'EUR':
            return CurrencyCodes.__EUR
        if currency_name == 'GBP':
            return CurrencyCodes.__GBP
        if currency_name == 'CHF':
            return CurrencyCodes.__CHF
        return None
