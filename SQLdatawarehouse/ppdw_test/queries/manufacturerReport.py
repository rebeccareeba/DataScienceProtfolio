def allManufacturersSQL():
    sql = "SELECT " \
          "m.manufacturer_id AS Manufacturer_ID, " \
          "manufacturer_name AS Manufacturer, " \
          "COUNT(pid) AS Product_Count, " \
          "ROUND(AVG(retail_price), 2) AS Avg_Retail, " \
          "MIN(retail_price) AS Min_Retail, " \
          "MAX(retail_price) AS Max_Retail " \
          "FROM manufacturer AS m " \
          "INNER JOIN product AS p ON  m.manufacturer_id = p.manufacturer_id " \
          "GROUP BY m.manufacturer_id " \
          "ORDER BY AVG(retail_price) DESC " \
          "LIMIT 100"

    return sql


def singleManufacturerSQL(id):
    sql = "SELECT " \
          "m.manufacturer_id AS Manufacturer_ID," \
          "m.manufacturer_name AS Manufacturer, " \
          "m.max_discount AS Max_Discount, " \
          "COUNT(p.pid) AS Total_Products, " \
          "ROUND(AVG(p.retail_price), 2) AS Avg_Retail, " \
          "MIN(p.retail_price) AS Min_Retail, " \
          "MAX(p.retail_price) AS Max_Retail " \
          "FROM manufacturer AS m " \
          "INNER JOIN product AS p on m.manufacturer_id = p.manufacturer_id " \
          "WHERE m.manufacturer_id = %d" % id

    return sql


def manufacturerProductsSQL(id):
    sql = "SELECT " \
          "p.pid AS Product_ID, " \
          "p.product_name AS Product_Name, " \
          "GROUP_CONCAT(DISTINCT c.category_name  SEPARATOR ', ') AS Category, " \
          "p.retail_price AS Retail_Price " \
          "FROM product AS p " \
          "LEFT JOIN product_category AS pc ON p.pid = pc.pid " \
          "LEFT JOIN category AS c ON pc.category_id = c.category_id " \
          "WHERE p.manufacturer_id = %d " \
          "GROUP BY p.pid " \
          "ORDER BY p.retail_price DESC" % id

    return sql
