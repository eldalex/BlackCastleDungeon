import random
import json
import peewee
from peewee import *
from modelsdungeon import *

user_id = 1606686846
start_stats = {2: {"agility": 8, "strange": 22, "charm": 8},
               3: {"agility": 10, "strange": 20, "charm": 6},
               4: {"agility": 12, "strange": 6, "charm": 5},
               5: {"agility": 9, "strange": 8, "charm": 18},
               6: {"agility": 11, "strange": 20, "charm": 6},
               7: {"agility": 9, "strange": 20, "charm": 7},
               8: {"agility": 10, "strange": 16, "charm": 7},
               9: {"agility": 8, "strange": 24, "charm": 7},
               10: {"agility": 9, "strange": 22, "charm": 6},
               11: {"agility": 10, "strange": 18, "charm": 7},
               12: {"agility": 11, "strange": 20, "charm": 5}}


class Game_Items:
    def __init__(self, item_id, name, count=1):
        self.item_id = item_id
        self.name = name
        self.count = count
        self.empty = False

    def increase_count(self):
        self.count += 1

    def decrease_count(self):
        self.count -= 1
        if self.count <= 0:
            self.empty = True


class Character_Inventory:
    def __init__(self, user_id, count_slot=7):
        self.user_id = user_id
        self.slots = count_slot
        self.char_items = {"item1":None,
                           "item2":None,
                           "item3":None,
                           "item4":None,
                           "item5":None,
                           "item6":None,
                           "item7":None,
                           "item8":None,
                           "item9":None}
        # self.item1 = None
        # self.item2 = None
        # self.item3 = None
        # self.item4 = None
        # self.item5 = None
        # self.item6 = None
        # self.item7 = None
        # self.item8 = None
        # self.item9 = None

    def add_item(self, item):
        for i in self.char_items:
            if self.char_items[i]!=None:
                if self.char_items[i]["item_id"]==item.item_id:
                    self.char_items[i]["count"]+=item.count
                    break
            else:
                self.char_items[i]={"item_id":item.item_id,"count":item.count}
                break

        #
        # if self.item1 != None:
        #     if self.item1.item_id == item.item_id:
        #         self.item1.count+=item.count
        # elif self.item1 == None:
        #     self.item1 = item
        # elif self.item2 == None:
        #     self.item2 = item
        # elif self.item3 == None:
        #     self.item3 = item
        # elif self.item4 == None:
        #     self.item4 = item
        # elif self.item5 == None:
        #     self.item5 = item
        # elif self.item6 == None:
        #     self.item6 = item
        # elif self.item7 == None:
        #     self.item7 = item
        # elif self.slots == 9 and self.item8 == None:
        #     self.item8 = item
        # elif self.slots == 9 and self.item9 == None:
        #     self.item9 = item

    def get_item(self, id):
        item = GameItemsModel.get(id=id)
        return item


class Game_Character:
    def __init__(self, name, max_agility, current_agility, max_strange, current_strange, max_charm, current_charm,
                 lucky=[1, 2, 3, 4, 5, 6]):
        self.name = name
        self.max_agility = max_agility
        self.current_agility = current_agility
        self.max_strange = max_strange
        self.current_strange = current_strange
        self.max_charm = max_charm
        self.current_charm = current_charm
        self.lucky = lucky

    def delete_lucky(self, dice):
        try:
            self.lucky.remove(dice)
        except ValueError:
            pass

    def get_hurt(self, wound=2):
        self.current_strange -= wound

    def eat_and_heal(self, heal=4):
        if self.current_strange + heal <= self.max_strange:
            self.current_strange += heal
        else:
            self.current_strange = self.max_strange


def roll_the_dice(count):
    dice1 = random.randrange(1, 7)
    dice2 = random.randrange(1, 7)
    if count == 2:
        return dice1, dice2
    if count == 1:
        return dice1


