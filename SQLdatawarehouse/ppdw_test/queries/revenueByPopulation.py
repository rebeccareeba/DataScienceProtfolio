
def revenueByPopulation():
    sql = "SELECT " \
          "rev.Year, " \
          "SUM(CASE WHEN rev.Population_Category = 'Small' THEN rev.Avg_Annual_Revenue ELSE 0 END) AS Small, " \
          "SUM(CASE WHEN rev.Population_Category = 'Medium' THEN rev.Avg_Annual_Revenue ELSE 0 END) AS Medium, " \
          "SUM(CASE WHEN rev.Population_Category = 'Large' THEN rev.Avg_Annual_Revenue ELSE 0 END) AS Large, " \
          "SUM(CASE WHEN rev.Population_Category = 'XLarge' THEN rev.Avg_Annual_Revenue ELSE 0 END) AS XLarge " \
          "FROM (  " \
          "SELECT  " \
          "t.Year AS Year, " \
          "(CASE   " \
          " WHEN t.population < 3700000 THEN 'Small'   " \
          " WHEN t.population >= 3700000 AND t.population < 6700000 THEN 'Medium' " \
          "WHEN t.population >= 6700000 AND t.population < 9000000 THEN 'Large'   " \
          "WHEN t.population >= 9000000 THEN 'XLarge'   " \
          "ELSE NULL  " \
          " END) AS Population_Category, " \
          "ROUND(SUM(t.Annual_Revenue), 2) AS Avg_Annual_Revenue " \
          "FROM ( " \
          "SELECT  " \
          " YEAR(sh.sold_date) AS Year, " \
          " c.city_id AS City_ID, " \
          " c.city AS City, " \
          " c.state AS State, " \
          "c.population AS Population, " \
          "SUM((CASE WHEN ps.sale_date = sh.sold_date THEN (sh.quantity * ps.sale_price) ELSE (sh.quantity * p.retail_price) END)) AS Annual_Revenue " \
          "FROM sales_history sh  " \
          "LEFT JOIN store s ON sh.store_id = s.store_id " \
          "LEFT JOIN city c ON s.city_id = c.city_id " \
          "LEFT JOIN product p ON sh.pid = p.pid  " \
          "LEFT JOIN product_sale ps ON sh.sold_date = ps.sale_date AND sh.pid = ps.pid  " \
          "GROUP BY YEAR(sh.sold_date), c.city_id) AS t " \
          "GROUP BY Year, Population_Category) AS rev " \
          "GROUP BY Year  " \
          "ORDER BY Year ASC "
    return sql

