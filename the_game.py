'''Подготовка игры. загрузка предметов, создание/загруска персонажа, проверки'''
from modelsdungeon import *
from game_character import Game_Character
from character_inventory import Character_Inventory
from game_items import Game_Items
from game_spell_book import Game_Spell_Book
from game_spell_book import Game_Spell
import dice
from scene import Scene

user_id = 1606686846
import json


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
                    GameSpellsModel.create(spell_id=item["spell_id"],
                                           name=item["name"],
                                           description=item["description"])
                except Exception as e:
                    pass
        except Exception as e:
            print(e)

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
        chartobase.history_of_travel = json.dumps(self.char.history_of_travel, ensure_ascii=False)
        chartobase.paragraphs = json.dumps(self.paragraphs, ensure_ascii=False)
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
        skill = dice.roll_the_dice(1) + 6
        dice1, dice2 = dice.roll_the_dice(2)
        stamina = dice1 + dice2 + 12
        luck = dice.roll_the_dice(1) + 6
        self.char = Game_Character(name='Alex',
                                   max_skill=skill,
                                   current_skill=skill,
                                   max_stamina=stamina,
                                   current_stamina=stamina,
                                   lucky=luck)

    def setup_paragraphs(self):
        self.state = 1
        with open('game_parafraphs.json', 'r', encoding='utf-8') as file:
            self.paragraphs = json.load(file)

    def setup_spell_book(self):
        self.char_spell_book = Game_Spell_Book(self.user_id)
        print(f"Выбери 10 заклинаний(можно повторяться)!")
        base_spells = GameSpellsModel.select()
        for item in base_spells:
            print(f"{item.id}) '{item.name}': {item.description}")
        while not self.char_spell_book.check_free_cell():
            correct_num = False
            while not correct_num:
                try:
                    nubber_of_spell = int(input())
                    if nubber_of_spell in range(1, 9):
                        correct_num = True
                except Exception as e:
                    print(e)
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
        self.state = char_from_base.state
        self.char.history_of_travel = json.loads(char_from_base.history_of_travel)
        self.paragraphs = json.loads(char_from_base.paragraphs)
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
            if load_spell_book[cell] is not None:
                spell = Game_Spell(GameSpellsModel.select().where(GameSpellsModel.id == load_spell_book[cell]['id']).get())
                self.char_spell_book.add_spell(spell)
        print(f"Отлично! персонаж Загружен!")

    @staticmethod
    def game_cycle(BalckCastleDungenon):
        action = BalckCastleDungenon.state
        session_game_history=[]
        while True:
            if action == 'exit':
                break
            scene = Scene(action, BalckCastleDungenon,session_game_history)
            session_game_history = scene.session_game_history
            cross = 0
            TheGame.print_description(scene)
            if len(scene.crossing) == 1:
                if scene.crossing[0] == 999:
                    print('\n\nТы проиграл, но всегда же можно попробовать ещё разок!')
                    break

            while True:
                action = input()

                try:
                    if int(action) in scene.variants:
                        action = scene.variants[int(action)]['commands']
                    cross = int(action)
                    BalckCastleDungenon.char.history_of_travel.append(cross)
                    BalckCastleDungenon.state = cross
                except:
                    pass
                if action == 'stats':
                    TheGame.get_information_about_char(BalckCastleDungenon.char)
                elif action == 'inv':
                    TheGame.get_information_about_inventory(BalckCastleDungenon.char_inventory)
                elif action == 'env':
                    TheGame.get_information_about_env_items(scene.list_items)
                elif action == 'get_item':
                    TheGame.get_env_item(scene.list_items, BalckCastleDungenon.char_inventory,
                                         BalckCastleDungenon.paragraphs,
                                         scene.paragrph_id)
                elif action == 'shop':
                    TheGame.get_buy_item(scene.list_shop, BalckCastleDungenon.char_inventory,
                                         BalckCastleDungenon.paragraphs,
                                         scene.paragrph_id)
                elif action == 'exit':
                    BalckCastleDungenon.save_character_to_base()
                    BalckCastleDungenon.save_inventory_to_base()
                    BalckCastleDungenon.save_char_spell_book_to_base()
                    break
                elif action == 'var':
                    TheGame.print_description(scene)
                elif action == 'luck':
                    scene.do_luck_crossing()
                elif action == 'bspell':
                    scene.cast_battle_spell()
                elif cross in scene.crossing:
                    break
                elif cross in scene.prepare_secret_crossing_if_exist_item(BalckCastleDungenon.char_inventory):
                    break
                elif cross in scene.secret_crossing:
                    break
                elif cross in scene.prepare_secret_crossing_after_visit(BalckCastleDungenon.char.history_of_travel):
                    break
                else:
                    print('К сожалению нет. попробуем ещё варианты?')

    @staticmethod
    def print_description(scene):
        print('---------------------------------')
        max_count = 20
        de = scene.description.split(' ')
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
        print('\n---------------------------------')
        for i in scene.variants:
            print(f"{i}: {scene.variants[i]['description']}")

    @staticmethod
    def get_information_about_char(char):
        print(f"Имя:{char.name}\n"
              f"Мастерство:{char.max_skill}\n"
              f"Выносливость:{char.max_stamina}\n"
              f"Удача:{char.lucky}\n"
              f"Меч:{char.sword}\n")

    @staticmethod
    def get_information_about_inventory(char_inventory):
        print(f"инвентарь:")
        for item in char_inventory.char_items:
            if char_inventory.char_items[item] is not None:
                print(char_inventory.char_items[item].item_id,
                      char_inventory.char_items[item].name,
                      char_inventory.char_items[item].count)

    @staticmethod
    def get_information_about_env_items(list_items):
        if len(list_items) == 0:
            print('Вы не видите предметов, которые могли бы положить к себе в мешок')
        else:
            print(f"Вы оглядываетесь еще раз и видите следущие предметы:")
            for item in list_items:
                if item.count > 1:
                    print(f"{item.name}, в количестве: {item.count} шт.")
                else:
                    print(f"{item.name}")

    @staticmethod
    def get_env_item(list_items, char_inventory, paragrapsh, id):
        print(f"Что вы хотите взять?:")
        it = input()

        for item in list_items:
            if item.name == it:
                char_inventory.add_item(item)
                print(f"id: {item.item_id}, name: {item.name}, count: {item.count}")
                list_items.remove(item)
                paragrapsh[id]['items'].remove({'id': item.item_id, 'count': item.count})

    @staticmethod
    def get_money_count(char_inventory):
        ch_money_count = None
        for ch_item in char_inventory.char_items:
            if char_inventory.char_items[ch_item] is not None:
                if char_inventory.char_items[ch_item].item_id == 1:
                    ch_money_count = char_inventory.char_items[ch_item].count
        return ch_money_count

    @staticmethod
    def list_shop_items(list_shop):
        print(f"Что вы хотите купить?:")
        for item in list_shop.shop_items:
            print(f"{item.id}: {item.name}, количество:{item.count}, цена:{item.price}")
        print('exit: Выйти из магазина')

    @staticmethod
    def get_buy_item(list_shop, char_inventory, paragrapsh, id):
        while True:
            TheGame.list_shop_items(list_shop)
            choise = input()
            if choise != 'exit':
                try:
                    choise = int(choise)
                except:
                    print('Не понимаю о чем вы!')
                    choise = None
                if choise is not None:
                    buy_item: Shop_item = None
                    for item in list_shop.shop_items:
                        if item.id == choise:
                            buy_item = item
                    if buy_item is not None:
                        ch_money = TheGame.get_money_count(char_inventory)
                        if ch_money is not None:
                            if buy_item.price > ch_money:
                                print('К сожалению вам не хватит на это денег, выберите что то другое или уходите.')
                            else:
                                bd_item = GameItemsModel.get(buy_item.id)
                                new_item_for_char = Game_Items(bd_item.item_id, bd_item.item_name, count=1,
                                                               paragraph=bd_item.paragraph)
                                char_inventory.add_item(new_item_for_char)
                                char_inventory.decrement_count(1, buy_item.price)
                                buy_item.decrement_item()
                                list_shop.check_count()
                                char_inventory.clean_zero_inventory()
                        else:
                            print(
                                'Похоже что вы где то оставили свой кошелёк,в кредит незнакомцам я не даю.\nВозвращайтесь когда у вас будут деньги!')
                            break
                    else:
                        print('Увы, такого у меня нет, но ты посмотри на остальные товары!')
            else:
                paragrapsh[id]["shop"] = []
                for item in list_shop.shop_items:
                    paragrapsh[id]["shop"].append({"id": item.id, "count": item.count, "price": item.price})
                print('Досвидания, приходите к нам ещё!')
                break
