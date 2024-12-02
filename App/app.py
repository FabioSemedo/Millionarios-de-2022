import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db

APP = Flask(__name__,static_folder='css')
min_limit = "-1000000000000"
max_limit = "1000000000000"

# Start page
@APP.route('/')
def index():
    return render_template('index.html')



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

    continent = db.execute('''SELECT
                                  DISTINCT c.continent
                              FROM
                                  Countries c
                           ''').fetchall()
     
    filters = []
    countries = []
    if request.method == 'POST':
        name = request.form.get('name')
        min_tax_rate = request.form.get('min_tax_rate')
        max_tax_rate = request.form.get('max_tax_rate')
        min_tax_rev = request.form.get('min_tax_rev')
        max_tax_rev = request.form.get('max_tax_rev')
        min_cpi = request.form.get('min_cpi')
        max_cpi = request.form.get('max_cpi')
        min_change = request.form.get('min_change')
        max_change = request.form.get('max_change')
        min_gdp = request.form.get('min_gdp')
        max_gdp = request.form.get('max_gdp')
        min_trt = request.form.get('min_trt')
        max_trt = request.form.get('max_trt')
        min_prm = request.form.get('min_prm')
        max_prm = request.form.get('max_prm')
        continent_n = request.form.getlist('continent_filter[]')
        if name:
            query += " AND c.name LIKE ?"
            filters.append(f"%{name}%")

        if min_tax_rate:
            query += " AND ? <= m.tax_rate"
            filters.append(float(min_tax_rate))
        if max_tax_rate:
            query += " AND m.tax_rate <= ?"
            filters.append(float(max_tax_rate))
            
        if min_tax_rev:
            query += " AND ? <= m.tax_rev"
            filters.append(float(min_tax_rev))
        if max_tax_rev:
            query += " AND m.tax_rev <= ?"
            filters.append(float(max_tax_rev))
            
        if min_cpi:
            query += " AND ? <= m.cpi"
            filters.append(float(min_cpi))
        if max_cpi:
            query += " AND m.cpi <= ?"
            filters.append(float(max_cpi))

        if min_change:
            query += " AND ? <= m.cpi_change"
            filters.append(float(min_change))
        if max_change:
            query += " AND m.cpi_change <= ?"
            filters.append(float(max_change))

        if min_gdp:
            query += " AND ? <= m.gdp"
            filters.append(int(min_gdp))
        if max_gdp:
            query += " AND m.gdp <= ?"
            filters.append(int(max_gdp))

        if min_trt:
            query += " AND ? <= m.grs_trt_enroll"
            filters.append(float(min_trt))
        if max_trt:
            query += " AND m.grs_trt_enroll <= ?"
            filters.append(float(max_trt))

        if min_prm:
            query += " AND ? <= m.grs_prm_enroll"
            filters.append(float(min_prm))
        if max_prm:
            query += " AND m.grs_prm_enroll <= ?"
            filters.append(float(max_prm))
            
        if continent_n:
            placeholders = ', '.join(['?'] * len(continent_n))
            query += f" AND c.continent in ({placeholders})"
            filters.extend(continent_n)
            
    result = db.execute(query, tuple(filters))
    countries = result.fetchall()
    return render_template('search-country.html', countries=countries,continent=continent)    

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
            query += " AND b.wealth_millions >= ?"
            filters.append(int(min_money))
        
        if max_money:
            query += " AND b.wealth_millions <= ?"
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
def billionaire_info(id):

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
                          s.source, s.sourceID
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
    return render_template('billionaire-info.html',billionaire=billionaire,country=country,source=source,city=city)


@APP.route('/countries/<int:id>')
# Country Info
def country(id):
    return render_template('country-info-split.html',countryID=id)


@APP.route('/countries/<int:id>/geographic')
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


@APP.route('/countries/<int:id>/economy')
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

@APP.route('/cities', methods=['GET','POST'])
def cities():
    query = '''SELECT
                   c.name, c.cityID
               FROM
                   Cities c
               JOIN
                  (SELECT c2.countryID, c2.name as countryName FROM Countries c2) c1 ON c1.countryID = c.countryID
               WHERE
                   1 = 1
           '''
    filters = []
    cities = []
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        if name:
            query += "AND c.name LIKE ?"
            filters.append(f"%{name}%")
        if location:
            query += "AND c1.countryName LIKE ?"
            filters.append(f"%{location}%")
    result = db.execute(query,tuple(filters))
    cities = result.fetchall()
    return render_template('search-cities.html',cities=cities)




@APP.route('/cities/<int:id>')
def cities_info(id):
    city_query = '''SELECT
                        c.name, c1.countryName, c.countryID
                    FROM
                        Cities c
                    JOIN
                       (SELECT a.*,a.name AS countryName FROM Countries a) c1 ON c.countryID = c1.countryID
                    WHERE
                        c.cityID = ?
                 '''
    city = db.execute(city_query,[id]).fetchone()

    state_query = '''SELECT
                        s.state, s.region
                    FROM
                        USStates s 
                    JOIN 
                        USCities c ON s.stateID = c.stateID
                    
                    WHERE
                        c.cityID = ?
                 '''
    state = db.execute(state_query,[id]).fetchone()
    
    return render_template('cities-info.html',city=city,state=state)



