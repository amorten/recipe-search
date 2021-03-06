
import MySQLdb

# I considered using the defaults:
#     host="localhost",user="root",passwd="pwd4recDB",db="recipes",
# but that could be dangerous if I later want to change to a different
# database.

def get_db(host,user,passwd,dbname):

    db = MySQLdb.connect (host = host,
                          user = user,
                          passwd = passwd,
                          db = dbname,
                          use_unicode=True)

    db.set_character_set('utf8')

    return db

def get_cursor(db):

    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    return cursor


