
def storeCountSQL():
    sql = "SELECT COUNT(store_id) AS Number_of_Stores FROM store"

    return sql


def manufacturerCountSQL():
    sql = "SELECT COUNT(manufacturer_id) AS Number_of_Manufacturers FROM manufacturer"

    return sql


def productCountSQL():
    sql = "SELECT COUNT(pid) AS Number_of_Products FROM product"

    return sql


def memberCountSQL():
    sql = "SELECT COUNT(member_id) AS Number_of_Memberships FROM membership"

    return sql

