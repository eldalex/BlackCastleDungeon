'''класс реализующий игровые предметы.'''
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