# Импортируем модуль random для работы с случайными числами
import random
from unittest import result
import math

# Определяем класс Unit
class Unit:
    # Инициализируем атрибуты юнита
    def __init__(self,
                 name: str,
                 faction: str,
                 model: str,
                 movement: int,
                 weapon_skill: int,
                 ballistic_skill: int,
                 strength: int,
                 toughness: int,
                 wounds: int,
                 attacks: int,
                 leadership: int,
                 save: int,
                 invulnerable_save: int or None,
                 weapons: list[Weapon],
                 abilities: list[Ability]):
        self.name = name # Имя юнита
        self.faction = faction # Фракция юнита
        self.model = model # Имя 3D модели юнита
        self.movement = movement # Скорость перемещения юнита в дюймах
        self.weapon_skill = weapon_skill # Навык стрельбы юнита (от 1 до 6)
        self.ballistic_skill = ballistic_skill # Навык ближнего боя юнита (от 1 до 6)
        self.strength = strength # Сила юнита (от 1 до 10)
        self.toughness = toughness # Выносливость юнита (от 1 до 10) 
        self.wounds = wounds # Количество ран юнита (от 1 до бесконечности)
        self.attacks = attacks # Количество атак юнита в ближнемs бою (от 1 до бесконечности)
        self.leadership = leadership # Лидерство юнита (от 1 до 10)
        self.save = save # Спасбросок юнита (от 2+ до 6+)
        self.invulnerable_save = invulnerable_save # Непробиваемый спасбросок юнита (от 2+ до 6+ или None, если нет)
        self.weapons = weapons # Список оружия юнита
        self.abilities = abilities # Список способностей юнита
#Определяем метод для получения значения характеристики по ее имени
    def get_stat(self, stat: str) -> int: # Если характеристика есть в атрибутах юнита, возвращаем ее значение
        if hasattr(self, stat):
            return getattr(self, stat)
        else:
            return 0 # Если это так, возвращаем 0
#Определяем метод для изменения значения характеристики по ее имени
    def set_stat(self, stat: str) -> int:
        if hasattr(self, stat):
            return getattr(self, stat)
        else:
            return 0
#Определяем метод для проверки жив ли юнит
    def is_alive(self) -> bool: # Проверяем статус юнита
        return self.wounds > 0
#Определяем метод для получения списка оружия определенного типа
    def get_weapons_by_type(self, type:str) -> list[Weapon]:
        result = [] # Создаем пустой список для результа
        # Создаем пустой список для результата result = [] # Проходим по всему оружию юнита
        for weapon in self.weapons: # Перебираем список всего оружия
            # Если тип оружия совпадает с заданным, добавляем его в список
            if weapon.type == type: 
                result.append(weapon)
            # Возвращаем список оружия юнита по
            return result
#Определяем метод для получения списка способностей с определенным условием
    def get_abilities_by_condition(self, condition: Condition) -> list[Ability]:
        result = []
    # Проходим по всем способностям юнита
        for ability in self.abilities: # Перебираем список способностей
            if ability.condition == condition: 
                result.append(ability)
            return result
        
# Определяем метод для получения списка способностей с определенным эффектом
def get_abilities_by_effect(self, effect: Effect) -> list[Ability]:
    # Создаем пустой список для результата
    result = []
    # Проходим по всем способностям юнита
    for ability in self.abilities:
        # Если эффект способности совпадает с заданным, добавляем ее в список
        if ability.effect == effect:
            result.append(ability)
    # Возвращаем список
    return result

# Определяем метод для получения списка эффектов оружия с определенным типом
def get_weapon_effects_by_type(self, type: str) -> list[Effect]:
    # Создаем пустой список для результата
    result = []
    # Проходим по всему оружию юнита
    for weapon in self.weapons:
        # Проходим по всем эффектам оружия
        for effect in weapon.effects:
            # Если тип эффекта совпадает с заданным, добавляем его в список
            if effect.type == type:
                result.append(effect)
    # Возвращаем список
    return result

# Определяем метод для получения списка эффектов способностей с определенным типом
def get_ability_effects_by_type(self, type: str) -> list[Effect]:
    # Создаем пустой список для результата
    result = []
    # Проходим по всем способностям юнита
    for ability in self.abilities:
        # Если способность имеет эффект и его тип совпадает с заданным, добавляем его в список
        if ability.effect and ability.effect.type == type:
            result.append(ability.effect)
    # Возвращаем список
    return result

# Определяем метод для получения общего списка эффектов юнита с определенным типом (из оружия и способностей)
def get_effects_by_type(self, type: str) -> list[Effect]:
    # Складываем списки эффектов оружия и способностей с заданным типом и возвращаем результат
    return self.get_weapon_effects_by_type(type) + self.get_ability_effects_by_type(type)

class Weapon:
    # Инициализируем атрибуты оружия
    def init(self, type: str,
             name: str,
             range: int or None,
             shots: int or str,
             strenght: int or str,
             armor_penetration: int,
             damage: int or str,
             effects: list[Effect]):
        self.name = name
        self.type = type
        self.range = range
        self.shots = shots
        self.strenght = strenght  # сила
        self.armor_penetration = armor_penetration
        self.damage = damage  # урон от оружия
        self.effects = effects  # эффект оружия

def get_stats(self, stat: str) -> int or str:
    if hasattr(self, stat):
        return getattr(self, stat)
    else:
        return 0
    
def set_stat(self, stat: str, value: int or str) -> None:
    if hasattr(self, stat):
        setattr(self, stat, value)

def get_effects_by_type(self, type: str) -> list[Effect]:  # список эффектов с типом оружия
    result = []
    for effect in self.effects:  # список эффектов
        if effect.type == type:
            result.append(effect)  # список эффектов
        return result
    
class Abilty:
    def init(self,
             name: str,
             description: str,
             condition: Condition or None,
             effect: Effect or None):
        self.namme = name
        self.description = description  # список условий с учето
        self.condition = condition  # управление условиями с
        self.effect = effect  # список эффектов

class Condition:
    def init(self, type: str, parameters: dict[str, any]):
        self.type = type
        self.parameters = parameters

# Определяем метод для проверки выполнения условия
def check(self) -> bool:
    # В зависимости от типа условия применяем разную логику проверки
    if self.type == "phase":
        # Проверяем, что текущая фаза игры совпадает с заданной в параметрах
        return game.phase.name == self.parameters["name"]
    elif self.type == "distance":
        # Проверяем, что расстояние между двумя объектами в игре меньше или равно заданному в параметрах
        return game.get_distance(self.parameters["object1"], self.parameters["object2"]) <= self.parameters["value"]
    elif self.type == "roll":
        # Проверяем, что последний бросок кубика удовлетворяет заданному в параметрах условию (например, ">3" или "==6")
        return eval(str(game.last_roll) + self.parameters["value"])
    else:
        # Если тип условия неизвестен, возвращаем False
        return False
    
class Effect:
    def init(self, type: str, parameters dict[str, any]):
        self.type = type # Тип эффекта (например, “reroll”, “modify”, “wound” и т.д.)
        self.parameters = parameters #Словарь параметров эффекта (например, {“dice”: “1”, “value”: “<=3”} для эффекта типа “reroll”)

# Определяем метод для применения эффекта к соответствующим объектам или броскам кубиков
def apply(self) -> None:
    # В зависимости от типа эффекта применяем разную логику применения
    if self.type == “reroll”: # Повторяем бросок кубика с заданным номером в последнем броске, если он удовлетворяет заданному условию (например, “<=3”)
        dice = int(self.parameters["dice"]) - 1