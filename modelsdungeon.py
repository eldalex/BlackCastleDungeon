from peewee import *

dbhandler = SqliteDatabase('dungeon.db')


class BaseModel(Model):
    class Meta:
        database = dbhandler


class GameCharacterModel(BaseModel):
    user_id = IntegerField(column_name='UserID', null=False, unique=True)
    character_name = TextField(column_name='Name', null=False)
    max_skill = IntegerField(column_name='MaxSkill', null=False)
    current_skill = IntegerField(column_name='CurrentSkill', null=False)
    max_stamina = IntegerField(column_name='MaxStamina', null=False)
    current_stamina = IntegerField(column_name='CurrentStamina', null=False)
    lucky = IntegerField(column_name='Lucky', null=False)
    state = IntegerField(column_name='State', null=False)
    paragraphs = TextField(column_name='Paragraphs', null=False)

    class Meta:
        table_name = 'Game_Characters'


class GameCharacterInventoryModel(BaseModel):
    user_id = ForeignKeyField(GameCharacterModel, null=False, unique=True)
    slots = IntegerField(column_name='SlotsOfBackpack', null=False)
    char_items = TextField(column_name='CharItems', null=True)

    class Meta:
        table_name = 'Inventory_Characters'


class GameCharacterSpellBookModel(BaseModel):
    user_id = ForeignKeyField(GameCharacterModel, null=False, unique=True)
    spells = TextField(column_name='Spells', null=True)

    class Meta:
        table_name = 'Game_Character_Spell_Book'


class GameItemsModel(BaseModel):
    item_id = IntegerField(column_name='Item_id', null=False)
    item_name = TextField(column_name='Item_Name', null=False, unique=True)
    paragraph = IntegerField(column_name='Paragraph', null=False, default=0)

    class Meta:
        table_name = 'Game_Items'


class GameSpellsModel(BaseModel):
    name = TextField(column_name='Name', null=False, unique=True)
    description = TextField(column_name='Description', null=False)

    class Meta:
        table_name = 'Game_Spells'


class GameEnemysModel(BaseModel):
    name = TextField(column_name='Name', null=False, unique=True)
    nameRU = TextField(column_name='NameRus', null=False)
    paragraph = IntegerField(column_name='Paragraph', null=False)
    agility = TextField(column_name='Agility', null=False)
    strange = TextField(column_name='Strange', null=False)
    in_battle = IntegerField(column_name='In_Battle', null=False)
    ater_death = IntegerField(column_name='Ater_Death', null=False)
    delay = IntegerField(column_name='Delay', null=False)
    loyalty = TextField(column_name='Loyalty', null=False)

    class Meta:
        table_name = 'Game_Enemys'
