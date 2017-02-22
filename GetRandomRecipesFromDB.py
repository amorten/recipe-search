

import MySQLdb
import time


# The SQL statement comes from
# http://stackoverflow.com/questions/4329396/mysql-select-10-random-rows-from-600k-rows-fast
# For now WE ASSUME THAT PRIMARY KEY IS SEQUENTIAL WITH NO GAPS.
# The same webpage has ideas for handling gaps.
# We can implement that later.

#Also, the below code assumes that rec_id is a primary key
#  of tablename.

def GetRandomRecipesFromDB(cursor,numrows,tablename,temp_tablename):

    cursor.execute("""
      DROP PROCEDURE IF EXISTS get_rands;""")
    cursor.execute("""
      CREATE PROCEDURE get_rands(IN cnt INT)
      BEGIN
        DROP TEMPORARY TABLE IF EXISTS """+temp_tablename+""" ;
        CREATE TEMPORARY TABLE  """+temp_tablename+""" 
         ( 
          rec_id INT UNSIGNED NOT NULL, 
          PRIMARY KEY (rec_id)""" #,
          #FOREIGN KEY (rec_id) REFERENCES """+tablename+""" (rec_id)
        """);
    
        loop_me: LOOP
          IF cnt < 1 THEN
            LEAVE loop_me;
          END IF;

          INSERT IGNORE INTO  """+temp_tablename+""" 
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
    #cursor.execute("""
    #  SELECT rec.rec_id, rec.rec_name FROM """+tablename+""" AS rec 
    #            INNER JOIN """+temp_tablename+""" AS temp
    #            ON rec.rec_id=temp.rec_id;""")

    
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


    time_before = time.time()
    
    rand_recipes = GetRandomRecipesFromDB(cursor,100,'recipes','recipesasdf')

    print("Total run time: {} seconds".format(time.time()-time_before))
    
    #print rand_recipes
