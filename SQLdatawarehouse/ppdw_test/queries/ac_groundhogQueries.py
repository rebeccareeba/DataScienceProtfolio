def air_cond_groundhog_day():
    sql = '''
        SELECT  
        YEAR(sh.sold_date) AS `Year`, 
        SUM(sh.quantity) AS AC_Units_Sold_per_year, 
        ROUND(SUM(sh.quantity)/365, 2) AS Average_AC_Units_Sold_per_day, 
        SUM(CASE WHEN (MONTH(sh.sold_date) = 2 AND DAY(sh.sold_date) = 2) THEN sh.quantity ELSE 0 END) AS AC_Units_Sold_on_GroundhogDay
        FROM sales_history sh  
        LEFT JOIN product p ON sh.pid = p.pid  
        LEFT JOIN product_category pc on p.pid = pc.pid 
        LEFT JOIN category c on pc.category_id = c.category_id 
        WHERE c.category_name LIKE '%Air Conditioner%' 
        GROUP BY YEAR(sh.sold_date) 
        ORDER BY YEAR(sh.sold_date) ASC; 
        '''
    return sql
