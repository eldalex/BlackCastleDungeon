from dice import roll_the_dice
import json
import peewee
from peewee import *
from modelsdungeon import *

user_id = 1606686846


class Scene:
    def __init__(self, paragrph_id, paragraphs):
        self.paragrph_id = str(paragrph_id)
        self.paragraphs = paragraphs
        self.prepare_scene()
        self.prepare_env_items()
        self.prepare_enemy()
        self.prepare_cross()

    def prepare_enemy(self):
        self.list_enemys = []
        enemys_from_bd = GameEnemysModel.select().where(GameEnemysModel.paragraph == self.paragrph_id)
        for enemy in enemys_from_bd:
            self.list_enemys.append(Enemy(enemy))

    def prepare_env_items(self):
        self.list_items = []
        for i in self.paragraphs[self.paragrph_id]["items"]:
            bd_item = GameItemsModel.get(id=i["id"])
            item = Game_Items(bd_item.item_id, bd_item.item_name, count=i["count"], paragraph=bd_item.paragraph)
            self.list_items.append(item)

    def prepare_scene(self):
        self.description = self.paragraphs[self.paragrph_id]["content"]

    def prepare_cross(self):
        self.crossing = self.paragraphs[self.paragrph_id]["crossing"]


class TheGame:
    def __init__(self, user_id):
        self.user_id = user_id

    def check_char_in_base(self):
        try:
            char = GameCharacterModel.get(GameCharacterModel.user_id == self.user_id)
        except DoesNotExist:
            char = None
        finally:
            return char

    def check_book_in_base(self):
        try:
            spell_book = GameCharacterSpellBookModel.get(GameCharacterSpellBookModel.user_id == self.user_id)
        except DoesNotExist:
            spell_book = None
        finally:
            return spell_book

    def check_inventory_in_base(self):
        try:
            inventory = GameCharacterInventoryModel.get(GameCharacterInventoryModel.user_id == self.user_id)
        except DoesNotExist:
            inventory = None
        finally:
            return inventory

    def prepare_enviroment(self):
        GameCharacterModel.create_table()
        GameCharacterInventoryModel.create_table()
        GameItemsModel.create_table()
        GameEnemysModel.create_table()
        GameSpellsModel.create_table()
        GameCharacterSpellBookModel.create_table()
        self.load_items()
        self.load_enemys()
        self.load_spell()

    def load_items(self):
        try:
            with open('game_items.json', 'r', encoding='utf-8') as file:
                items = json.load(file)
            for item in items:
                try:
                    GameItemsModel.create(
                        item_id=items[item]["item_id"],
                        item_name=items[item]["item_name"])
                except Exception as e:
                    pass
        except:
            pass

    def load_spell(self):
        try:
            with open('game_spells.json', 'r', encoding='utf-8') as file:
                items = json.load(file)
            for item in items:
                try:
                    GameSpellsModel.create(name=item["name"],
                                           description=item["description"])
                except Exception as e:
                    pass
        except:
            pass

    def load_enemys(self):
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

    def create_character(self):
        self.setup_char()
        self.setup_inventory()
        self.setup_spell_book()
        self.setup_paragraphs()
        print(f"Отлично! персонаж создан!")
        self.save_character()

    def save_character_to_base(self):
        chartobase = self.check_char_in_base()
        if chartobase is None:
            chartobase = GameCharacterModel()
        chartobase.user_id = self.user_id
        chartobase.character_name = self.char.name
        chartobase.max_skill = self.char.max_skill
        chartobase.current_skill = self.char.current_skill
        chartobase.max_stamina = self.char.max_stamina
        chartobase.current_stamina = self.char.current_stamina
        chartobase.lucky = self.char.lucky
        chartobase.state = self.state
        chartobase.paragraphs = json.dumps(self.parapraphs, ensure_ascii=False)
        chartobase.save()

    def save_char_spell_book_to_base(self):
        spell_book_to_base = self.check_book_in_base()
        if spell_book_to_base is None:
            spell_book_to_base = GameCharacterSpellBookModel()
        spell_book_to_base.user_id = self.char_spell_book.user_id
        char_spell_book_json = {}
        for spell in self.char_spell_book.spells:
            if self.char_spell_book.spells[spell] is not None:
                char_spell_book_json.update({spell: {
                    "id": self.char_spell_book.spells[spell].id,
                    "name": self.char_spell_book.spells[spell].name,
                    "description": self.char_spell_book.spells[spell].description
                }})
            else:
                char_spell_book_json.update({spell: None})
        spell_book_to_base.spells = json.dumps(char_spell_book_json, ensure_ascii=False)
        spell_book_to_base.save()

    def save_inventory_to_base(self):
        inventory_to_base = self.check_inventory_in_base()
        if inventory_to_base is None:
            inventory_to_base = GameCharacterInventoryModel()
        inventory_to_base.user_id = self.char_inventory.user_id
        inventory_to_base.slots = self.char_inventory.slots
        char_inventory_json = {}
        for item in self.char_inventory.char_items:
            if self.char_inventory.char_items[item] is not None:
                char_inventory_json.update({item: {"item_id": self.char_inventory.char_items[item].item_id,
                                                   "count": self.char_inventory.char_items[item].count}})
            else:
                char_inventory_json.update({item: None})
        inventory_to_base.char_items = json.dumps(char_inventory_json)
        inventory_to_base.save()

    def save_character(self):
        self.save_character_to_base()
        self.save_inventory_to_base()
        self.save_char_spell_book_to_base()


    def setup_inventory(self):
        self.char_inventory = Character_Inventory(self.user_id)
        bd_item = GameItemsModel.get(id=2)
        item = Game_Items(bd_item.item_id, bd_item.item_name, count=3, paragraph=bd_item.paragraph)
        self.char_inventory.add_item(item)
        bd_item = GameItemsModel.get(id=1)
        item = Game_Items(bd_item.item_id, bd_item.item_name, count=15, paragraph=bd_item.paragraph)
        self.char_inventory.add_item(item)
        bd_item = GameItemsModel.get(id=3)
        item = Game_Items(bd_item.item_id, bd_item.item_name, count=2, paragraph=bd_item.paragraph)
        self.char_inventory.add_item(item)

    def setup_char(self):
        print('Крутим кубы')
        skill = roll_the_dice(1) + 6
        dice1, dice2 = roll_the_dice(2)
        stamina = dice1 + dice2 + 12
        luck = roll_the_dice(1) + 6
        self.char = Game_Character(name='Alex',
                                   max_skill=skill,
                                   current_skill=skill,
                                   max_stamina=stamina,
                                   current_stamina=stamina,
                                   lucky=luck)
    def setup_paragraphs(self):
        self.state=1
        with open('game_parafraphs.json', 'r', encoding='utf-8') as file:
            self.parapraphs = json.load(file)

    def setup_spell_book(self):
        self.char_spell_book = Game_Spell_Book(self.user_id)
        print(f"Выбери 10 заклинаний(можно повторяться)!")
        base_spells = GameSpellsModel.select()
        for item in base_spells:
            print(f"{item.id}) '{item.name}': {item.description}")
        while not self.char_spell_book.check_free_cell():
            correct_num = False
            while not correct_num:
                nubber_of_spell = int(input())
                if nubber_of_spell in range(1, len(GameSpellsModel.select()) + 1):
                    correct_num = True
            spell = Game_Spell(GameSpellsModel.select().where(GameSpellsModel.id == nubber_of_spell).get())
            self.char_spell_book.add_spell(spell)
            print(f"{spell.name} добавлен в книгу")

    def load_character(self):
        char_from_base = self.check_char_in_base()
        self.char = Game_Character(name=char_from_base.character_name,
                                   max_skill=char_from_base.max_skill,
                                   current_skill=char_from_base.current_skill,
                                   max_stamina=char_from_base.max_stamina,
                                   current_stamina=char_from_base.current_stamina,
                                   lucky=char_from_base.lucky)
        self.state=char_from_base.state
        self.parapraphs=json.loads(char_from_base.paragraphs)
        inventory_from_base = self.check_inventory_in_base()
        self.char_inventory = Character_Inventory(self.user_id)
        self.char_inventory.slots = inventory_from_base.slots
        load_items = json.loads(inventory_from_base.char_items)
        for item in load_items:
            if load_items[item] is not None:
                bd_item = GameItemsModel.get(id=load_items[item]['item_id'])
                item = Game_Items(bd_item.item_id, bd_item.item_name, count=load_items[item]['count'])
                self.char_inventory.add_item(item)
        load_spell_book = json.loads(GameCharacterSpellBookModel.get(user_id=user_id).spells)
        self.char_spell_book = Game_Spell_Book(self.user_id)
        for cell in load_spell_book:
            spell = Game_Spell(GameSpellsModel.select().where(GameSpellsModel.id == load_spell_book[cell]['id']).get())
            self.char_spell_book.add_spell(spell)
        print(f"Отлично! персонаж Загружен!")


