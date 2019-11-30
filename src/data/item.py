import statistics

from src.config.definitions import TIMESTAMP


class Item:

    def __init__(self, buff_id, name, price, sell_num, steam_url, steam_predict_price, buy_max_price):
        self.id = buff_id
        self.name = name
        self.price = float(price)
        self.sell_num = int(sell_num)
        self.steam_url = steam_url
        self.steam_predict_price = float(steam_predict_price)
        self.buy_max_price = float(buy_max_price)

        # be overridden later with real history price
        self.gap = self.steam_predict_price - self.price
        self.gap_percent = self.gap * 1.0 / self.price
        self.crawl_time = TIMESTAMP

        # set history price later
        self.history_prices = []
        self.history_sold = 0
        self.history_days = 0
        self.average_sold_price = 0

    def set_history_prices(self, prices, days):
        self.history_prices = prices
        self.history_sold = len(prices)
        self.history_days = days
        self.average_sold_price = self.centered_average(prices)
        self.gap = self.average_sold_price - self.price
        self.gap_percent = self.gap * 1.0 / self.price

    def detail(self):
        return "{}: {}(steam average sold price) - {}(buff) = {}(beyond {:.2%}). Sold {} items in {} days.\n steam url:{}"\
            .format(self.name, self.average_sold_price, self.price, self.gap, self.gap_percent, self.history_sold, self.history_days, self.steam_url)

    def to_dict(self):
        item_dict = {
            # id is index, not content column
            # "id": self.id,
            "name": self.name,
            "price": self.price,
            "sell_num": self.sell_num,
            "steam_url": self.steam_url,
            "steam_predict_price": self.steam_predict_price,
            "buy_max_price": self.buy_max_price,
            "gap": self.gap,
            "gap_percent": self.gap_percent,
            "crawl_time": self.crawl_time,
            "history_prices": self.history_prices,
            "history_sold": self.history_sold,
            "history_days": self.history_days,
            "average_sold_price": self.average_sold_price
        }
        return item_dict

    @staticmethod
    def centered_average(numbers):
        if len(numbers) > 2:
            return (sum(numbers) - max(numbers) - min(numbers)) / (len(numbers) - 2)
        else:
            return statistics.mean(numbers)
