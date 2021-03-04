def getState():
    sql = """
    SELECT DISTINCT state FROM city ORDER BY state ASC; 
    """
    return sql

def getStoreRevenue(state):
    sql = """
    	SELECT 
			 YEAR(sh.sold_date) AS Sales_Year
            ,sh.store_id
            ,s.street_addr AS Store_Address
            ,c.city
            ,c.state
		    ,ROUND(SUM((Quantity * (CASE WHEN ps.sale_price > 0 Then ps.sale_price ELSE 0 END))) + 
				SUM((Quantity * (CASE WHEN (ps.sale_price is null or ps.sale_price = 0) Then p.retail_price ELSE 0 END))),2) AS Total_Revenue
	FROM sales_history sh 
		LEFT JOIN product p ON sh.pid = p.pid 
		LEFT JOIN product_sale ps ON sh.pid = ps.pid AND sh.sold_date = ps.sale_date
        LEFT JOIN store s on sh.store_id = s.store_id
        LEFT JOIN city c on s.city_id = c.city_id
	WHERE c.state = '%s'
    GROUP BY
			 YEAR(sh.sold_date) 
            ,sh.store_id
            ,s.street_addr
            ,c.city
            ,c.state
	ORDER BY
		Sales_Year ASC
        ,Total_Revenue DESC;
    """ % state
    return sql


