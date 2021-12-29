"""
Routes and views for the flask application.
"""

import os

from flask import Flask
from flask import render_template, jsonify, redirect, url_for, request
#from flask_restplus import Api, Resource

from datetime import datetime
from flasgger import Swagger
from Country import app
import sqlite3 as sql

Swagger(app)

def connect_db():  
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "country.db")
    conn = sql.connect (db_path)
    conn.row_factory = sql.Row
    return conn

@app.route('/list')
def list():
    """
        Возвращает список строк или кортежей. У каждого кортеже(объекта) 6 атрибутов.
        ---
        tags:
            - list
        parameters: []
        definitions:
            List:
                type: array
                items: 
                    type: object
                    properties:
                        id_country:
                            type: integer
                        country:
                            type: string
                        capital:
                            type: string
                        population:
                            type: integer
                        language:
                            type: string
                        square:
                            type: integer                       
        responses:
            200:
                description: Возвращает списосок кортежей БД
                schema:
                    $ref: '#/definitions/List'
                examples:
                    version: '1.0'
    """
    conn = connect_db()
    rows = conn.execute ( "SELECT * FROM country" ).fetchall()
    conn.close()
    return rows

@app.route('/get_list')
def get_list(id):
    """
        Возвращает строку из базы данных по указанному id.
        ---
        tags:
            - get_list
        parameters: []
        definitions:
            getList:
                type: array
                items: 
                    type: object
                    properties:
                        country:
                            type: string
                        capital:
                            type: string
                        population:
                            type: integer
                        language:
                            type: string
                        square:
                            type: integer                       
        responses:
            200:
                description: Возвращает выбранную строку из БД
                schema:
                    $ref: '#/definitions/get_list'
                examples:
                    version: '1.0'
    """
    conn = connect_db()
    rows = conn.execute ('SELECT * FROM country WHERE id_country = ?', (id,)).fetchone()
    conn.close()
    return rows

@app.route('/list_MAXpopulation')
def list_MAXpopulation():
    """
        Возвращает из БД кортеж с максимальным значение поля "population".
        ---
        tags:
            - MAXpopulation
        parameters: []
        definitions:
            Tuple:
                type: object
                properties:
                    id_country:
                        type: integer
                    country:
                        type: string
                    capital:
                        type: string
                    population:
                        type: integer
                    language:
                        type: string
                    square:
                        type: integer                       
        responses:
            200:
                description: Кортеж с максимальным значением поля "population"
                schema:
                    $ref: '#/definitions/MAXpopulation'
                examples:
                    version: '1.0'
    """
    conn = connect_db()
    rows = conn.execute ( "select * from country where population in (select max(population) as max from country)" ).fetchall()
    conn.close()
    return rows

@app.route('/list_MINpopulation')
def list_MINpopulation():
    """
        Возвращает из БД кортеж с минимальным значение поля "population".
        ---
        tags:
            - MINpopulation
        parameters: []
        definitions:
            Tuple:
                type: object
                properties:
                    id_country:
                        type: integer
                    country:
                        type: string
                    capital:
                        type: string
                    population:
                        type: integer
                    language:
                        type: string
                    square:
                        type: integer                       
        responses:
            200:
                description: Кортеж с минимальным значением поля "population"
                schema:
                    $ref: '#/definitions/MINpopulation'
                examples:
                    version: '1.0'
    """
    conn = connect_db()
    rows = conn.execute ( "select * from country where population in (select min(population) as min from country)" ).fetchall();
    conn.close()
    return rows

@app.route('/list_MAXsquare')
def list_MAXsquare():
    """
        Возвращает из БД кортеж с максимальным значение поля "square".
        ---
        tags:
            - MAXsquare
        parameters: []
        definitions:
            Tuple:
                type: object
                properties:
                    id_country:
                        type: integer
                    country:
                        type: string
                    capital:
                        type: string
                    population:
                        type: integer
                    language:
                        type: string
                    square:
                        type: integer                       
        responses:
            200:
                description: Кортеж с максимальным значением поля "square"
                schema:
                    $ref: '#/definitions/MAXsquare'
                examples:
                    version: '1.0'
    """
    conn = connect_db()
    rows = conn.execute ( "select * from country where square in (select max(square) as max from country)" ).fetchall();
    conn.close()
    return rows

@app.route('/list_MINsquare') 
def list_MINsquare():
    """
        Возвращает из БД кортеж с минимальным значение поля "square".
        ---
        tags:
            - MINsquare
        parameters: []
        definitions:
            Tuple:
                type: object
                properties:
                    id_country:
                        type: integer
                    country:
                        type: string
                    capital:
                        type: string
                    population:
                        type: integer
                    language:
                        type: string
                    square:
                        type: integer                       
        responses:
            200:
                description: Кортеж с минимальным значением поля "square"
                schema:
                    $ref: '#/definitions/MINsquare'
                examples:
                    version: '1.0'
    """
    conn = connect_db()
    rows = conn.execute ( "select * from country where square in (select min(square) as min from country)" ).fetchall();
    conn.close()
    return rows


