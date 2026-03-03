from abc import ABC, abstractmethod
from typing import List


class StockObserver(ABC):
    @abstractmethod
    def update(self, stock: str, new_price: int) -> None:
        raise NotImplementedError


class Stock:
    def __init__(self, stock: str, price: int):
        self._stock = stock
        self._price = price
        self._observers: List[StockObserver] = []

    def attach(self, observer: StockObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: StockObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def set_price(self, price: int) -> None:
        self._price = price
        self.notify()

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._stock, self._price)


class PriceLogger(StockObserver):
    def update(self, stock: str, new_price: int) -> None:
        print(f"Price for {stock} updated to {new_price}")


class PriceAlert(StockObserver):
    def __init__(self):
        self._register = {}

    def set_stock_alert(self, stock: str, threshold: int) -> None:
        self._register[stock] = threshold

    def update(self, stock: str, new_price: int) -> None:
        if stock in self._register and new_price > self._register[stock]:
            print(
                f"Price for {stock} crossed threshold "
                f"{self._register[stock]} → New price: {new_price}"
            )


if __name__ == "__main__":
    apple = Stock("AAPL", 150)
    investor1 = PriceLogger()
    price_alert = PriceAlert()

    price_alert.set_stock_alert("AAPL", 230)

    apple.attach(investor1)
    apple.attach(price_alert)

    apple.set_price(180)  # notify observers
    apple.set_price(250)  # alert should trigger
