def membershipTrendsSQL():
    sql = "SELECT " \
          " YEAR(m.signup_date) AS year," \
          "(COUNT(m.member_id)) AS total_memberships_for_the_year  " \
          " FROM membership m   " \
          "GROUP BY YEAR(m.signup_date) " \
          " ORDER BY YEAR(m.signup_date) DESC"
    return sql


def topCitiesByYear(year):
    sql = "SELECT " \
          "YEAR(m.signup_date) AS year, " \
          "c.city_id AS city_id, " \
          "COUNT(DISTINCT s.store_id) AS number_of_stores_in_city," \
          "c.city AS city, " \
          "c.state AS state," \
          "COUNT(m.member_id) AS membership_count " \
          "FROM membership m " \
          "INNER JOIN store s on m.store_id = s.store_id " \
          "INNER JOIN city c on s.city_id = c.city_id " \
          "WHERE YEAR(m.signup_date) = {} " \
          "GROUP BY c.city, c.state, YEAR(m.signup_date), c.city_id  " \
          "ORDER BY COUNT(m.member_id) DESC " \
          "LIMIT 0, 25; " .format(year)
    return sql


def bottomCitiesByYear(year):
    sql = "SELECT " \
          "YEAR(m.signup_date) AS year, " \
          "c.city_id AS city_id, " \
          "COUNT(DISTINCT s.store_id) AS number_of_stores_in_city, " \
          "c.city AS city, " \
          "c.state AS state, " \
          "COUNT(m.member_id) AS membership_count " \
          "FROM membership m " \
          "INNER JOIN store s on m.store_id = s.store_id " \
          "INNER JOIN city c on s.city_id = c.city_id " \
          "WHERE YEAR(m.signup_date) = {} " \
          "GROUP BY c.city, c.state, YEAR(m.signup_date), c.city_id  " \
          "ORDER BY COUNT(m.member_id) ASC " \
          "LIMIT 0, 25; " .format(year)
    return sql


def drilldownByYearByCity(year, cityId):
    sql = "SELECT " \
          " YEAR(total.signup_date) AS year,  " \
          "total.street_addr AS street_address, " \
          "total.store_id AS store_id, " \
          " total.city AS city, " \
          " total.state AS state, " \
          "SUM(total.member_count) AS membership_count    " \
          "FROM ( " \
          " SELECT  " \
          " m.signup_date, " \
          " s.street_addr, " \
          " s.store_id, " \
          " c.city, " \
          " c.state,    " \
          " COUNT(m.member_id) AS member_count     " \
          " FROM membership `m`      " \
          " INNER JOIN store s ON m.store_id = s.store_id      " \
          "INNER JOIN city c ON s.city_id = c.city_id    " \
          "WHERE YEAR(m.signup_date) = {} AND c.city_id = {}     " \
          "GROUP BY  m.member_id) total    " \
          "GROUP BY  " \
          "total.street_addr,  " \
          "total.store_id,  " \
          "total.city, " \
          "total.state, " \
          "YEAR(total.signup_date)   " \
          "ORDER BY SUM(total.member_count) DESC;".format(year, cityId)
    return sql
