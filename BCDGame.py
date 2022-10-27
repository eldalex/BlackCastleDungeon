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


class Game_Battle:
    def __init__(self, char, list_enemy):
        self.char = char
        self.list_enemy = list_enemy
        self.char_winner = None
        self.round = 1
        self.count_parry = 0

    def check_dead_or_alive(self):
        self.dead_alive = []
        self.count_death = 0
        for enemy in self.list_enemy:
            self.dead_alive.append(enemy.is_alive)
            if not enemy.is_alive:
                self.count_death += 1

    def get_battle_mobs(self):
        self.battle_mobs = []
        for enemy in self.list_enemy:
            if enemy.is_alive and self.round > enemy.delay and self.count_death >= enemy.ater_death:
                self.battle_mobs.append(enemy)

    def check_loyalty(self):
        for enemy in self.list_enemy:
            if enemy.loyalty <= 3:
                enemy.is_alive = False
                enemy.strange = 0
            elif enemy.loyalty > 18:
                enemy.modificator_plus = 1
            else:
                enemy.modificator_plus = 0

    def round_preparation(self):
        while self.char_winner is None:
            self.check_loyalty()
            self.check_dead_or_alive()
            self.get_battle_mobs()
            self.start_battle()
            if not self.char.is_alive:
                self.char_winner = False
            if not any(self.dead_alive):
                self.char_winner = True
            self.round += 1

    def start_battle(self):
        if self.char.is_alive and any(self.dead_alive):
            names = []
            under_attack = 0
            for enemy in self.battle_mobs:
                names.append({under_attack: enemy.nameRU})
                under_attack += 1
            print(f"дерёмся! c {names}\n")
            print(f"кого будем бить?")
            check = False
            while not check:
                try:
                    vibor = int(input())
                    if vibor not in range(0, len(self.battle_mobs)):
                        pass
                    else:
                        check = True
                except:
                    pass

            print(f"Раунд: {self.round}")
            self.char.calculate_power_punch()
            print(
                f"ТЫ: {self.char.name}; ловкость:{self.char.current_agility}; сила:{self.char.current_strange}; мощность в раунде:{self.char.power_punch}")
            for enemy in self.battle_mobs:
                enemy.calculate_power_punch()
                print(
                    f"Враг: {enemy.nameRU}; ловкость:{enemy.agility}; сила:{enemy.strange}; мощность в раунде:{enemy.power_punch}")

            if self.char.power_punch > self.battle_mobs[vibor].power_punch:
                print(f"{self.char.power_punch} > {self.battle_mobs[vibor].power_punch}: Вы нанесли ранение\n")
                self.battle_mobs[vibor].get_hurt()
                self.count_parry = 0
            elif self.char.power_punch < self.battle_mobs[vibor].power_punch:
                print(f"{self.char.power_punch} < {self.battle_mobs[vibor].power_punch}:Вам наенсли ранение\n")
                self.char.get_hurt()
                self.battle_mobs[vibor].loyalty += 1
                self.count_parry = 0
            else:
                print(f"{self.char.power_punch} = {self.battle_mobs[vibor].power_punch}:Силы равны, парирование.\n")
                self.count_parry += 1
                if self.count_parry == 2:
                    self.battle_mobs[vibor].loyalty -= 1

            for other in range(0, len(self.battle_mobs)):
                if other != vibor:
                    if self.char.power_punch < self.battle_mobs[other].power_punch:
                        char.get_hurt()
                        print(
                            f"{self.char.power_punch} < {self.battle_mobs[other].power_punch}:Вам нанес ранение второй противник \n")


class Enemy:
    def __init__(self, bd_enemy):
        self.id = bd_enemy.id
        self.name = bd_enemy.name
        self.nameRU = bd_enemy.nameRU
        self.paragraph = int(bd_enemy.paragraph)
        self.agility = int(bd_enemy.agility)
        self.strange = int(bd_enemy.strange)
        self.delay = int(bd_enemy.delay)
        self.loyalty = int(bd_enemy.loyalty)
        self.in_battle = int(bd_enemy.in_battle)
        self.ater_death = int(bd_enemy.ater_death)
        self.modificator_plus = 0
        self.modificator_minus = 0
        self.power_punch = 0
        self.is_alive = True

    def calculate_power_punch(self):
        dice = roll_the_dice(1)
        self.power_punch = dice * 2 + int(self.agility) + self.modificator_plus

    def get_hurt(self):
        self.strange -= 2
        self.loyalty -= 2
        if self.strange <= 0:
            self.is_alive = False
            print(f'{self.nameRU} - погиб')


class Game_Items:
    def __init__(self, item_id, name, count=1, paragraph=0):
        self.item_id = item_id
        self.name = name
        self.count = count
        self.paragraph = paragraph
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
    # def get_item(self, id):
    #     item = GameItemsModel.get(id=id)
    #     return item


