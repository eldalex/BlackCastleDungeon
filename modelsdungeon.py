from peewee import *

dbhandler = SqliteDatabase('dungeon.db')


class BaseModel(Model):
    class Meta:
        database = dbhandler


class GameCharacterModel(BaseModel):
    user_id = IntegerField(column_name='UserID', null=False, unique=True)
    character_name = TextField(column_name='Name', null=False)
    max_agility = IntegerField(column_name='MaxAgility', null=False)
    current_agility = IntegerField(column_name='CurrentAgility', null=False)
    max_strange = IntegerField(column_name='MaxStrange', null=False)
    current_strange = IntegerField(column_name='CurrentStrange', null=False)
    max_charm = IntegerField(column_name='MaxCharm', null=False)
    current_charm = IntegerField(column_name='CurrentCharm', null=False)
    lucky = TextField(column_name='lucky', null=False)

    class Meta:
        table_name = 'Game_Characters'


class CharacterInventoryModel(BaseModel):
    user_id =ForeignKeyField(GameCharacterModel, null=False,unique=True)
    slots = IntegerField(column_name='SlotsOfBackpack', null=False)
    char_items = TextField(column_name='CharItems', null=True)

    class Meta:
        table_name = 'Inventory_Characters'

class GameItemsModel(BaseModel):
    name = TextField(column_name='Name', null=False, unique=True)

    class Meta:
        table_name = 'Game_items'