
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
