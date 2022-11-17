'''Класс реализующий игрового персонажа'''
class Game_Character:
    def __init__(self, name, max_skill, current_skill, max_stamina, current_stamina, lucky):
        self.name = name
        self.max_skill = int(max_skill)
        self.current_skill = int(current_skill)
        self.max_stamina = int(max_stamina)
        self.current_stamina = int(current_stamina)
        self.lucky = lucky
        self.sword = 0
        self.power_punch = None
        self.power_punch_modifikator = 0
        self.is_alive = True
        self.history_of_travel=[1]
        self.skill_modificator=0

    def delete_lucky(self):
        try:
            self.lucky -= 1
        except ValueError:
            pass

    def add_lucky(self):
        try:
            self.lucky += 1
        except ValueError:
            pass

    def get_hurt(self, modifikator=0):
        self.current_stamina -= 2 + modifikator
        if self.current_stamina <= 0:
            self.is_alive = False

    def eat_and_heal(self, heal=4):
        if self.current_stamina + heal <= self.max_stamina:
            self.current_stamina += heal
        else:
            self.current_stamina = self.max_stamina

    def calculate_power_punch(self, modifikator=0):
        dice = roll_the_dice(1)
        self.power_punch = dice * 2 + int(self.current_skill) + modifikator
