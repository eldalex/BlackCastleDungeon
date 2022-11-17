'''Игровая сцена, текущее состояние игры.'''
import dice
from modelsdungeon import *
from modelsdungeon import GameEnemysModel
from game_items import Game_Items
from game_shop import Game_Shop
from game_battle import Enemy


class Paragraph:
    def __init__(self, paragraph_id, paragraphs, content=None, crossing=None, secret_crossing_if_exist_item=None,
                 secret_crossing=None, secret_crossing_after_visit=None, items=None, shop=None,
                 conditional_crossing=None, win_crossing=None, luck_crossing_yes=None, luck_crossing_no=None,
                 battle_lucky=None, char_modificator=None):
        self.paragraph_id = paragraph_id
        if "content" in paragraphs[str(paragraph_id)]:
            self.content = paragraphs[str(paragraph_id)]["content"]
        else:
            self.content = None
        if "crossing" in paragraphs[str(paragraph_id)]:
            self.crossing = paragraphs[str(paragraph_id)]["crossing"]
        else:
            self.crossing = None
        if "secret_crossing_if_exist_item" in paragraphs[str(paragraph_id)]:
            self.secret_crossing_if_exist_item = paragraphs[str(paragraph_id)]["secret_crossing_if_exist_item"]
        else:
            self.secret_crossing_if_exist_item = None
        if "secret_crossing" in paragraphs[str(paragraph_id)]:
            self.secret_crossing = paragraphs[str(paragraph_id)]["secret_crossing"]
        else:
            self.secret_crossing = None
        if "secret_crossing_after_visit" in paragraphs[str(paragraph_id)]:
            self.secret_crossing_after_visit = paragraphs[str(paragraph_id)]["secret_crossing_after_visit"]
        else:
            self.secret_crossing_after_visit = None
        if "items" in paragraphs[str(paragraph_id)]:
            self.items = paragraphs[str(paragraph_id)]["items"]
        else:
            self.items = None
        if "shop" in paragraphs[str(paragraph_id)]:
            self.shop = paragraphs[str(paragraph_id)]["shop"]
        else:
            self.shop = None
        if "conditional_crossing" in paragraphs[str(paragraph_id)]:
            self.conditional_crossing = paragraphs[str(paragraph_id)]["conditional_crossing"]
        else:
            self.conditional_crossing = None
        if "win_crossing" in paragraphs[str(paragraph_id)]:
            self.win_crossing = paragraphs[str(paragraph_id)]["win_crossing"]
        else:
            self.win_crossing = None
        if "luck_crossing_yes" in paragraphs[str(paragraph_id)]:
            self.luck_crossing_yes = paragraphs[str(paragraph_id)]["luck_crossing_yes"]
        else:
            self.luck_crossing_yes = None
        if "luck_crossing_no" in paragraphs[str(paragraph_id)]:
            self.luck_crossing_no = paragraphs[str(paragraph_id)]["luck_crossing_no"]
        else:
            self.luck_crossing_no = None
        if "battle_lucky" in paragraphs[str(paragraph_id)]:
            self.battle_lucky = paragraphs[str(paragraph_id)]["battle_lucky"]
        else:
            self.battle_lucky = None
        if "char_modificator" in paragraphs[str(paragraph_id)]:
            self.char_modificator = paragraphs[str(paragraph_id)]["char_modificator"]
        else:
            self.char_modificator = None


