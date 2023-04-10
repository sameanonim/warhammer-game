# Импортировать необходимые модули из SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Создать базовый класс для моделей данных
Base = declarative_base()

# Создать таблицу unit_weapon для связи между юнитами и оружием
unit_weapon = Table('unit_weapon', Base.metadata,
    Column('unit_id', Integer, ForeignKey('unit.id'), primary_key=True),
    Column('weapon_id', Integer, ForeignKey('weapon.id'), primary_key=True)
)

# Создать таблицу unit_psychic_power для связи между юнитами и психическими способностями
unit_psychic_power = Table('unit_psychic_power', Base.metadata,
    Column('unit_id', Integer, ForeignKey('unit.id'), primary_key=True),
    Column('psychic_power_id', Integer, ForeignKey('psychic_power.id'), primary_key=True)
)

# Создать таблицу unit_special_rule для связи между юнитами и специальными правилами
unit_special_rule = Table('unit_special_rule', Base.metadata,
    Column('unit_id', Integer, ForeignKey('unit.id'), primary_key=True),
    Column('special_rule_id', Integer, ForeignKey('special_rule.id'), primary_key=True)
)

# Создать таблицу weapon_special_rule для связи между оружиями и специальными правилами
weapon_special_rule = Table('weapon_special_rule', Base.metadata,
    Column('weapon_id', Integer, ForeignKey('weapon.id'), primary_key=True),
    Column('special_rule_id', Integer, ForeignKey('special_rule.id'), primary_key=True)
)

class Unit(Base):
    # Определить имя таблицы в базе данных
    __tablename__ = 'unit'

    # Определить атрибуты класса, соответствующие столбцам в таблице
    id = Column(Integer, primary_key=True) # первичный ключ
    name = Column(String, unique=True) # имя юнита
    movement = Column(Integer) # скорость передвижения
    melee_skill = Column(Integer) # навык в рукопашном бою
    shooting_skill = Column(Integer) # точность в дальнем бою
    strength = Column(Integer) # сила юнита
    toughness = Column(Integer) # стойкость юнита
    wounds = Column(Integer) # количество урона перед смертью
    attacks = Column(Integer) # количество ударов в рукопашном бою
    leadership = Column(Integer) # храбрость и решительность юнита
    save = Column(Integer) # защита от урона
    faction_id = Column(Integer, ForeignKey('faction.id')) # внешний ключ

    # Определить отношение многие ко многим с классом Weapon через таблицу unit_weapon
    weapons = relationship('Weapon', secondary=unit_weapon, back_populates='units')
    psychic_powers = relationship('PsychicPower', secondary=unit_psychic_power, back_populates='units')

    # Определить метод __repr__ для представления объекта класса в виде строки
    def __repr__(self):
        return f'<Unit(name={self.name}, movement={self.movement}, melee_skill={self.melee_skill}, shooting_skill={self.shooting_skill}, strength={self.strength}, toughness={self.toughness}, wounds={self.wounds}, attacks={self.attacks}, leadership={self.leadership}, save={self.save})>'

# Создать класс PsychicPower для представления психической способности в игре
class PsychicPower(Base):
    # Определить имя таблицы в базе данных
    __tablename__ = 'psychic_power'

    # Определить атрибуты класса, соответствующие столбцам в таблице
    id = Column(Integer, primary_key=True) # первичный ключ
    name = Column(String, unique=True) # имя психической способности
    type = Column(String) # тип психической способности
    range = Column(Integer) # дальность действия психической способности
    warp_charge = Column(Integer) # количество энергии Искажения для активации психической способности
    effect = Column(String) # описание эффекта психической способности

    # Определить отношение многие ко многим с классом Unit через таблицу unit_psychic_power
    units = relationship('Unit', secondary=unit_psychic_power, back_populates='psychic_powers')

    # Определить метод __repr__ для представления объекта класса в виде строки
    def __repr__(self):
        return f'<PsychicPower(name={self.name}, type={self.type}, range={self.range}, warp_charge={self.warp_charge}, effect={self.effect})>'
     
# Создать класс Weapon для представления оружия в игре
class Weapon(Base):
    # Определить имя таблицы в базе данных
    __tablename__ = 'weapon'

    # Определить атрибуты класса, соответствующие столбцам в таблице
    id = Column(Integer, primary_key=True) # первичный ключ
    name = Column(String, unique=True) # имя оружия
    type = Column(String) # тип оружия
    range = Column(Integer) # дальность стрельбы
    shots = Column(Integer) # количество выстрелов за ход
    strength = Column(Integer) # сила оружия
    armor_piercing = Column(Integer) # способность пробивать броню
    damage = Column(Integer) # количество урона

    # Определить отношение многие ко многим с классом Unit через таблицу unit_weapon
    units = relationship('Unit', secondary=unit_weapon, back_populates='weapons')

    # Определить метод __repr__ для представления объекта класса в виде строки
    def __repr__(self):
        return f'<Weapon(name={self.name}, type={self.type}, range={self.range}, shots={self.shots}, strength={self.strength}, armor_piercing={self.armor_piercing}, damage={self.damage})>'

class SpecialRule(Base):
    # Определить имя таблицы в базе данных
    __tablename__ = 'special_rule'

    # Определить атрибуты класса, соответствующие столбцам в таблице
    id = Column(Integer, primary_key=True) # первичный ключ
    name = Column(String, unique=True) # имя специального правила
    description = Column(String) # описание специального правила

    # Определить отношение многие ко многим с классом Unit через таблицу unit_special_rule
    units = relationship('Unit', secondary=unit_special_rule, back_populates='special_rules')

# Создать класс Faction для представления фракции в игре
class Faction(Base):
    # Определить имя таблицы в базе данных
    __tablename__ = 'faction'

    # Определить атрибуты класса, соответствующие столбцам в таблице
    id = Column(Integer, primary_key=True) # первичный ключ
    name = Column(String, unique=True) # имя фракции
    description = Column(String) # описание фракции

    # Определить отношение один ко многим с классом Unit через внешний ключ faction_id
    units = relationship('Unit', backref='faction')

    # Определить метод __repr__ для представления объекта класса в виде строки
    def __repr__(self):
        return f'<Faction(name={self.name}, description={self.description})>'