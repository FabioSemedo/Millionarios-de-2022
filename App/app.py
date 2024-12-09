import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
from flask import abort, render_template, Flask, request
import logging
import db


APP = Flask(__name__,static_folder='css')
min_limit = "-10000000000000000"
max_limit = "10000000000000000"


def create():
    result = db.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'view' AND name = 'Ranks';
   """).fetchone()

    if result is None:
        db.execute('''CREATE VIEW Ranks AS
    SELECT
        DISTINCT b.personId,
        Rank() Over( ORDER BY wealth_millions DESC) as rank
    FROM
        Billionaires b
    ''')

def convert(num):
    if len(num) >= 15 :
        if num[0] == '-':
            num = min_limit
        else:
            num = max_limit
    
    return num

# Start page
@APP.route('/')
def index():
    create()
    query = '''SELECT
                   r.rank, b.personId, b.first_name, b.personId, b.last_name, c2.country, b.wealth_millions as wealth, b.name_suffix,
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
               JOIN
                   Ranks r ON b.personId = r.personId
               GROUP BY b.personId
               LIMIT 50;
            '''
    data = db.execute(query).fetchall()
    return render_template('index.html',data=data)



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
            min_tax_rate = convert(min_tax_rate)
            filters.append(float(min_tax_rate))
        if max_tax_rate:
            query += " AND m.tax_rate <= ?"
            max_tax_rate = convert(max_tax_rate)
            filters.append(float(max_tax_rate))
            
        if min_tax_rev:
            query += " AND ? <= m.tax_rev"
            min_tax_rev = convert(min_tax_rev)
            filters.append(float(min_tax_rev))
        if max_tax_rev:
            query += " AND m.tax_rev <= ?"
            max_tax_rev = convert(max_tax_rev)
            filters.append(float(max_tax_rev))
            
        if min_cpi:
            query += " AND ? <= m.cpi"
            min_cpi = convert(min_cpi)
            filters.append(float(min_cpi))
        if max_cpi:
            query += " AND m.cpi <= ?"
            max_cpi = convert(max_cpi)
            filters.append(float(max_cpi))

        if min_change:
            query += " AND ? <= m.cpi_change"
            min_change = convert(min_change)
            filters.append(float(min_change))
        if max_change:
            query += " AND m.cpi_change <= ?"
            max_change = convert(max_change)
            filters.append(float(max_change))

        if min_gdp:
            query += " AND ? <= m.gdp"
            min_gdp = convert(min_gdp)
            filters.append(int(min_gdp))
        if max_gdp:
            query += " AND m.gdp <= ?"
            max_gdp = convert(max_gdp)
            filters.append(int(max_gdp))

        if min_trt:
            query += " AND ? <= m.grs_trt_enroll"
            min_trt = convert(min_trt)
            filters.append(float(min_trt))
        if max_trt:
            query += " AND m.grs_trt_enroll <= ?"
            max_trt = convert(max_trt)
            filters.append(float(max_trt))

        if min_prm:
            query += " AND ? <= m.grs_prm_enroll"
            min_prm = convert(min_prm)
            filters.append(float(min_prm))
        if max_prm:
            query += " AND m.grs_prm_enroll <= ?"
            max_prm = convert(max_prm)
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
    query = '''SELECT b.*, (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) as age
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
           query += " AND (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) >= ?"
           min_age = convert(min_age)
           filters.append(int(min_age))
        
        if max_age:
            query += " AND (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) <= ?"
            max_age = convert(max_age)
            filters.append(int(max_age))
        
        if min_money:
            query += " AND b.wealth_millions >= ?"
            min_money = convert(min_money)
            filters.append(int(min_money))
        
        if max_money:
            query += " AND b.wealth_millions <= ?"
            max_money = convert(max_money)
            filters.append(int(max_money))
        if gender:
            query += " AND b.gender = ?"
            filters.append(gender)
    query += " ORDER BY b.first_name, b.last_name, b.name_suffix"        
    result = db.execute(query, tuple(filters))
    billionaires = result.fetchall()
    return render_template('search-billionaires.html', billionaires=billionaires)



@APP.route('/billionaires/<int:id>')
# Billionaire Info
def billionaire_info(id):

    # billionaire
    query_billionaire = '''SELECT
                              b.*, Group_Concat(s.source, ', ') as source,(CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) as age
                           FROM
                               Billionaires b
                           JOIN
                               Activities a ON a.personId = b.personId
                           JOIN
                               SourcesOfWealth s ON s.sourceID = a.sourceID
                           WHERE
                               b.personId = ?
                           GROUP BY b.personId
                        '''
    billionaire = db.execute(query_billionaire,[id]).fetchone()

    # country
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
    return render_template('billionaire-info.html',billionaire=billionaire,country=country,city=city)


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


@APP.route('/countries/<int:id>/economic')
def economic(id):
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
    create()
    query = '''SELECT
                   r.rank, b.personId, b.first_name, b.last_name, c2.country, b.wealth_millions as wealth, b.name_suffix, 
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
               JOIN
                   Ranks r ON r.personId = b.personId
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
           query += " AND (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) >= ?"
           min_age = convert(min_age)
           filters.append(int(min_age))
        
        if max_age:
            query += " AND (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) / 365.25 AS INTEGER)) <= ?"
            max_age = convert(max_age)
            filters.append(int(max_age))
        
        if min_money:
            query += " AND b.wealth_millions >= ?"
            min_money = convert(min_money)
            filters.append(int(min_money))
        
        if max_money:
            query += " AND b.wealth_millions <= ?"
            max_money = convert(max_money)
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





@APP.route('/stats')
# Statistics page
def stats():
    create()
    # Query 4
    sub_query_1 = db.execute('''SELECT 
                         rank, personId, first_name, last_name, wealth_millions, (2591 - rank - (gender_row - 1)) AS quantity, 
                         printf("%.4f", ((100*(2591 - rank - (gender_row - 1)) / 1.0) / ((SELECT count(gender) FROM Billionaires WHERE gender = "F" GROUP BY gender)))) AS percentage 
                     FROM 
                         (SELECT *, Rank() OVER (PARTITION BY gender ORDER BY rank DESC) AS gender_row FROM (Billionaires b join Ranks r on b.personId = r.personId)) 
                     WHERE gender = "M" 
                     ORDER BY quantity DESC, wealth_millions DESC''').fetchall()

    sub_query_2 = db.execute('''SELECT 
                         rank, personId, first_name, last_name, wealth_millions, (2591 - rank - (gender_row - 1)) AS quantity, 
                         printf("%.4f", ((100*(2591 - rank - (gender_row - 1)) / 1.0) / ((SELECT count(gender) FROM Billionaires WHERE gender = "M" GROUP BY gender)))) as percentage 
                     FROM 
                         (SELECT *, Rank() OVER (PARTITION BY gender ORDER BY rank DESC) AS gender_row FROM (Billionaires b join Ranks r on b.personID = r.personID)) 
                     WHERE 
                         gender = "F" 
                     ORDER BY quantity DESC, wealth_millions DESC''').fetchall()

    # Query 5
    query_2 = db.execute('''SELECT 
                     industry, SUM(wealth_millions) AS total 
                 FROM 
                     Billionaires 
                 GROUP BY industry ORDER BY total DESC, industry''').fetchall()


    # Query 6
    query_3 = db.execute('''SELECT 
                                o.continent, printf("%.1f", ((100 * count(b.personID)) / 2591.0)) AS percentage
                            FROM 
                                Billionaires b 
                            JOIN 
                                Cities c ON b.cityID = c.cityID 
                            JOIN 
                                Countries o ON c.countryID = o.countryID 
                            GROUP BY o.continent 
                            ORDER BY o.continent''').fetchall()
    
    # Query 1
    query_4 = db.execute('''SELECT 
                                quantity, 
                                printf("%.2f", ((total_wealth / 1.0) / (SELECT SUM(wealth_millions) FROM (SELECT personID, conglomorate, wealth_millions FROM Billionaires) WHERE conglomorate = 0 GROUP BY personID, conglomorate))) AS total_wealth_perc, 
                                grs_prm_enroll, grs_trt_enroll 
                            FROM 
                                (SELECT 
                                     COUNT(wealth_millions) AS quantity, SUM(wealth_millions) AS total_wealth, 
                                     e.grs_prm_enroll, ABS(e.grs_prm_enroll - 100), e.grs_trt_enroll, ABS(e.grs_trt_enroll) 
                                 FROM 
                                     Billionaires b 
                                 JOIN 
                                     Cities c ON b.cityID = c.cityID 
                                 JOIN 
                                     EconomicDetails e ON c.countryID = e.countryID 
                                 WHERE b.conglomorate = 0 
                                     GROUP BY ABS(grs_prm_enroll - 100), ABS(grs_trt_enroll - 100) 
                                     ORDER BY ABS(grs_prm_enroll - 100), ABS(grs_trt_enroll - 100))''').fetchall()


    # Query 2
    query_5 = db.execute('''SELECT 
                                o.name, printf("%.2E", (count(b.personID) / (e.population / 1.0))) AS ratio
                            FROM 
                                Billionaires b 
                            JOIN 
                                Cities c ON b.cityID = c.cityID 
                            JOIN 
                                EconomicDetails e ON c.countryID = e.countryID 
                            JOIN 
                                Countries o ON e.countryID = o.countryID 
                            GROUP BY population 
                            ORDER BY o.name DESC
                         ''').fetchall()


    # Query 3
    query_6 = db.execute('''SELECT 
                                b.industry, COUNT(b.personID) AS quantity 
                            FROM 
                                Billionaires b 
                            JOIN 
                                Cities c ON b.cityID = c.cityID 
                            JOIN 
                                EconomicDetails e ON c.countryID = e.countryID 
                            WHERE (CAST((julianday('2022-06-30') - julianday(b.birth_date)) AS integer) / 365.25) > e.life_expect AND (b.industry = "Metals & Mining" OR b.industry = "Construction & Engineering") 
                            GROUP BY b.industry 
                            ORDER BY b.industry DESC
                         ''').fetchall()

    # Query 7
    query_7 = db.execute('''SELECT 
                                s.region, b.industry, COUNT(b.personID) AS quantity, SUM(b.wealth_millions) AS total_wealth 
                            FROM 
                                Billionaires b 
                            JOIN 
                                Cities c ON b.cityID = c.cityID 
                            JOIN 
                                USCities uc ON c.cityID = uc.cityID 
                            JOIN
                                USStates s ON uc.stateID = s.stateID 
                            GROUP BY s.region, b.industry 
                            ORDER BY s.region, quantity desc, b.industry
                         ''').fetchall()

    # Query 8
    query_8 = db.execute('''SELECT
                                 k.first_name, k.last_name, k.wealth_millions, k.name, k.tax_rate 
                            FROM 
                                (SELECT b.first_name, b.last_name, b.wealth_millions, o.name, e.tax_rate, (ROW_NUMBER() OVER (PARTITION BY e.tax_rate ORDER BY b.wealth_millions desc)) AS ROW 
                                FROM 
                                   (Billionaires b 
                                JOIN 
                                    Cities c ON b.cityID = c.cityID 
                                JOIN 
                                    EconomicDetails e ON c.countryID = e.countryID
                                JOIN 
                                    Countries o ON e.countryID = o.countryID
                                )
                                ORDER BY e.tax_rate DESC) k
                             WHERE row <= 5
                         ''').fetchall()

    query_9 = db.execute('''SELECT k.name,
                                (k.sum / k.population) AS wealth
                            FROM (
                                SELECT 
                                    o.name AS name,
                                    sum(b.wealth_millions)*1000000 AS sum,
                                    e.population AS population
                                FROM (
                                Billionaires b
                                JOIN
                                Cities c ON b.cityID = c.cityID
                                JOIN
                                Countries o ON c.countryID = o.countryID
                                JOIN
                                EconomicDetails e ON o.countryID = e.countryID
                                )
                            GROUP BY o.name
                            ) k
                         ''').fetchall()

    query_10 = db.execute('''SELECT 
                                 name, source, MAX(soma) AS best_total 
                             FROM 
                                 (SELECT 
                                      o.name AS name, s.source AS source, SUM(b.wealth_millions) AS soma 
                                 FROM 
                                     Billionaires b 
                                 JOIN 
                                     Activities a ON b.personID = a.personID 
                                 JOIN 
                                     SourcesOfWealth s ON a.sourceID = s.sourceID 
                                 JOIN 
                                     Cities c ON b.cityID = c.cityID 
                                 JOIN 
                                     Countries o ON c.countryID = o.countryID 
                                 GROUP BY o.name) 
                             GROUP BY name 
                             ORDER BY best_total DESC, name, source
                         ''').fetchall()


    # Query 1 Rafael
    query_11 = db.execute('''SELECT 
                                 c1.name AS Origin_Country,
                                 c2.name AS Destination_Country,
                                 COUNT(b.personId) AS Total_Billionaires
                             FROM 
                                 Billionaires b
                             JOIN 
                                 Countries c1 ON b.citizenshipID = c1.countryid
                             JOIN 
                                 Cities ci ON b.cityID = ci.cityid
                             JOIN 
                                 Countries c2 ON ci.countryid = c2.countryid
                             WHERE 
                                 b.citizenshipID != ci.countryid
                             GROUP BY c1.name, c2.name
                             ORDER BY Total_Billionaires DESC;
                          ''').fetchall()

    # Query 2 Rafael
    query_12 = db.execute('''WITH IndustryCounts AS (
                                 SELECT 
                                 b.industry,
                                 COUNT(*) AS Total_Billionaires
                             FROM 
                                 Billionaires b
                             GROUP BY 
                                 b.industry
                             HAVING 
                                 COUNT(*) <= 50
                             )
                             SELECT 
                                 b.first_name AS First_name,
                                 b.last_name AS Last_name,
                                 b.industry AS Industry,
                                 b.wealth_millions AS Wealth_in_Millions,
                                 Total_billionaires,
                                 (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) AS INTEGER) / 365.25) AS Age
                             FROM 
                                 Billionaires b
                             JOIN 
                                 IndustryCounts ic ON b.industry = ic.industry
                             WHERE 
                                 (CAST((JULIANDAY('2022-06-30') - JULIANDAY(b.birth_date)) AS INTEGER) / 365.25) < 45
                             ORDER BY Age ASC, Wealth_in_Millions DESC;
                          ''').fetchall()

    query_13 = db.execute('''SELECT t1.continent, ROUND(t1.RelativeGdp,2) AS Relative_Gdp, ROUND(t1.RelativeGdp/(SUM(t2.RelativeGdp))*100, 2) as percentage
                             FROM 
                             (    SELECT continent, AVG(AdjGdp) as RelativeGdp
                                 FROM
                                 (SELECT cn.name, cn.continent, e1.gdp/e1.population AS AdjGdp, e1.*
                                 FROM EconomicDetails e1 INNER JOIN Countries cn on e1.countryid = cn.countryid
                                 )
                                 GROUP BY continent
                                 ORDER BY AVG(AdjGdp) Desc
                             ) t1, 
                             (    SELECT continent, AVG(AdjGdp) as RelativeGdp
                                 FROM
                                 (SELECT cn.name, cn.continent, e1.gdp/e1.population AS AdjGdp, e1.*
                                 FROM EconomicDetails e1 INNER JOIN Countries cn on e1.countryid = cn.countryid
                                 )
                                 GROUP BY continent
                                 ORDER BY AVG(AdjGdp) Desc
                             ) t2
                             GROUP BY t1.continent
                             ORDER BY percentage DESC
                                 ''').fetchall()

    
    return render_template('stats.html',sub_query_1=sub_query_1, sub_query_2=sub_query_2,query_2=query_2,query_3=query_3,query_4=query_4,query_5=query_5,query_6=query_6,query_7=query_7,query_8=query_8,query_9=query_9,query_10=query_10,query_11=query_11,query_12=query_12,query_13=query_13)