@APP.route('/search', methods=['GET','POST'])
# Search page
def search():
    query = '''SELECT
                   b.personId, b.first_name, b.personId, b.last_name, c2.country, b.wealth_millions as wealth, 
                   c3.nationality,c2.continent, Group_Concat(s.source, ', ') as source
               FROM
                   Billionaires b
               JOIN
                   Cities c1 ON c1.cityID = b.cityID
               JOIN
                   (SELECT f1.continent, f1.countryID, f1.name as country FROM Countries f1) c2 ON c2.countryID = c1.countryID
               JOIN
                   (SELECT f2.countryID as nationalityID, f2.name as nationality FROM Countries f2) c3 ON c3.nationalityID = b.citizenshipID
               JOIN
                   Activities a ON a.personId = b.personId
               JOIN
                   (SELECT f3.sourceID, f3.source FROM SourcesOfWealth f3) s ON s.sourceID = a.sourceID
               WHERE 
                   1 = 1
            '''
    filters = []
    data = []
    aux = '''SELECT 
                  k1.cityID
              FROM
                  USCities k1
              JOIN
                  USStates k2 ON k1.stateID = k2.stateID
              WHERE
                  1 = 1
          ''' 
    country = db.execute('''SELECT
                                DISTINCT c.countryID, c.name
                            FROM
                                Countries c               
                         ''').fetchall()

    industry = db.execute('''SELECT
                                 DISTINCT b.industry
                             FROM
                                 Billionaires b
                          ''').fetchall()

    source = db.execute('''SELECT
                               s.*
                           FROM
                               SourcesOfWealth s
                        ''').fetchall()

    gender = db.execute('''SELECT
                               DISTINCT b.gender
                           FROM
                               Billionaires b
                       ''').fetchall()

    city = db.execute('''SELECT
                             DISTINCT c.cityID,c.name
                         FROM
                             Cities c
                      ''').fetchall()
    state = db.execute('''SELECT
                              DISTINCT s.stateID,s.state
                          FROM
                              USStates s
                       ''').fetchall()
    region = db.execute('''SELECT
                               DISTINCT s.region
                           FROM
                               USStates s
                        ''').fetchall()

    continent = db.execute('''SELECT
                                  DISTINCT c.continent
                              FROM
                                  Countries c
                           ''').fetchall()

    order_s = ""
    if request.method == 'POST':
        name = request.form.get('name')
        country_id = request.form.getlist('country_filter[]')
        min_age = request.form.get('min_age')
        max_age = request.form.get('max_age')
        min_money = request.form.get('min_money')
        max_money = request.form.get('max_money')
        gender_n = request.form.getlist('gender_filter[]')
        industry_n = request.form.getlist('industry_filter[]')
        source_id = request.form.getlist('source_filter[]')
        print(source_id)
        city_id = request.form.getlist('city_filter[]')
        state_id = request.form.getlist('state_filter[]')
        region_n = request.form.getlist('region_filter[]')
        continent_n = request.form.getlist('continent_filter[]')
        order_by = request.form.get('order_by')
        

        if name:
            query += " AND ((b.first_name LIKE ?) or (b.last_name LIKE ?))"
            filters.append(f"%{name}%")
            filters.append(f"%{name}%")
            
        if country_id:
            placeholders = ', '.join(['?'] * len(country_id))
            query += f" AND (c2.countryID IN ({placeholders}) OR b.citizenshipID IN ({placeholders})) "
            filters.extend(country_id)
            filters.extend(country_id)
        
        if min_age:
           query += " AND (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) = ?"
           filters.append(int(min_age))
        
        if max_age:
            query += " AND (CAST((JULIANDAY('now') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) = ?"
            filters.append(int(max_age))
        
        if min_money:
            query += " AND b.wealth_millions >= ?"
            filters.append(int(min_money))
        
        if max_money:
            query += " AND b.wealth_millions <= ?"
            filters.append(int(max_money))
        if gender_n:
            placeholders = ', '.join(['?'] * len(gender_n))
            query += f" AND b.gender IN ({placeholders})"
            filters.extend(gender_n)
        if industry_n:
            placeholders = ', '.join(['?'] * len(industry_n))
            query += f" AND b.industry IN ({placeholders})"
            filters.extend(industry_n)
        if source_id:
            placeholders = ', '.join(['?'] * len(source_id))
            query += f" AND a.sourceID IN ({placeholders})"
            filters.extend(source_id)
        if continent_n:
            placeholders = ', '.join(['?'] * len(continent_n))
            query += f" AND c2.continent IN ({placeholders})"
            filters.extend(continent_n)
        if order_by:
            if order_by == "wealth_desc":
                order_s = " ORDER BY b.wealth_millions DESC"
            if order_by == "wealth_asc":
                order_s = " ORDER BY b.wealth_millions ASC"
            if order_by == "name_asc":
                order_s = " ORDER BY b.first_name,b.last_name"
            if order_by == "name_desc":
                order_s = " ORDER BY b.first_name DESC, b.last_name DESC"
            if order_by == "age_asc":
                order_s = " ORDER BY b.birth_date DESC"
            if order_by == "age_desc":
                order_s = " ORDER BY b.birth_date ASC"
            if order_by == "country_asc":
                order_s = " ORDER BY c2.country, c3.nationality"
        if state_id:
            placeholders =  ', '.join(['?'] * len(state_id))
            aux += f" AND k1.stateID in ({placeholders})"
            filters.extend(state_id)
        if region_n:
            placeholders =  ', '.join(['?'] * len(region_n))
            aux += f" AND k2.region in ({placeholders})"
            filters.extend(region_n)
        if city_id:
            placeholders =  ', '.join(['?'] * len(city_id))
            query += f" AND b.cityID in ({placeholders})"
            filters.extend(city_id)
            
        if state_id or region_n:
            query += " AND b.cityID IN (" + aux + ")"
            
    query += " GROUP BY b.personId"
    query += order_s
    data = db.execute(query, tuple(filters)).fetchall()
    return render_template('search.html',country=country,industry=industry,source=source,gender=gender,city=city,state=state,region=region,continent=continent,data=data)
