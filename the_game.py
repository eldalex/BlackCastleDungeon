from modelsdungeon import *
from game_character import Game_Character
from character_inventory import Character_Inventory
from game_items import Game_Items
from game_spell_book import Game_Spell_Book
from game_spell_book import Game_Spell

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
        self.state = 1
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
                if nubber_of_spell in range(1, 9):
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
        self.state = char_from_base.state
        self.parapraphs = json.loads(char_from_base.paragraphs)
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
