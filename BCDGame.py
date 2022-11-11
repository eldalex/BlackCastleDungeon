from dice import roll_the_dice
import json
import peewee
from peewee import *
from modelsdungeon import *
from scene import Scene
from game_items import Game_Items
from the_game import TheGame
from character_inventory import Character_Inventory
from game_character import Game_Character
from game_battle import Game_Battle
from game_battle import Enemy

user_id = 1606686846


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
    if len(list_items) == 0:
        print('Вы не видите предметов, которые могли бы положить к себе в мешок')
    else:
        print(f"Вы оглядываетесь еще раз и видите следущие предметы:")
        for item in list_items:
            if item.count > 1:
                print(f"{item.name}, в количестве: {item.count} шт.")
            else:
                print(f"{item.name}")


def get_env_item(list_items, char_inventory, paragrapsh, id):
    print(f"Что вы хотите взять?:")
    it = input()

    for item in list_items:
        if item.name == it:
            char_inventory.add_item(item)
            print(f"id: {item.item_id}, name: {item.name}, count: {item.count}")
            list_items.remove(item)
            paragrapsh[id]['items'].remove({'id': item.item_id, 'count': item.count})


def get_money_count(char_inventory):
    ch_money_count = None
    for ch_item in char_inventory.char_items:
        if char_inventory.char_items[ch_item] is not None:
            if char_inventory.char_items[ch_item].item_id == 1:
                ch_money_count = char_inventory.char_items[ch_item].count
    return ch_money_count


def get_buy_item(list_shop, char_inventory, paragrapsh, id):
    print(f"Что вы хотите купить?:")
    for item in list_shop:
        print(f"id:{item['item'].item_id}, {item['item'].name}, количество:{item['item'].count}, цена:{item['price']}")
    while True:
        try:
            it = int(input())
            buy_item = None
            for item in list_shop:
                if item['item'].item_id == it:
                    buy_item = {"id": item['item'].item_id, "shop_item": item['item'], "cost": item['price']}
            if buy_item is None:
                print('Некорректный ввод')
            else:
                break
        except:
            print('некорректный ввод')

    ch_money = get_money_count(char_inventory)
    if buy_item['cost'] > ch_money:
        print('недостаточно денег')
    else:
        bd_item = GameItemsModel.get(id=buy_item["id"])
        new_item_for_char = Game_Items(bd_item.item_id, bd_item.item_name, count=1, paragraph=bd_item.paragraph)
        char_inventory.add_item(new_item_for_char)
        char_inventory.decrement_count(1, buy_item['cost'])
        buy_item["shop_item"].count -= 1
        if buy_item["shop_item"].count == 0:
            for item in list_shop:
                if item['item'].item_id == it:
                    list_shop.remove(item)
            for item in paragrapsh[id]["shop"]:
                if item['id'] == it:
                    paragrapsh[id]["shop"].remove(item)
        else:
            for item in paragrapsh[id]["shop"]:
                if item['id'] == it:
                    item['count'] -= 1

    ch_money = get_money_count(char_inventory)
    if ch_money == 0:
        char_inventory.delete_item(1)

    if ch_money is not None:
        print(ch_money)
    else:
        print('У вас нет денег')

        #
        # char_inventory.add_item(item)
        # print(f"id: {item.item_id}, name: {item.name}, count: {item.count}")
        # list_items.remove(item)
        # paragrapsh[id]['items'].remove({'id':item.item_id,'count':item.count})


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
        print(
            f'\nчто делать? варианты:{scene.crossing}\n stats - инфо о персонаже, inv - инвентарь, env - осмотреться, get_item - взять предмет, exit - сохранить т выйти ')
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
                get_env_item(scene.list_items, BalckCastleDungenon.char_inventory, BalckCastleDungenon.parapraphs,
                             scene.paragrph_id)
            elif action == 'shop':
                get_buy_item(scene.list_shop, BalckCastleDungenon.char_inventory, BalckCastleDungenon.parapraphs,
                             scene.paragrph_id)
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
# print('конец')
# print('----------------------------------------ПОДЕРЁМСЯ----------------------------------------')
# BalckCastleDungenon.char.current_stamina = 100
# battle = Game_Battle(BalckCastleDungenon.char, list_enemys)
# battle.round_preparation()
# if battle.char_winner:
#     print('ты победил!')
# else:
#     print('ты проиграл')
