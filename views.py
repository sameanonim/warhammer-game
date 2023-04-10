# Импортировать необходимые модули из Flask и SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re

# Импортировать модели данных из файла models.py
from models import Base, Unit, Weapon, PsychicPower, SpecialRule, Faction

# Создать объект app для приложения Flask
app = Flask(__name__)

# Создать объект engine для подключения к базе данных PostgreSQL
engine = create_engine('postgresql://warhammer_user:warhammer_password@localhost/warhammer')

# Создать объект Session для работы с данными в базе данных
Session = sessionmaker(bind=engine)
session = Session()

# Определить функцию index(), которая будет отображать главную страницу приложения
@app.route('/')
def index():
    # Получить список всех фракций из базы данных
    factions = session.query(Faction).all()

    # Отрендерить шаблон index.html с передачей списка фракций в качестве аргумента
    return render_template('index.html', factions=factions)

# Определить функцию faction(), которая будет отображать страницу с информацией о выбранной фракции и ее юнитах
@app.route('/faction/<int:faction_id>')
def faction(faction_id):
    # Получить объект фракции по ее id из базы данных
    faction = session.query(Faction).get(faction_id)

    # Если фракция не найдена, то вернуть 404 ошибку
    if faction is None:
        return 'Faction not found', 404

    # Получить список юнитов фракции из базы данных
    units = session.query(Unit).filter(Unit.faction_id == faction_id).all()

    # Отрендерить шаблон faction.html с передачей объекта фракции и списка юнитов в качестве аргументов
    return render_template('faction.html', faction=faction, units=units)

# Определить функцию unit(), которая будет отображать страницу с информацией о выбранном юните и его характеристиках
@app.route('/unit/<int:unit_id>')
def unit(unit_id):
    # Получить объект юнита по его id из базы данных
    unit = session.query(Unit).get(unit_id)

    # Если юнит не найден, то вернуть 404 ошибку
    if unit is None:
        return 'Unit not found', 404

    # Получить список оружия юнита из базы данных
    weapons = session.query(Weapon).filter(Weapon.units.any(id=unit_id)).all()

    # Получить список психических способностей юнита из базы данных
    psychic_powers = session.query(PsychicPower).filter(PsychicPower.units.any(id=unit_id)).all()

    # Получить список специальных правил юнита из базы данных
    special_rules = session.query(SpecialRule).filter(SpecialRule.units.any(id=unit_id)).all()

    # Отрендерить шаблон unit.html с передачей объекта юнита и списков оружия, психических способностей и специальных правил в качестве аргументов
    return render_template('unit.html', unit=unit, weapons=weapons, psychic_powers=psychic_powers, special_rules=special_rules)

# Определить функцию create_unit(), которая будет обрабатывать запросы на создание нового юнита в базе данных
@app.route('/create_unit', methods=['GET', 'POST'])
def create_unit():
    # Если запрос имеет метод GET, то отрендерить шаблон create_unit.html с передачей списка фракций в качестве аргумента
    if request.method == 'GET':
        factions = session.query(Faction).all()
        return render_template('create_unit.html', factions=factions)

    # Если запрос имеет метод POST, то получить данные из формы и создать новый объект класса Unit с этими данными
    if request.method == 'POST':
        name = request.form.get('name')
        movement = request.form.get('movement')
        melee_skill = request.form.get('melee_skill')
        shooting_skill = request.form.get('shooting_skill')
        strength = request.form.get('strength')
        toughness = request.form.get('toughness')
        wounds = request.form.get('wounds')
        attacks = request.form.get('attacks')
        leadership = request.form.get('leadership')
        save = request.form.get('save')
        faction_id = request.form.get('faction_id')

        new_unit = Unit(name=name, movement=movement, melee_skill=melee_skill, shooting_skill=shooting_skill,
                        strength=strength, toughness=toughness, wounds=wounds, attacks=attacks,
                        leadership=leadership, save=save, faction_id=faction_id)

        # Добавить новый объект класса Unit в сессию и сохранить изменения в базе данных
        session.add(new_unit)
        session.commit()

        # Перенаправить пользователя на страницу с информацией о созданном юните
        return redirect(url_for('unit', unit_id=new_unit.id))
    
# Определить функцию delete_unit(), которая будет обрабатывать запросы на удаление существующего юнита из базы данных
@app.route('/delete_unit/<int:unit_id>', methods=['POST'])
def delete_unit(unit_id):
    # Получить объект юнита по его id из базы данных
    unit = session.query(Unit).get(unit_id)

    # Если юнит не найден, то вернуть 404 ошибку
    if unit is None:
        return 'Unit not found', 404

    # Удалить объект юнита из сессии и базы данных
    session.delete(unit)
    session.commit()

    # Перенаправить пользователя на главную страницу приложения
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    # Если запрос имеет метод GET, то отрендерить шаблон search.html
    if request.method == 'GET':
        return render_template('search.html')

    # Если запрос имеет метод POST, то получить данные из формы и выполнить поиск юнитов по имени
    if request.method == 'POST':
        query = request.form.get('query')
        # Если запрос пустой, то вернуть сообщение об ошибке
        if query == '':
            return 'Please enter a name to search', 400

        # Создать регулярное выражение для поиска юнитов, чье имя содержит запрос в любом регистре
        pattern = re.compile(query, re.IGNORECASE)

        # Получить список всех юнитов из базы данных
        units = session.query(Unit).all()

        # Создать пустой список для хранения найденных юнитов
        results = []

        # Пройтись по списку всех юнитов и проверить, соответствует ли их имя регулярному выражению
        for unit in units:
            if pattern.search(unit.name):
                # Если да, то добавить юнит в список результатов
                results.append(unit)

        # Отрендерить шаблон results.html с передачей списка результатов в качестве аргумента
        return render_template('results.html', results=results)
    
# Определить функцию filter(), которая будет обрабатывать запросы на фильтрацию юнитов по фракции
@app.route('/filter', methods=['GET', 'POST'])
def filter():
    # Если запрос имеет метод GET, то отрендерить шаблон filter.html с передачей списка фракций в качестве аргумента
    if request.method == 'GET':
        factions = session.query(Faction).all()
        return render_template('filter.html', factions=factions)

    # Если запрос имеет метод POST, то получить данные из формы и выполнить фильтрацию юнитов по фракции
    if request.method == 'POST':
        faction_id = request.form.get('faction_id')
        # Если id фракции не выбран, то вернуть сообщение об ошибке
        if faction_id == '':
            return 'Please select a faction to filter', 400

        # Получить список юнитов, принадлежащих выбранной фракции из базы данных
        units = session.query(Unit).filter(Unit.faction_id == faction_id).all()

        # Отрендерить шаблон results.html с передачей списка юнитов в качестве аргумента
        return render_template('results.html', results=units)