def create_character():
    print('Крутим кубы')
    dice1, dice2 = roll_the_dice(2)
    summa = dice1 + dice2
    print(f'Кубик1:{dice1}, Кубик2{dice2}')
    char = Game_Character(name='Alex',
                          max_agility=start_stats[summa]['agility'],
                          current_agility=start_stats[summa]['agility'],
                          max_strange=start_stats[summa]['strange'],
                          current_strange=start_stats[summa]['strange'],
                          max_charm=start_stats[summa]['charm'],
                          current_charm=start_stats[summa]['charm'])
    char_inventory = Character_Inventory(user_id)
    bd_item = GameItemsModel.get(id=1)
    item = Game_Items(bd_item.id, bd_item.name, count=3)
    char_inventory.add_item(item)
    bd_item = GameItemsModel.get(id=1)
    item = Game_Items(bd_item.id, bd_item.name, count=5)
    char_inventory.add_item(item)
    item.increase_count()
    print(f"Отлично! персонаж создан!\n"
          f"Имя:{char.name}\n"
          f"Ловкость:{char.max_agility}\n"
          f"Сила:{char.max_strange}\n"
          f"Харизма:{char.max_charm}\n"
          f"Удача:{char.lucky}\n")
    print(f"инвентарь:{char_inventory.item1.name, char_inventory.item1.count}")
    dice1 = roll_the_dice(1)
    char.delete_lucky(dice1)
    dice1 = roll_the_dice(1)
    char.delete_lucky(dice1)
    save_character(user_id, char, char_inventory)


def check_char_in_base(user_id):
    try:
        char = GameCharacterModel.get(GameCharacterModel.user_id == user_id)
    except DoesNotExist:
        char = None
    finally:
        return char

def check_inventory_in_base(user_id):
    try:
        inventory = CharacterInventoryModel.get(CharacterInventoryModel.user_id == user_id)
    except DoesNotExist:
        inventory = None
    finally:
        return inventory

def save_character_to_base(user_id, char):
    chartobase = check_char_in_base(user_id)
    if chartobase is None:
        chartobase = GameCharacterModel()
    chartobase.user_id = user_id
    chartobase.character_name = char.name
    chartobase.max_agility = char.max_agility
    chartobase.current_agility = char.current_agility
    chartobase.max_strange = char.max_strange
    chartobase.current_strange = char.current_strange
    chartobase.max_charm = char.max_charm
    chartobase.current_charm = char.current_charm
    chartobase.lucky = char.lucky
    chartobase.save()

def save_inventory_to_base(user_id, char_inventory):
    inventory_to_base = check_inventory_in_base(user_id)
    if inventory_to_base is None:
        inventory_to_base=CharacterInventoryModel()
    inventory_to_base.user_id= char_inventory.user_id
    inventory_to_base.slots =char_inventory.slots
    if char_inventory.item1 is not None:
        inventory_to_base.item1 ={"item_id":char_inventory.item1.item_id, "name":char_inventory.item1.name, "count":char_inventory.item1.count}
    if char_inventory.item2 is not None:
        inventory_to_base.item2 ={"item_id":char_inventory.item2.item_id, "name":char_inventory.item2.name, "count":char_inventory.item2.count}
    if char_inventory.item3 is not None:
        inventory_to_base.item3 ={"item_id":char_inventory.item3.item_id, "name":char_inventory.item3.name, "count":char_inventory.item3.count}
    if char_inventory.item4 is not None:
        inventory_to_base.item4 ={"item_id":char_inventory.item4.item_id, "name":char_inventory.item4.name, "count":char_inventory.item4.count}
    if char_inventory.item5 is not None:
        inventory_to_base.item5 ={"item_id":char_inventory.item5.item_id, "name":char_inventory.item5.name, "count":char_inventory.item5.count}
    if char_inventory.item6 is not None:
        inventory_to_base.item6 ={"item_id":char_inventory.item6.item_id, "name":char_inventory.item6.name, "count":char_inventory.item6.count}
    if char_inventory.item7 is not None:
        inventory_to_base.item7 ={"item_id":char_inventory.item7.item_id, "name":char_inventory.item7.name, "count":char_inventory.item7.count}
    if char_inventory.item8 is not None:
        inventory_to_base.item8 ={"item_id":char_inventory.item8.item_id, "name":char_inventory.item8.name, "count":char_inventory.item8.count}
    if char_inventory.item9 is not None:
        inventory_to_base.item9 ={"item_id":char_inventory.item9.item_id, "name":char_inventory.item9.name, "count":char_inventory.item9.count}
    inventory_to_base.save()

def save_character(user_id, char, char_inventory):
    save_character_to_base(user_id, char)
    save_inventory_to_base(user_id, char_inventory)



def load_items():
    try:
        with open('game_items.json', 'r', encoding='utf-8') as file:
            items = json.load(file)
        for item in items:
            GameItemsModel.create(name=item)
    except:
        pass


if __name__ == '__main__':
    GameCharacterModel.create_table()
    CharacterInventoryModel.create_table()
    GameItemsModel.create_table()
    load_items()
    print("Шаг первый. создать персонаж + инвентарь.")
    create_character()
