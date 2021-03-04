def categorySQL():
    sql = "SELECT  " \
          "c.category_name AS Category,  " \
          "COUNT(p.pid) AS Number_of_Products, " \
          "COUNT(DISTINCT p.manufacturer_id) AS Number_of_Manufacturers, " \
          "ROUND(AVG(p.retail_price), 2) AS Average_Retail  " \
          "FROM category c " \
          "LEFT JOIN product_category pc ON c.category_id = pc.category_id " \
          "INNER JOIN product p ON pc.pid = p.pid " \
          "GROUP BY c.category_name " \
          "ORDER BY c.category_name ASC;  " \

    return sql