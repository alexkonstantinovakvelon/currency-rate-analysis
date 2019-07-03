from datetime import date


class Rate:
    def __init__(self, date: date, rate: float):
        self.date = date
        self.rate = rate
