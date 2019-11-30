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

        self.gap = self.steam_predict_price - self.price
        self.gap_percent = self.gap * 1.0 / self.price
        self.time = TIMESTAMP

    def detail(self):
        return "{}: {}(steam) - {}(buff) = {}(beyond {:.2%}). when {}. steam url:{}"\
            .format(self.name, self.steam_predict_price, self.price, self.gap, self.gap_percent, self.time, self.steam_url)

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
            "time": self.time
        }
        return item_dict
