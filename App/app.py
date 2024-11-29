import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db

APP = Flask(__name__,static_folder='css')

# Start page
@APP.route('/')
def index():
    '''cursor = db.execute
    SELECT *
    FROM TEST
    
    columns = [name[0] for name in cursor.description]
    data = cursor.fetchall()
    logging.info(data)'''
    return render_template('index.html')

@APP.route('/search')
# Search page
def search():
    return render_template('search.html')

@APP.route('/stats')
# Statistics page
def stats():
    return render_template('stats.html')

@APP.route('/about')
# About page
def about():
    return render_template('about.html')

@APP.route('/countries', methods=['GET','POST'])
# Search Country
def countries():
    query = '''SELECT 
                    *
                FROM
                    Countries c
                JOIN
                    MetaDetails m ON m.countryID = c.countryID
                WHERE 
                    1=1'''
    filters = []
    countries = []
    if request.method == 'POST':
        name = request.form.get('name')
        min_tax_rate = request.form.get('min_tax_rate')
        max_tax_rate = request.form.get('max_tax_rate')
        continent = request.form.get('continent')
        if name:
            query += " AND c.name LIKE ?"
            filters.append(f"%{name}%")
        if min_tax_rate:
            query += " AND ? <= m.tax_rate"
            filters.append(float(min_tax_rate))
        if max_tax_rate:
            query += " AND m.tax_rate <= ?"
            filters.append(float(max_tax_rate))
        if continent:
            query += " AND c.continent like ?"
            filters.append(continent)
    result = db.execute(query, tuple(filters))
    countries = result.fetchall()
    return render_template('search-country.html', countries=countries)    

@APP.route('/billionaires', methods=['GET','POST'])
# Search Billionaire
def billionaires():
    query = '''SELECT b.*, (CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', b.birth_date) AS INTEGER)) AS age
             FROM Billionaires b
             WHERE 1=1'''
    filters = []
    billionaires = []
    if request.method == 'POST':
        name = request.form.get('name')
        min_age = request.form.get('min_age')
        max_age = request.form.get('max_age')
        min_money = request.form.get('min_money')
        max_money = request.form.get('max_money')
        gender = request.form.get('gender')
        if name:
            query += " AND ((b.first_name LIKE ?) or (b.last_name LIKE ?))"
            filters.append(f"%{name}%")
            filters.append(f"%{name}%")
        
        if min_age:
            query += " AND (CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', b.birth_date) AS INTEGER)) <= ?"
            filters.append(int(min_age))
        
        if max_age:
            query += " AND (CAST(strftime('%Y', 'now') AS INTEGER) - CAST(strftime('%Y', b.birth_date) AS INTEGER)) <= ?"
            filters.append(int(max_age))
        
        if min_money:
            # int ou float?
            query += " AND b.wealth >= ?"
            filters.append(float(min_money))
        
        if max_money:
            query += " AND b.wealth <= ?"
            filters.append(float(max_money))
        if gender:
            query += " AND b.gender = ?"
            filters.append(gender)
    result = db.execute(query, tuple(filters))
    billionaires = result.fetchall()
    return render_template('search-billionaires.html', billionaires=billionaires)



@APP.route('/billionaires/<int:id>')
# Billionaire Info
def billionarie_info(id):
    query
    return render_template('billionaire-info.html')


@APP.route('/country/<int:id>')
# Country Info
def country_info(name):

    return render_template('country-info.html')
