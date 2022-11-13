'''Класс реализующий инвентарь персонажа'''
from modelsdungeon import *
class Character_Inventory:
    def __init__(self, user_id, count_slot=7):
        self.user_id = user_id
        self.slots = count_slot
        self.char_items = {"item1": None,
                           "item2": None,
                           "item3": None,
                           "item4": None,
                           "item5": None,
                           "item6": None,
                           "item7": None,
                           "item8": None,
                           "item9": None}

    def add_item(self, item):
        success = False
        usage_slots = 0
        # проверка на присутствие + попытка добавить
        if success == False:
            for i in self.char_items:
                if self.char_items[i] != None:
                    if self.char_items[i].item_id == item.item_id:
                        self.char_items[i].count += item.count
                        success = True
                        break
        # Предметов этого типа нет, тогда подсчитаем количество занятых слотов
        if success == False:
            for i in self.char_items:
                if self.char_items[i] != None:
                    usage_slots += 1
            # Если количество слотов позволяет, то запишем новый слот
            if usage_slots < self.slots:
                for i in self.char_items:
                    if self.char_items[i] == None:
                        self.char_items[i] = item
                        break
            else:
                print('место закончилось')

    def change_backpack(self):
        self.slots = 9

    def delete_item(self, item_id):
        for item in self.char_items:
            if self.char_items[item].item_id == item_id:
                self.char_items[item] = None

    #
    def decrement_count(self, item_id, count):
        for item in self.char_items:
            if self.char_items[item] is not None:
                if self.char_items[item].item_id == item_id:
                    self.char_items[item].count -= count

    def clean_zero_inventory(self):
        for ch_item in self.char_items:
            if self.char_items[ch_item] is not None:
                if self.char_items[ch_item].count == 0:
                    self.char_items[ch_item]=None
    # def get_item(self, id):
    #     item = GameItemsModel.get(id=id)
    #     return item

