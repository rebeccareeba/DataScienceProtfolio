
def viewHolidays():
    sql = "SELECT holiday_date, holiday_name FROM holiday"

    return sql

def getEventDate(date):
    sql = "SELECT COUNT(event_date) FROM event_date WHERE event_date = '%s'" % date

    return sql

def getHoliday(date):
    sql = "SELECT COUNT(holiday_date) FROM holiday WHERE holiday_date = '%s'" % date

    return sql

def insertEventDate(date):
    sql = "INSERT into event_date (`event_date`) VALUES ('%s')" % date

    return sql

def insertHoliday(date, name):
    sql = "INSERT INTO holiday (`holiday_date`, `holiday_name`) VALUES ('%s', '%s')" % (date, name)

    return sql