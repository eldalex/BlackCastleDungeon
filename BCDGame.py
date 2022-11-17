'''Основная игра'''
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
from game_shop import Shop_item

user_id = 1606686846







if __name__ == '__main__':
    BalckCastleDungenon = TheGame(user_id)
    # BalckCastleDungenon.prepare_enviroment()
    # BalckCastleDungenon.create_character()
    BalckCastleDungenon.load_character()
    print('Предыстория, поехали!')
    TheGame.game_cycle(BalckCastleDungenon)


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