class Game_Spell_Book:
    def __init__(self, user_id):
        self.user_id = user_id
        self.spells = {"cell1": None,
                       "cell2": None,
                       "cell3": None,
                       "cell4": None,
                       "cell5": None,
                       "cell6": None,
                       "cell7": None,
                       "cell8": None,
                       "cell9": None,
                       "cell10": None}

    def add_spell(self, spell):
        for cell in self.spells:
            if self.spells[cell] == None:
                self.spells[cell] = spell
                break

    def check_free_cell(self):
        free = True
        for cell in self.spells:
            if self.spells[cell] is None:
                free = False
                break
        return free


class Game_Spell:
    def __init__(self, spell_from_bd):
        self.id = spell_from_bd.id
        self.name = spell_from_bd.name
        self.description = spell_from_bd.description


class Game_Battle:
    def __init__(self, char, list_enemy, special_condition=None):
        self.char = char
        self.list_enemy = list_enemy
        self.char_winner = None
        self.round = 1
        self.count_parry = 0
        self.special_condition = special_condition

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
                f"ТЫ: {self.char.name}; ловкость:{self.char.current_skill}; сила:{self.char.current_stamina}; мощность в раунде:{self.char.power_punch}")
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
                        self.char.get_hurt()
                        print(
                            f"{self.char.power_punch} < {self.battle_mobs[other].power_punch}:Вам нанес ранение второй противник \n")


