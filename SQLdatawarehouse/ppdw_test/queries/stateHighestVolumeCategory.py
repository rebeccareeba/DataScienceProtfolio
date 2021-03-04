def getYear():
    sql = "SELECT DISTINCT(Year) FROM (SELECT DISTINCT YEAR(sold_date) AS `Year`," \
          "MONTH(sold_date) AS `Month` " \
          "FROM sales_history " \
          "ORDER BY 1,2) yr; "
    return sql


def getMonth(year):
    sql = "SELECT Month FROM (SELECT  " \
          "DISTINCT YEAR(sold_date) AS `Year`,  " \
          "MONTH(sold_date) AS `Month` " \
          "FROM sales_history " \
          "ORDER BY 1,2) rev " \
          "WHERE Year = {}; ".format(year)
    return sql


def topCategoriesByYearByMonth(year, month):
    sql = "SELECT " \
          "ct.category_name, " \
          "ct.state AS State_with_highest_number_units_sold, " \
          "Ct.Number_of_units_sold   " \
          "FROM ( " \
          "SELECT " \
          "s.category_name, " \
          "s.state, " \
          "s.Number_of_units_sold,  " \
          "ROW_NUMBER() OVER (PARTITION BY s.category_name ORDER BY s.Number_of_units_sold DESC, s.state) AS rn " \
          "FROM ( " \
          "SELECT  " \
          "cat.category_name, " \
          "c.state, " \
          "SUM(sh.quantity) AS Number_of_units_sold " \
          "FROM sales_history sh " \
          "LEFT JOIN store s ON sh.store_id = s.store_id " \
          "LEFT JOIN city c ON s.city_id = c.city_id " \
          "LEFT JOIN product_category pc ON sh.pid = pc.pid " \
          "LEFT JOIN category cat ON pc.category_id = cat.category_id " \
          "WHERE YEAR(sh.sold_date) = {} AND MONTH(sh.sold_date) = {} " \
          "GROUP BY cat.category_name, c.state " \
          ") s " \
          ") ct " \
          "WHERE rn = 1; ".format(year, month)
    return sql
