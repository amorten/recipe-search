

import MySQLdb



# The SQL statement comes from
# http://stackoverflow.com/questions/4329396/mysql-select-10-random-rows-from-600k-rows-fast
# For now WE ASSUME THAT PRIMARY KEY IS SEQUENTIAL WITH NO GAPS.
# The same webpage has ideas for handling gaps.
# We can implement that later.

def GetRandomRowFromDB(cursor,numrows,tablename,temp_tablename):

    cursor.execute("""
      DROP PROCEDURE IF EXISTS get_rands;""")
    cursor.execute("""
      CREATE PROCEDURE get_rands(IN cnt INT)
      BEGIN
        DROP TEMPORARY TABLE IF EXISTS """+temp_tablename+""" ;
        CREATE TEMPORARY TABLE  """+temp_tablename+""" ( rand_id INT );
    
        loop_me: LOOP
          IF cnt < 1 THEN
            LEAVE loop_me;
          END IF;

          INSERT INTO  """+temp_tablename+""" 
          SELECT r1.rec_id
            FROM """+tablename+""" AS r1 JOIN
              (SELECT (RAND() *
                            (SELECT MAX(rec_id)
                               FROM """+tablename+""" )) AS rec_id)
               AS r2
            WHERE r1.rec_id >= r2.rec_id
            ORDER BY r1.rec_id ASC
            LIMIT 1;

          SET cnt = cnt - 1;
        END LOOP loop_me;
      END;""")
    cursor.execute("""
      CALL get_rands("""+str(numrows)+""");""")
    cursor.execute("""
      SELECT * FROM """+temp_tablename+""";""")

    
    return cursor.fetchall()



if __name__ == "__main__":

    db = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "pwd4recDB",
                        db = "recipes")

    db.set_character_set('utf8')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')


    rand_recipes = GetRandomRowFromDB(cursor,2,'recipes','recipesasdf')

    print rand_recipes