class Game_Character:
    def __init__(self, name, max_agility, current_agility, max_strange, current_strange, max_charm, current_charm,
                 lucky=[1, 2, 3, 4, 5, 6]):
        self.name = name
        self.max_agility = int(max_agility)
        self.current_agility = int(current_agility)
        self.max_strange = int(max_strange)
        self.current_strange = int(current_strange)
        self.max_charm = int(max_charm)
        self.current_charm = int(current_charm)
        self.lucky = lucky
        self.sword = 0
        self.power_punch = None
        self.is_alive = True

    def delete_lucky(self, dice):
        try:
            self.lucky.remove(dice)
        except ValueError:
            pass

    def get_hurt(self, modifikator=0):
        self.current_strange -= 2 + modifikator
        if self.current_strange <= 0:
            self.is_alive = False

    def eat_and_heal(self, heal=4):
        if self.current_strange + heal <= self.max_strange:
            self.current_strange += heal
        else:
            self.current_strange = self.max_strange

    def calculate_power_punch(self):
        dice = roll_the_dice(1)
        self.power_punch = dice * 2 + int(self.current_agility)


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
    print(f'Кубик1:{dice1}, Кубик2:{dice2}')
    char = Game_Character(name='Alex',
                          max_agility=start_stats[summa]['agility'],
                          current_agility=start_stats[summa]['agility'],
                          max_strange=start_stats[summa]['strange'],
                          current_strange=start_stats[summa]['strange'],
                          max_charm=start_stats[summa]['charm'],
                          current_charm=start_stats[summa]['charm'])
    char_inventory = Character_Inventory(user_id)
    bd_item = GameItemsModel.get(id=1)
    item = Game_Items(bd_item.id, bd_item.name, count=3, paragraph=bd_item.paragraph)
    char_inventory.add_item(item)
    dice1 = roll_the_dice(1)
    char.delete_lucky(dice1)
    dice1 = roll_the_dice(1)
    char.delete_lucky(dice1)

    print(f"Отлично! персонаж создан!")
    save_character(user_id, char, char_inventory)
    return char, char_inventory


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
        inventory_to_base = CharacterInventoryModel()
    inventory_to_base.user_id = char_inventory.user_id
    inventory_to_base.slots = char_inventory.slots
    char_inventory_json = {}
    for item in char_inventory.char_items:
        if char_inventory.char_items[item] is not None:
            char_inventory_json.update({item: {"item_id": char_inventory.char_items[item].item_id,
                                               "count": char_inventory.char_items[item].count}})
        else:
            char_inventory_json.update({item: None})
    inventory_to_base.char_items = json.dumps(char_inventory_json)
    inventory_to_base.save()


def save_character(user_id, char, char_inventory):
    save_character_to_base(user_id, char)
    save_inventory_to_base(user_id, char_inventory)


def load_character(user_id):
    char_from_base = check_char_in_base(user_id)
    character = Game_Character(name=char_from_base.character_name,
                               max_agility=char_from_base.max_agility,
                               current_agility=char_from_base.current_agility,
                               max_strange=char_from_base.max_strange,
                               current_strange=char_from_base.current_strange,
                               max_charm=char_from_base.max_charm,
                               current_charm=char_from_base.current_charm,
                               lucky=char_from_base.lucky)
    inventory_from_base = check_inventory_in_base(user_id)
    char_inventory = Character_Inventory(user_id)
    char_inventory.slots = inventory_from_base.slots
    load_items = json.loads(inventory_from_base.char_items.replace("'", '"'))
    for item in load_items:
        if load_items[item] is not None:
            bd_item = GameItemsModel.get(id=load_items[item]['item_id'])
            item = Game_Items(bd_item.id, bd_item.name, count=load_items[item]['count'])
            char_inventory.add_item(item)
    print(f"Отлично! персонаж Загружен!")
    return character, char_inventory


def load_items():
    try:
        with open('game_items.json', 'r', encoding='utf-8') as file:
            items = json.load(file)
        for item in items:
            try:
                GameItemsModel.create(name=item)
            except:
                pass
    except:
        pass


def load_enemys():
    try:
        with open('GameEnemys.json', 'r', encoding='utf-8') as file:
            items = json.load(file)
        for item in items:
            try:
                GameEnemysModel.create(name=item,
                                       nameRU=items[item]["nameRU"],
                                       paragraph=items[item]["paragraph"],
                                       agility=items[item]["agility"],
                                       strange=items[item]["strange"],
                                       in_battle=items[item]["in_battle"],
                                       ater_death=items[item]["ater_death"],
                                       delay=items[item]["delay"],
                                       loyalty=items[item]["loyalty"])
            except Exception as e:
                pass
    except Exception as e:
        print(e)
        pass


def check_is_alive(list_enemys):
    check_list = []
    for enemy in list_enemys:
        check_list.append(enemy.is_alive)
    if any(check_list):
        return True
    else:
        return False


if __name__ == '__main__':
    GameCharacterModel.create_table()
    CharacterInventoryModel.create_table()
    GameItemsModel.create_table()
    GameEnemysModel.create_table()
    load_items()
    load_enemys()
    print("Шаг первый. создать персонаж + инвентарь.")
    # char, char_inventory = create_character()
    char, char_inventory = load_character(user_id)
    print(f"Имя:{char.name}\n"
          f"Ловкость:{char.max_agility}\n"
          f"Сила:{char.max_strange}\n"
          f"Харизма:{char.max_charm}\n"
          f"Удача:{char.lucky}\n"
          f"Меч:{char.sword}\n")
    print(f"инвентарь:")
    for item in char_inventory.char_items:
        if char_inventory.char_items[item] is not None:
            print(char_inventory.char_items[item].item_id, char_inventory.char_items[item].name,
                  char_inventory.char_items[item].count)
    list_enemys = []
    # paragraph = 628
    paragraph = 6
    enemys_from_bd = GameEnemysModel.select().where(GameEnemysModel.paragraph == paragraph)
    for enemy in enemys_from_bd:
        list_enemys.append(Enemy(enemy))
    print('----------------------------------------ПОДЕРЁМСЯ----------------------------------------')
    char.current_strange = 100
    battle = Game_Battle(char, list_enemys)
    battle.round_preparation()
    if battle.char_winner:
        print('ты победил!')
    else:
        print('ты проиграл')
