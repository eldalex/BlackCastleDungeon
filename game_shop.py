'''Игровой магазин и предметы'''
from game_items import Game_Items
from modelsdungeon import GameItemsModel


class Shop_item:
    def __init__(self, item_id, count, price):
        bd_item = GameItemsModel.get(item_id)
        self.id = item_id
        self.name = bd_item.item_name
        self.count = count
        self.price = price

    def decrement_item(self):
        self.count-=1



class Game_Shop:
    def __init__(self):
        self.shop_items = []

    def add_shop_item(self, item_id, count, price):
        shop_item = Shop_item(item_id, count, price)
        self.shop_items.append(shop_item)

    def check_count(self):
        for i in self.shop_items:
            if i.count == 0:
                self.shop_items.remove(i)

