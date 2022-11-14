'''Игровая сцена, текущее состояние игры.'''
from modelsdungeon import *
from game_items import Game_Items
from game_shop import Game_Shop
class Scene:
    def __init__(self, paragrph_id, paragraphs):
        self.paragrph_id = str(paragrph_id)
        self.paragraphs = paragraphs
        self.prepare_scene()
        self.prepare_env_items()
        self.prepare_enemy()
        self.prepare_cross()
        self.prepare_shop()

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

    def prepare_shop(self):
        gsh = Game_Shop()
        if "shop" in self.paragraphs[self.paragrph_id]:
            for i in self.paragraphs[self.paragrph_id]["shop"]:
                gsh.add_shop_item(i["id"],i["count"],i["price"])
        self.list_shop = gsh
