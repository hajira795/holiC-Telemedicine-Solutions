import pymysql
def connecton():
    db = pymysql.connect(host="localhost", user="root", passwd="", db="holic")
    cur = db.cursor()
    return cur,db
