def viewCities():
    sql = "SELECT city_id, city, state, population FROM city"
    return sql


def getCityById(city_id):
    sql = "SELECT city_id, city, state, population FROM city WHERE city_id=%d" % city_id
    return sql


def updateCityPopulation(city_id, population):
    sql = "UPDATE city SET population=%d WHERE city_id=%d" % (population, city_id)
    return sql
