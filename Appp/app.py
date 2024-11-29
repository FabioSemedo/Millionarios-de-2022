import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db

APP = Flask(__name__,static_folder='css')

# Start page
@APP.route('/')
def index():
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
                    EconomicDetails m ON m.countryID = c.countryID
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
    query = '''SELECT b.*, (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) as age
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
           query += " AND (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) = ?"
           filters.append(int(min_age))
        
        if max_age:
            query += " AND (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) = ?"
            filters.append(int(max_age))
        
        if min_money:
            query += " AND b.wealth >= ?"
            filters.append(int(min_money))
        
        if max_money:
            query += " AND b.wealth <= ?"
            filters.append(int(max_money))
        if gender:
            query += " AND b.gender = ?"
            filters.append(gender)
    query += " ORDER BY b.first_name, b.last_name"        
    result = db.execute(query, tuple(filters))
    billionaires = result.fetchall()
    return render_template('search-billionaires.html', billionaires=billionaires)



@APP.route('/billionaires/<int:id>')
# Billionaire Info
def billionarie_info(id):

    # billionaire
    query_billionaire = '''SELECT
                               *
                           FROM
                               Billionaires b
                           WHERE
                               b.personId = ?
                        '''
    billionaire = db.execute(query_billionaire,[id]).fetchone()

    #country
    query_country = '''SELECT
                           c.name
                        FROM
                            Billionaires b
                        JOIN
                            Countries c ON b.citizenshipID = c.countryID
                        WHERE
                            b.personId = ?
                    '''
    country = db.execute(query_country,[id]).fetchone()

    #source
    source_query = '''SELECT
                          s.source
                      FROM
                          Billionaires b
                      JOIN
                          Activities a ON b.personId = a.personId
                      JOIN 
                          SourcesOfWealth s ON a.sourceID = s.sourceID
                      WHERE
                          b.personId = ?
                   '''
    source = db.execute(source_query,[id]).fetchone()

    #city
    city_query = '''SELECT
                        c.name
                    FROM
                        Billionaires b 
                    JOIN
                        Cities c on c.cityID = b.cityID
                    WHERE
                        b.personId = ?
                  '''
    city = db.execute(city_query,[id]).fetchone()
    print(billionaire)
    return render_template('billionaire-info.html',billionaire=billionaire,country=country,source=source,city=city)


@APP.route('/countries/<int:id>')
# Country Info
def country(id):
    return render_template('country-info-split.html',countryID=id)


@APP.route('/country/<int:id>/geographic')
def geographic(id):
    query = '''SELECT
                   *
               FROM
                   Countries c
               WHERE
                   c.countryID = ?               
           '''
    country = db.execute(query,[id]).fetchone()
    return render_template('country-geographic.html', country=country)


@APP.route('/country/<int:id>/economy')
def economy(id):
    query = '''SELECT
                   *
               FROM
                   Countries c
               JOIN 
                   EconomicDetails e ON c.countryID = e.countryID
               WHERE
                   c.countryID = ?               
           '''
    country = db.execute(query,[id]).fetchone()
   
    return render_template('country-economy.html', country=country)

@APP.route('/cities')
def cities():
    
    return render_template('search-cities.html')




@APP.route('/cities/<int:id>')
def cities_info(id):
    
    return render_template('cities-info.html')