class Scene:
    def __init__(self, paragraph_id, BalckCastleDungenon, session_game_history):
        self.paragraph_id = paragraph_id
        self.session_game_history = session_game_history
        print('pause')
        self.paragraph = None
        for item in self.session_game_history:
            if int(item.paragraph_id) == int(paragraph_id):
                self.paragraph = item
        if self.paragraph == None:
            self.paragraph = Paragraph(paragraph_id, BalckCastleDungenon.paragraphs)
            session_game_history.append(self.paragraph)
        self.char = BalckCastleDungenon.char
        self.char_spell_book = BalckCastleDungenon.char_spell_book
        self.prepare_scene()
        self.prepare_env_items()
        self.prepare_enemy()
        self.prepare_cross()
        self.prepare_shop()
        self.prepare_secret_crossing()
        self.prepare_variants()
        self.apply_char_modificators()

    def cast_spell(self):
        print('колдунство!')

    def cast_char_power(self):
        self.char.power_punch_modifikator = 2

    def cast_enemy_power(self):
        case_enemy=[]
        print('На кого накладывать заклинание:')
        for enemy in self.list_enemys:
            case_enemy.append(enemy.id)
            print(f"{enemy.id}:{enemy.nameRU}")
        if case_enemy!=[]:
            while True:
                try:
                    case= int(input())
                    if case in case_enemy:
                        for enemy in self.list_enemys:
                            if enemy.id==case:
                                enemy.modificator_minus=-2
                        break
                    else:
                        print('нет')
                except Exception as e:
                    print(e)
        else:
            print('нет никого')
        print('stop')

    def cast_copy_enemy(self):
        case_enemy=[]
        print('На кого накладывать заклинание:')
        for enemy in self.list_enemys:
            case_enemy.append(enemy.id)
            print(f"{enemy.id}:{enemy.nameRU}")
        if case_enemy!=[]:
            while True:
                try:
                    case= int(input())
                    if case in case_enemy:
                        for enemy in self.list_enemys:
                            if enemy.id==case:
                                print('сделать копию ')
                                ####### сделать копию #######
                        break
                    else:
                        print('нет')
                except Exception as e:
                    print(e)
        else:
            print('нет никого')
        print('stop')


    def cast_battle_spell(self):
        battle_spell = {}
        exists_spell = []
        for spell in self.char_spell_book.spells:

            if self.char_spell_book.spells[spell] is not None and self.char_spell_book.spells[spell].id in [4, 5, 6]:
                battle_spell.update({self.char_spell_book.spells[spell].id: self.char_spell_book.spells[spell].name})
        if battle_spell != {}:
            print('что колдуем?')
            for i in battle_spell:
                print(f"{i}: {battle_spell[i]}")
                exists_spell.append(i)
            while True:
                try:
                    sp = input()
                    if sp == 'cancel':
                        break
                    sp = int(sp)
                    if sp in exists_spell and sp == 4:
                        self.cast_char_power()
                        self.char_spell_book.del_spell_from_book(sp)
                        break
                    elif sp in exists_spell and sp == 5:
                        self.cast_enemy_power()
                        self.char_spell_book.del_spell_from_book(sp)
                        break
                    elif sp in exists_spell and sp == 5:
                        self.cast_copy_enemy()
                        self.char_spell_book.del_spell_from_book(sp)
                        break
                    else:
                        print('неа')
                except Exception as e:
                    print(e)

    def apply_char_modificators(self):
        if self.paragraph.char_modificator is not None:
            if "power_punch_modifikator" in self.paragraph.char_modificator:
                self.char.power_punch_modifikator = self.paragraph.char_modificator["power_punch_modifikator"]
                self.paragraph.char_modificator = None

    def prepare_enemy(self):
        self.list_enemys = []
        enemys_from_bd = GameEnemysModel.select().where(GameEnemysModel.paragraph == self.paragraph_id)
        for enemy in enemys_from_bd:
            self.list_enemys.append(Enemy(enemy))

    def prepare_env_items(self):
        self.list_items = []
        for i in self.paragraph.items:
            bd_item = GameItemsModel.get(id=i["id"])
            item = Game_Items(bd_item.item_id, bd_item.item_name, count=i["count"], paragraph=bd_item.paragraph)
            self.list_items.append(item)

    def prepare_scene(self):
        self.description = self.paragraph.content

    def prepare_cross(self):
        self.crossing = self.paragraph.crossing

    def prepare_shop(self):
        gsh = Game_Shop()
        if self.paragraph.shop is not None:
            for i in self.paragraph.shop:
                gsh.add_shop_item(i["id"], i["count"], i["price"])
        self.list_shop = gsh

    def prepare_secret_crossing_if_exist_item(self, list_item):
        self.secret_crossing_if_exist_item = []
        if self.paragraph.secret_crossing_if_exist_item is not None:
            char_items_id = []
            for item in list_item.char_items:
                if list_item.char_items[item] is not None:
                    char_items_id.append(list_item.char_items[item].item_id)
            for item in self.paragraph.secret_crossing_if_exist_item:
                if item['item_id'] in char_items_id:
                    self.secret_crossing_if_exist_item.append(item['crossing'])
        return self.secret_crossing_if_exist_item

    def prepare_secret_crossing(self):
        self.secret_crossing = []
        if self.paragraph.secret_crossing is not None:
            self.secret_crossing = self.paragraph.secret_crossing

    def prepare_secret_crossing_after_visit(self, history):
        self.secret_crossing_after_visit = []
        if self.paragraph.secret_crossing_after_visit:
            for item in self.paragraph.secret_crossing_after_visit:
                if item['visit_loc_id'] in history:
                    self.secret_crossing_after_visit.append(item['crossing'])
        return self.secret_crossing_after_visit

    def do_luck_crossing(self):
        if self.paragraph.luck_crossing_yes is not None:
            if len(self.paragraph.luck_crossing_yes) > 0:
                print('Бросаем кубы!')
                dice1, dice2 = dice.roll_the_dice(2)
                if dice1 + dice2 <= self.char.lucky:
                    print(f'Вы сегодня удачливы! в сумме на кубах {dice1 + dice2}, а ваша удача{self.char.lucky}')
                    if self.paragraph.luck_crossing_yes[0] not in self.paragraph.crossing:
                        self.paragraph.crossing.append(self.paragraph.luck_crossing_yes[0])
                    self.paragraph.luck_crossing_yes = []
                    self.prepare_variants()
                    return True
                else:
                    self.paragraph.luck_crossing_yes = []
                    if self.paragraph.luck_crossing_no is not None:
                        if self.paragraph.luck_crossing_yes[0] not in self.paragraph.crossing:
                            self.paragraph.crossing.append(self.paragraph.luck_crossing_no[0])
                        self.paragraph.luck_crossing_no = []
                    print(f'Сегодня явно не ваш день! в сумме на кубах {dice1 + dice2}, а ваша удача{self.char.lucky}')
                    return False
            else:
                print('Запас удачи на сегодня исчерпан')

    def prepare_variants(self):
        n = 5
        self.variants = {0: {"description": f"Где я?", "commands": "var"},
                         1: {"description": "Посмотреть инвентарь", "commands": "inv"},
                         2: {"description": "Осмотреться в поисках предметов", "commands": "env"},
                         3: {"description": "Взять предмет", "commands": "get_item"},
                         4: {"description": "Посмотреть статы", "commands": "stats"}
                         }
        if self.paragraph.conditional_crossing is not None:
            if "spell_crossing" in self.paragraph.conditional_crossing:
                for cross in self.paragraph.conditional_crossing["spell_crossing"]:
                    spell_id = self.paragraph.conditional_crossing["spell_crossing"][cross]["spell_id"]
                    if self.char_spell_book.check_spell_in_book(spell_id):
                        if int(cross) not in self.paragraph.crossing:
                            self.paragraph.crossing.append(int(cross))

        if self.paragraph.crossing is not None:
            for item in self.paragraph.crossing:
                self.variants.update({n: {"description": f"перейти на {item}", "commands": f"{item}"}})
                n += 1
        if self.paragraph.luck_crossing_yes is not None:
            self.variants.update({n: {"description": f"Проверь свою удачу", "commands": "luck"}})
            n += 1
        if self.paragraph.battle_lucky is not None:
            self.variants.update({n: {"description": f"Проверь свою боевую удачу", "commands": "battleluck"}})
            n += 1
        if self.paragraph.shop is not None:
            self.variants.update({n: {"description": f"Магазин", "commands": "shop"}})
            n += 1
        self.variants.update({n: {"description": f"Сохранить и выйти!", "commands": "exit"}})