#Добавления записи через REST API
@app.route('/createaAPI', methods=['POST'])
def createAPI():
    """
        Добавить запись в БД REST API.
        ---
        tags:
            - createApi
        parameters: 
            - in: "body"
              name: "body"
              required: true
              schema:
                type: "object"
                required:
                  - POST
                properties:
                  country:
                    type: string
                    example: "Болгария"
                  capital:
                    type: string
                    example: "София"
                  population:
                    type: integer
                    example: 6875040
                  language:
                    type: string
                    example: "Болгарский"
                  square:
                    type: integer 
                    example: 110993
        responses:
            200:
                description: 
                    Запись успешно добавленна
        
    """
    if request.method == 'POST':
        post_data = request.get_json()
        country = post_data['country']
        capital = post_data['capital']
        population = post_data['population']
        language = post_data['language']
        square = post_data['square']

        if not country:
            flash('Название страны обязательно!')
        else:
            conn = connect_db()
            conn.execute('INSERT INTO country (country, capital, population, language, square) VALUES (?, ?, ?, ?, ?)',
                         (country, capital, population, language, square))
            
            conn.commit()
            conn.close()
            answer = "Запись успешно добавленна"
            return answer
            #return jsonify(url_for('home'))
            #return redirect(url_for('home'))

#REST API обновление записи по id
@app.route('/<int:id>/editAPI', methods=['PUT'])
def editAPI(id):
    """
        Обновить запись в БД REST API.
        ---
        tags:
            - editApi
        parameters:
            - in: "path"
              name: "id"
            - in: "body"
              name: "body"
              required: true
              schema:
                type: "object"
                required:
                  - PUT
                properties:
                  country:
                    type: string
                    example: "Израиль"
                  capital:
                    type: string
                    example: "Иерусалим"
                  population:
                    type: integer
                    example: 9291000
                  language:
                    type: string
                    example: "иврит"
                  square:
                    type: integer 
                    example: 20770
        responses:
            200:
                description: 
                    Запись успешно объновленна
        
    """
    line = get_list(id)

    #Формат передаваемого файла машиной - json
    if request.method == 'PUT':
        post_data = request.get_json()
        country = post_data['country']
        capital = post_data['capital']
        population = post_data['population']
        language = post_data['language']
        square = post_data['square']

        if not country:
            flash('Название страны обязательно!')
        else:
            conn = connect_db()
            conn.execute('UPDATE country SET country = ?, capital = ?, population = ?, language = ?, square = ?'
                         ' WHERE id_country = ?',
                         (country, capital, population, language, square, id))
            
            conn.commit()
            conn.close()
            answer = "Запись успешно объновленна"
            return answer


#REST API Удаление запись в БД по id
@app.route('/<int:id>/deleteAPI', methods=['DELETE'])
def deleteAPI(id):
    """
        Удалить запись в БД REST API.
        ---
        tags:
            - deleteApi
        parameters:
            - in: "path"
              name: "id"
        responses:
            200:
                description: 
                    Запись успешно удалена
        
    """
    conn = connect_db()
    conn.execute('DELETE FROM country WHERE id_country = ?', (id,))
    conn.commit()
    conn.close()
    answer = "Запись успешно удалена"
    return answer


#Добавить запись через форму
@app.route('/create', methods=('GET', 'POST'))
def create():
    
    if request.method == 'POST':
        country = request.form['country']
        capital = request.form['capital']
        population = request.form['population']
        language = request.form['language']
        square = request.form['square']

        if not country:
            flash('Название страны обязательно!')
        else:
            conn = connect_db()
            conn.execute('INSERT INTO country (country, capital, population, language, square) VALUES (?, ?, ?, ?, ?)',
                         (country, capital, population, language, square))
            
            conn.commit()
            conn.close()
            return redirect(url_for('home'))

    return render_template(
        'create.html',
        title='Добавить страну',
    )


#Редактирование записи через форму
@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):  
    line = get_list(id)
    if request.method == 'POST':
        country = request.form['country']
        capital = request.form['capital']
        population = request.form['population']
        language = request.form['language']
        square = request.form['square']

        if not country:
            flash('Название страны обязательно!')
        else:
            conn = connect_db()
            conn.execute('UPDATE country SET country = ?, capital = ?, population = ?, language = ?, square = ?'
                         ' WHERE id_country = ?',
                         (country, capital, population, language, square, id))
            
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
    
    return render_template(
        'edit.html',
        line = line,
        title='Редактировать объект'
    )

#Удалить запись используя форму
#Возвращает список строк или кортежей. У каждого кортеже(объекта) 6 атрибутов.
@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    conn = connect_db()
    conn.execute('DELETE FROM country WHERE id_country = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))



@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        title='Список всех стран',
        #rr = r,
        list = list(),
        year=datetime.now().year,
    )

@app.route('/square')
def square():
    return render_template(
        'square.html', 
        title='Страны с большей и меньшей площадью',
        squareMAX = list_MAXsquare(),
        squareMIN = list_MINsquare(),
        year=datetime.now().year,
    )

@app.route('/population')
def population():
    return render_template(
        'population.html',
        title='Страны с большей и меньшей численностью населения',
        populationMAX = list_MAXpopulation(),
        populationMIN = list_MINpopulation(),
        year=datetime.now().year,
    )