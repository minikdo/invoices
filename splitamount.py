import sys


class SplitAmount:

    integral: int = 0
    fraction: int = 0

    def __init__(self, amount: float):
        self.amount = amount
        try:
            self.integral = self.get_integral()
            self.fraction = self.get_fraction()
        except ValueError as error:
            print(error, file=sys.stderr)

    def get_fraction(self) -> int:
        fraction: float = self.amount - int(self.amount)
        return int(round(fraction, 2)*10*10)

    def get_integral(self) -> int:
        return int(self.amount)

    def get_full_amount(self) -> int:
        return self.integral*100 + self.fraction