class Enemy:
    def __init__(self, bd_enemy):
        self.id = bd_enemy.id
        self.name = bd_enemy.name
        self.nameRU = bd_enemy.nameRU
        self.paragraph = int(bd_enemy.action)
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
    def __init__(self, name, max_skill, current_skill, max_stamina, current_stamina, lucky):
        self.name = name
        self.max_skill = int(max_skill)
        self.current_skill = int(current_skill)
        self.max_stamina = int(max_stamina)
        self.current_stamina = int(current_stamina)
        self.lucky = lucky
        self.sword = 0
        self.power_punch = None
        self.is_alive = True

    def delete_lucky(self):
        try:
            self.lucky -= 1
        except ValueError:
            pass

    def add_lucky(self):
        try:
            self.lucky += 1
        except ValueError:
            pass

    def get_hurt(self, modifikator=0):
        self.current_stamina -= 2 + modifikator
        if self.current_stamina <= 0:
            self.is_alive = False

    def eat_and_heal(self, heal=4):
        if self.current_stamina + heal <= self.max_stamina:
            self.current_stamina += heal
        else:
            self.current_stamina = self.max_stamina

    def calculate_power_punch(self, modifikator=0):
        dice = roll_the_dice(1)
        self.power_punch = dice * 2 + int(self.current_skill) + modifikator


def print_description(desc):
    max_count = 20
    de = desc.split(' ')
    count = 0
    for i in de:
        if count == max_count:
            print(i + '\n', end='')
            count = 0
        elif count == 0:
            print(i.strip(), end=' ')
            count += 1
        else:
            print(i, end=' ')
            count += 1


def get_information_about_char(char):
    print(f"Имя:{char.name}\n"
          f"Мастерство:{char.max_skill}\n"
          f"Выносливость:{char.max_stamina}\n"
          f"Удача:{char.lucky}\n"
          f"Меч:{char.sword}\n")


def get_information_about_inventory(char_inventory):
    print(f"инвентарь:")
    for item in char_inventory.char_items:
        if char_inventory.char_items[item] is not None:
            print(char_inventory.char_items[item].item_id,
                  char_inventory.char_items[item].name,
                  char_inventory.char_items[item].count)


def get_information_about_env_items(list_items):
    if len(list_items)==0:
        print('Вы не видите предметов, которые могли бы положить к себе в мешок')
    else:
        print(f"Вы оглядываетесь еще раз и видите следущие предметы:")
        for item in list_items:
            if item.count>1:
                print(f"{item.name}, в количестве: {item.count} шт.")
            else:
                print(f"{item.name}")

def get_env_item(list_items,char_inventory,paragrapsh,id):
    print(f"Что вы хотите взять?:")
    it = input()

    for item in list_items:
        if item.name == it:
            char_inventory.add_item(item)
            print(f"id: {item.item_id}, name: {item.name}, count: {item.count}")
            list_items.remove(item)
            paragrapsh[id]['items'].remove({'id':item.item_id,'count':item.count})


if __name__ == '__main__':
    BalckCastleDungenon = TheGame(user_id)
    BalckCastleDungenon.prepare_enviroment()
    # BalckCastleDungenon.create_character()
    BalckCastleDungenon.load_character()
    print('Предыстория, поехали!')

    action = BalckCastleDungenon.state
    while True:
        if action == 'exit':
            break
        scene = Scene(action, BalckCastleDungenon.parapraphs)
        cross = 0
        print_description(scene.description)
        if len(scene.crossing) == 1:
            if scene.crossing[0] == 999:
                print('Ты проиграл')
                break
        print(f'\nчто делать? варианты:{scene.crossing}, stats - инфо о персонаже, inv - инвентарь')
        while True:
            action = input()
            try:
                cross = int(action)
                BalckCastleDungenon.state = cross
            except:
                pass
            if action == 'stats':
                get_information_about_char(BalckCastleDungenon.char)
            elif action == 'inv':
                get_information_about_inventory(BalckCastleDungenon.char_inventory)
            elif action == 'env':
                get_information_about_env_items(scene.list_items)
            elif action == 'get_item':
                get_env_item(scene.list_items,BalckCastleDungenon.char_inventory,BalckCastleDungenon.parapraphs,scene.paragrph_id)
            elif action == 'exit':
                BalckCastleDungenon.save_character_to_base()
                BalckCastleDungenon.save_inventory_to_base()
                BalckCastleDungenon.save_char_spell_book_to_base()
                break
            elif cross in scene.crossing:
                break
            else:
                print('нет такого выбора, давай ещё')

# paragraph = 628
print('конец')
# print('----------------------------------------ПОДЕРЁМСЯ----------------------------------------')
# BalckCastleDungenon.char.current_stamina = 100
# battle = Game_Battle(BalckCastleDungenon.char, list_enemys)
# battle.round_preparation()
# if battle.char_winner:
#     print('ты победил!')
# else:
#     print('ты проиграл')
