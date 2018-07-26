import random as rnd
import math
import numpy as np


class Creature(object):
    """
    :param size, intelligence, strength, speed, dexterity: positive num
    :param social: num between -1 and 1
        specifies social behaviour
        -1 for very extremely solo, +1 for extreme herds
    :param digestion: num between -1 and 1
        specifies digestion efficiency of eaten food
        -1 is for plants at full efficiency, +1 for creatures at full efficiency, 0 for both at half efficiency
    :param mutation_factor: num between 0 and 0.1 (should not be higher or negative numbers may appear)
        sets the variance of the randomly generated traits of a new create
    :param sex_drive: num between 0 and 1
        specifies intensity of sexual drive
        0 for no desire of sex, 1 for extreme sexual desire

    the max variables define the maximum obtainable values after full growth
    the start variables (at birth) are a tenth of the max variables
    """
    def __init__(self, size, intelligence, social, digestion, strength, speed, dexterity, sex_drive,
                 mutation_factor=0.04, hunger=0.5, thirst=0.5, health=1):

        self.gender          = rnd.choice(["male", "female"])
        self.mutation_factor = mutation_factor

        self.max_size = rnd.normalvariate(size, size*mutation_factor)
        self.size     = self.max_size / 10

        self.max_intelligence = rnd.normalvariate(intelligence, intelligence*mutation_factor)
        self.intelligence     = self.max_intelligence / 10

        self.max_strength = rnd.normalvariate(strength, strength*mutation_factor)
        self.strength     = self.max_strength / 10

        self.max_speed = rnd.normalvariate(speed, speed*mutation_factor)
        self.speed     = self.max_speed / 10

        self.max_dexterity = rnd.normalvariate(dexterity, dexterity*mutation_factor)
        self.dexterity     = self.max_dexterity / 10

        social      = math.tan(social)
        social      = rnd.normalvariate(social, social*mutation_factor)
        self.social = math.tanh(social)

        digestion      = math.tan(digestion)
        digestion      = rnd.normalvariate(digestion, digestion*mutation_factor)
        self.digestion = math.tanh(digestion)

        self.hunger  = hunger
        self.thirst  = thirst
        self.health  = health
        self.fitness = np.min(self.hunger, self.thirst, self.health)

        sex_drive          = math.tan(sex_drive * 2 - 1)
        sex_drive          = rnd.normalvariate(sex_drive, sex_drive*mutation_factor)
        self.max_sex_drive = np.sigmoid(sex_drive)
        self.sex_drive     = 0

    def procreation(self, partner):
        """
        :param partner: other creature
        :return: newborn creature

        creates new creature based on the stats of its parents
        """
        new_creature = Creature(size=np.mean(self.max_size, partner.max_size),
                                intelligence=np.mean(self.max_intelligence, partner.max_intelligence),
                                social=np.mean(self.max_social, partner.max_social),
                                digestion=np.mean(self.max_digestion, partner.max_digestion),
                                strength=np.mean(self.max_strength, partner.max_strength),
                                speed=np.mean(self.max_speed, partner.max_speed),
                                dexterity=np.mean(self.max_dexterity, partner.max_dexterity),
                                sex_drive=np.mean(self.max_sex_drive, partner.max_sex_drive)
                                )
        return new_creature

    def grow(self):
        self.size = np.min(self.size * 1.1, self.max_size)
        self.speed = np.min(self.speed * 1.1, self.max_speed)
        self.strength = np.min(self.strength * 1.1, self.max_strength)
        # if creatures is almost grown up, activate its sexual behaviour
        if self.size > self.max_size * 0.7:
            self.sex_drive = self.max_sex_drive

    def learn(self):
        self.intelligence = np.min(self.intelligence * 1.1, self.max_intelligence)

    def train(self):
        self.dexterity = np.min(self.dexterity * 1.1, self.max_dexterity)

    def drink(self, amount):
        self.thirst = np.min(self.thirst + amount / self.weight, 1)

    def eat(self, amount, food_type):
        if food_type == "creature":
            digest_efficiency = (self.digestion + 1) / 2
        elif food_type == "plant":
            digest_efficiency = (-self.digestion + 1) / 2
        else:
            digest_efficiency = 0

        self.hunger = np.min(self.hunger + amount * digest_efficiency / self.weigth, 1)

