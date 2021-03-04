from flask import Flask, render_template, redirect, jsonify
from flask_mysqldb import MySQL

from forms.categoryForm import categoryForm
from forms.cityForm import CityForm
from forms.holidayForm import HolidayForm
from forms.storeRevenueForm import storeRevenueForm
import queries.mainMenuQueries
import queries.manufacturerReport
import queries.membershipTrendsReport
import queries.revenueByPopulation
import queries.holidayQueries
import queries.cityQueries
import queries.gps
import queries.ac_groundhogQueries
import queries.categoryQueries
import queries.stateHighestVolumeCategory
import queries.storeRevenueReport
import reformatData
import os
import re

# Comment needed here
SECRET_KEY = os.urandom(32)

# Initialize Flask application with DB credentials
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'gtuser'
app.config['MYSQL_PASSWORD'] = 'gtuser'
app.config['MYSQL_DB'] = 'cs6400_fall20_team019'
app.config['SECRET_KEY'] = SECRET_KEY

# Create MySQL handle for the Flask application
mysql = MySQL(app)


# Function for establishing the MySQL DB connection and execute supplied query
def dbConnection(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    rv = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return rv


# Function for handling duplicate date scenario when adding a holiday
@app.route('/holiday_error_handler_duplicateDate', methods=['GET'])
def holiday_error_handler_duplicateDate():
    return render_template("holiday_error_handler_duplicateDate.html")


# Function for handling invalid name scenario when adding a holiday
@app.route('/holiday_error_handler_invalidName', methods=['GET'])
def holiday_error_handler_invalidName():
    return render_template("holiday_error_handler_invalidName.html")


# Function for handling no city found scenario when updating population
@app.route('/city_error_handler_noCityFound', methods=['GET'])
def city_error_handler_noCityFound():
    return render_template("city_error_handler_noCityFound.html")


# Function for handling invalid population scenario when updating population
@app.route('/city_error_handler_invalidPopulation', methods=['GET'])
def city_error_handler_invalidPopulation():
    return render_template("city_error_handler_invalidPopulation.html")


# Function for rendering report for selected manaufacturer
@app.route('/manufacturer_report/<int:manufacturer_id>', methods=['GET'])
def single_manufacturer_report(manufacturer_id):
    manufacturer = dbConnection(queries.manufacturerReport.singleManufacturerSQL(id=manufacturer_id))
    products = dbConnection(queries.manufacturerReport.manufacturerProductsSQL(id=manufacturer_id))
    manufacturer, products = reformatData.forSingleManufacturer(manufacturer, products)

    return render_template("single_manufacturer_report.html", val1=manufacturer, val2=products)


# Function for rendering manaufacturer report summary
@app.route('/manufacturer_report/', methods=['GET'])
def all_manufacturer_report():
    allManufacturers = dbConnection(queries.manufacturerReport.allManufacturersSQL())
    allManufacturers = reformatData.forAllManufacturers(allManufacturers)

    return render_template("manufacturer_report.html", value=allManufacturers)


# Function for rendering membership trend summary report
@app.route('/membership_trend', methods=['GET'])
def all_membership_trends():
    allMembershipTrends = dbConnection(queries.membershipTrendsReport.membershipTrendsSQL())

    return render_template("all_membership_trends.html", value=allMembershipTrends)


# Function for rendering membership trend report for selected year
@app.route('/membership_trend/<int:year>', methods=['GET'])
def membership_by_year(year):
    TopCities = dbConnection(queries.membershipTrendsReport.topCitiesByYear(year))
    BottomCities = dbConnection(queries.membershipTrendsReport.bottomCitiesByYear(year))

    return render_template("membership_trends_year.html", val1=TopCities, val2=BottomCities)


# Function for rendering membership trend report for selected year and city
@app.route('/membership_trend/<int:year>/<int:cityId>', methods=['GET'])
def membership_by_year_city(year, cityId):
    drilldown = dbConnection(queries.membershipTrendsReport.drilldownByYearByCity(year, cityId))

    return render_template("membership_trends_year_city.html", val1=drilldown)


# Function for rendering revenue by population report
@app.route('/revenue_population', methods=['GET'])
def revenue_by_population():
    revenue = dbConnection(queries.revenueByPopulation.revenueByPopulation())
    revenue = reformatData.forRevenueByPopulation(revenue)

    return render_template("revenue_population.html", value=revenue)


# Function for rendering report of currently defined holidays
@app.route('/holiday', methods=['GET', 'POST'])
def view_holiday():
    holiday = dbConnection(queries.holidayQueries.viewHolidays())

    return render_template("holiday.html", value=holiday)


# Function for rendering form for adding a holiday
@app.route('/add_holiday', methods=['GET', 'POST'])
def add_holiday():
    form = HolidayForm()

    if form.validate_on_submit():
        date = form.holiday_date.data
        name = re.sub(r"[^a-zA-Z0-9 ]+", '', form.holiday_name.data)

        if len(name) == 0:
            return redirect('/holiday_error_handler_invalidName')

        numEventDate = dbConnection(queries.holidayQueries.getEventDate(date))
        numHolidayDate = dbConnection(queries.holidayQueries.getHoliday(date))

        if numHolidayDate[0][0] == 0:
            if numEventDate[0][0] == 0:
                dbConnection(queries.holidayQueries.insertEventDate(date))

            dbConnection(queries.holidayQueries.insertHoliday(date, name))
        else:
            return redirect('/holiday_error_handler_duplicateDate')

        return redirect('/holiday')

    return render_template("add_holiday.html", form=form)


# Function for rendering report all cities
@app.route('/cities', methods=['GET', 'POST'])
def view_cities():
    cities = dbConnection(queries.cityQueries.viewCities())

    return render_template("cities.html", value=cities)


# Function for rendering form for updating population of selected city
@app.route("/city/<int:city_id>", methods=["POST", "GET"])
def city_details(city_id):
    form = CityForm()
    city = dbConnection(queries.cityQueries.getCityById(city_id))

    if city is None:
        return redirect('/city_error_handler_noCityFound')

    if form.validate_on_submit():
        try:
            population = int(form.population.data)
        except ValueError:
            return redirect('/city_error_handler_invalidPopulation')

        if population < 0:
            return redirect('/city_error_handler_invalidPopulation')

        dbConnection(queries.cityQueries.updateCityPopulation(city_id, population))
        # return redirect('/city/'+str(city_id))
        return redirect('/cities')

    return render_template("city.html", row=city, form=form)


# Function for rendering main menu
@app.route('/', methods=['GET'])
def index():
    storeCount = dbConnection(queries.mainMenuQueries.storeCountSQL())
    manufacturerCount = dbConnection(queries.mainMenuQueries.manufacturerCountSQL())
    productCount = dbConnection(queries.mainMenuQueries.productCountSQL())
    memberCount = dbConnection(queries.mainMenuQueries.memberCountSQL())

    return render_template("index.html", val1=storeCount[0][0], val2=manufacturerCount[0][0],
                           val3=productCount[0][0], val4=memberCount[0][0])


# Function for rendering actual vs predicted revenue for GPS summary
@app.route('/gps', methods=['GET'])
def GPS_report():
    gpsUnits = dbConnection(queries.gps.actual_predicted_rev_gps())
    gpsUnits = reformatData.forActualVSPredicted(gpsUnits)

    return render_template("gps.html", value=gpsUnits)


# Function for rendering air conditioners on Groundhog Day report
@app.route('/ac_groundhogDay', methods=['GET'])
def ac_groundhogDay_report():
    acUnits = dbConnection(queries.ac_groundhogQueries.air_cond_groundhog_day())

    #print(acUnits)

    return render_template("ac_groundhogDay.html", value=acUnits)


# Function for rendering category report
@app.route('/category', methods=['GET'])
def category_report():
    category_summary = dbConnection(queries.categoryQueries.categorySQL())
    category_summary = reformatData.forCategory(category_summary)

    return render_template("category.html", value=category_summary)


@app.route('/highest_category', methods=['GET', 'POST'])
def highest_category():
    form = categoryForm()
    years = dbConnection(queries.stateHighestVolumeCategory.getYear())
    months = dbConnection(queries.stateHighestVolumeCategory.getMonth(years[0][0]))

    form.year.choices = [year[0] for year in years]
    form.month.choices = [month[0] for month in months]
    print(form.month.data)
    if form.validate_on_submit():
        year = int(form.year.data)
        month = int(form.month.data)
        return redirect('/highest_category/' + str(year) + '/' + str(month))
    try:
        year = int(form.year.data)
        month = int(form.month.data)
        return redirect('/highest_category/' + str(year) + '/' + str(month))
    except:
        return render_template("highest_category.html", form=form)


@app.route('/highest_category/<int:year>/<int:month>', methods=['GET', 'POST'])
def categoryByYearMonth(year, month):
    form = categoryForm(year=year, month=month)
    years = dbConnection(queries.stateHighestVolumeCategory.getYear())
    months = dbConnection(queries.stateHighestVolumeCategory.getMonth(year))
    form.year.choices = [y[0] for y in years]
    form.month.choices = [m[0] for m in months]
    if form.validate_on_submit():
        newyear = int(form.year.data)
        newmonth = int(form.month.data)
        return redirect('/highest_category/' + str(newyear) + '/' + str(newmonth))
    data = dbConnection(queries.stateHighestVolumeCategory.topCategoriesByYearByMonth(year, month))
    print(data)
    return render_template("highest_category_year_month.html", value=data, form=form, year=year, month=month)


@app.route('/month/<int:year>/', methods=['GET', 'POST'])
def getMonth(year):
    months = dbConnection(queries.stateHighestVolumeCategory.getMonth(year))
    monthArray = []

    for month in months:
        monthObj = {}
        monthObj['id'] = month[0]
        monthObj['month'] = month[0]
        monthArray.append(monthObj)

    return jsonify({'months': monthArray})


# Function to render store revenue report by state by year
@app.route('/store_revenue', methods=['GET', 'POST'])
def store_revenue():
    form = storeRevenueForm()
    states = dbConnection(queries.storeRevenueReport.getState())
    form.state.choices = [state[0] for state in states]
    #print(form.state.data)

    if form.validate_on_submit():
        state = str(form.state.data)
        return redirect('/store_revenue/' + str(state))
    try:
        state = str(form.state.data)
        return redirect('/store_revenue/' + str(state))
    except:
        return render_template("store_revenue.html", form=form)


@app.route('/store_revenue/<string:state>', methods=['GET', 'POST'])
def storeRevenueByState(state):
    form = storeRevenueForm(state=state)
    states = dbConnection(queries.storeRevenueReport.getState())
    form.state.choices = [state[0] for state in states]

    if form.validate_on_submit():
        newstate = str(form.state.data)
        return redirect('/store_revenue/' + str(newstate))

    data = dbConnection(queries.storeRevenueReport.getStoreRevenue(state))
    data = reformatData.forStoreRevenueByYearByState(data)

    return render_template("store_revenue_state.html", value=data, form=form, state=state)


if __name__ == '__main__':
    app.run()
