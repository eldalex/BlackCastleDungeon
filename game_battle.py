''' Класс реализующий битву'''
import modelsdungeon


class Game_Battle:
    def __init__(self, char, list_enemy, special_condition=None):
        self.char = char
        self.list_enemy = list_enemy
        self.char_winner = None
        self.round = 1
        self.count_parry = 0
        self.special_condition = special_condition

    def check_dead_or_alive(self):
        self.dead_alive = []
        self.count_death = 0
        for enemy in self.list_enemy:
            self.dead_alive.append(enemy.is_alive)
            if not enemy.is_alive:
                self.count_death += 1

    def get_battle_mobs(self):
        self.battle_mobs = []
        for enemy in self.list_enemy:
            if enemy.is_alive and self.round > enemy.delay and self.count_death >= enemy.ater_death:
                self.battle_mobs.append(enemy)

    def check_loyalty(self):
        for enemy in self.list_enemy:
            if enemy.loyalty <= 3:
                enemy.is_alive = False
                enemy.strange = 0
            elif enemy.loyalty > 18:
                enemy.modificator_plus = 1
            else:
                enemy.modificator_plus = 0

    def round_preparation(self):
        while self.char_winner is None:
            self.check_loyalty()
            self.check_dead_or_alive()
            self.get_battle_mobs()
            self.start_battle()
            if not self.char.is_alive:
                self.char_winner = False
            if not any(self.dead_alive):
                self.char_winner = True
            self.round += 1

    def start_battle(self):
        if self.char.is_alive and any(self.dead_alive):
            names = []
            under_attack = 0
            for enemy in self.battle_mobs:
                names.append({under_attack: enemy.nameRU})
                under_attack += 1
            print(f"дерёмся! c {names}\n")
            print(f"кого будем бить?")
            check = False
            while not check:
                try:
                    vibor = int(input())
                    if vibor not in range(0, len(self.battle_mobs)):
                        pass
                    else:
                        check = True
                except:
                    pass

            print(f"Раунд: {self.round}")
            self.char.calculate_power_punch()
            print(
                f"ТЫ: {self.char.name}; ловкость:{self.char.current_skill}; сила:{self.char.current_stamina}; мощность в раунде:{self.char.power_punch}")
            for enemy in self.battle_mobs:
                enemy.calculate_power_punch()
                print(
                    f"Враг: {enemy.nameRU}; ловкость:{enemy.agility}; сила:{enemy.strange}; мощность в раунде:{enemy.power_punch}")

            if self.char.power_punch > self.battle_mobs[vibor].power_punch:
                print(f"{self.char.power_punch} > {self.battle_mobs[vibor].power_punch}: Вы нанесли ранение\n")
                self.battle_mobs[vibor].get_hurt()
                self.count_parry = 0
            elif self.char.power_punch < self.battle_mobs[vibor].power_punch:
                print(f"{self.char.power_punch} < {self.battle_mobs[vibor].power_punch}:Вам наенсли ранение\n")
                self.char.get_hurt()
                self.battle_mobs[vibor].loyalty += 1
                self.count_parry = 0
            else:
                print(f"{self.char.power_punch} = {self.battle_mobs[vibor].power_punch}:Силы равны, парирование.\n")
                self.count_parry += 1
                if self.count_parry == 2:
                    self.battle_mobs[vibor].loyalty -= 1

            for other in range(0, len(self.battle_mobs)):
                if other != vibor:
                    if self.char.power_punch < self.battle_mobs[other].power_punch:
                        self.char.get_hurt()
                        print(
                            f"{self.char.power_punch} < {self.battle_mobs[other].power_punch}:Вам нанес ранение второй противник \n")

class Enemy:
    def __init__(self, bd_enemy):
        self.id = bd_enemy.id
        self.name = bd_enemy.name
        self.nameRU = bd_enemy.nameRU
        self.paragraph = int(bd_enemy.paragraph)
        self.agility = int(bd_enemy.agility)
        self.strange = int(bd_enemy.strange)
        self.delay = int(bd_enemy.delay)
        self.loyalty = int(bd_enemy.loyalty)
        self.in_battle = int(bd_enemy.in_battle)
        self.ater_death = int(bd_enemy.ater_death)
        self.modificator_plus = 0
        self.modificator_minus = 0
        self.power_punch = 0
        self.is_alive = True

    def calculate_power_punch(self):
        dice = roll_the_dice(1)
        self.power_punch = dice * 2 + int(self.agility) + self.modificator_plus

    def get_hurt(self):
        self.strange -= 2
        self.loyalty -= 2
        if self.strange <= 0:
            self.is_alive = False
            print(f'{self.nameRU} - погиб')