def actual_predicted_rev_gps():
    sql = """
	SELECT t.pid, 
			   t.product_name AS Product_Name, 
			   t.retail_price AS Retail_Price,
			   t.Units_Ever_Sold, 
			   t.Units_Sold_At_Discount, 
			   t.Units_Sold_At_Retail,
			   t.Actual_Revenue, 
			   t.Predicted_Revenue, 
			   t.Predicted_Revenue_Differences
	FROM (
		SELECT 
			 rev.pid 
			,rev.product_name
			,rev.retail_price
			,SUM(rev.quantity) AS Units_Ever_Sold
			,SUM(CASE WHEN rev.sale_price > 0 THEN rev.quantity ELSE NULL END) AS Units_Sold_At_Discount
			,SUM(CASE WHEN (rev.sale_price is null or rev.sale_price = 0) THEN rev.quantity ELSE NULL END) AS Units_Sold_At_Retail
			,SUM(COALESCE(rev.SaleRevenue, 0)) AS  total_sale_revenue
			,SUM(COALESCE(rev.RetailRevenue,0)) AS total_retail_revenue
			,SUM(COALESCE(rev.PredictedRetailRevenue, 0)) AS total_predicted_sale_rev
			,ROUND(SUM(COALESCE(rev.SaleRevenue,0)) + SUM(COALESCE(rev.RetailRevenue,0)),2) AS Actual_Revenue
			,ROUND(SUM(COALESCE(rev.RetailRevenue,0)) + SUM(COALESCE(rev.PredictedRetailRevenue,0)),2) AS Predicted_Revenue
			,ROUND(SUM(COALESCE(SaleRevenue,0)) - SUM(COALESCE(rev.PredictedRetailRevenue,0)),2) AS Predicted_Revenue_Differences
		FROM 
			(SELECT 
					c.category_name
					,sh.pid
					,p.product_name
					,sh.sold_date
					,ps.sale_date
					,p.retail_price
					,ps.sale_price
					,sh.quantity
					,Quantity * (CASE WHEN ps.sale_price > 0 Then ps.sale_price ELSE 0 END) AS SaleRevenue	
					,Quantity * (CASE WHEN (ps.sale_price is null or ps.sale_price = 0) Then p.retail_price ELSE 0 END) AS RetailRevenue	
					,(0.75 * Quantity) * (CASE WHEN ps.sale_price > 0 Then p.retail_price ELSE 0 END) AS PredictedRetailRevenue	
				FROM sales_history sh 
				LEFT JOIN product p ON sh.pid = p.pid 
				LEFT JOIN product_sale ps ON sh.pid = ps.pid AND sh.sold_date = ps.sale_date
				LEFT JOIN product_category pc ON sh.pid = pc.pid
				LEFT JOIN category c ON pc.category_id = c.category_id
				WHERE 
					c.category_name LIKE '%GPS%') rev
		GROUP BY
			 rev.category_name
			,rev.pid 
			,rev.product_name
			,rev.retail_price) t
	WHERE abs(t.Predicted_Revenue_Differences) > 5000
	ORDER BY 
		t.Predicted_Revenue_Differences DESC;
		"""
    return sql
