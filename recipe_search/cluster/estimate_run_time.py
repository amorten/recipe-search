
import MySQLdb
import time

def estimate_run_time(cursor,num_ingreds_to_print=10):

    # The following MySQL command calculates the estimated run time
    # (single processor on my MacBook Pro) in numbers of days.
    # Run time for the hierarchical clustering of all recipes that
    #    a single given ingredient.
    
    cursor.execute("""select ing_nums.ingred_id,NaiveIngreds.ingred_text,ing_nums.cnt,ing_nums.cnt*ing_nums.cnt/1000000*4/3600/24/10 as runtime from (select ingred_id, count(ingred_id) as cnt from recipes_naiveingreds group by ingred_id order by count(ingred_id) desc) as ing_nums INNER JOIN SmartIngreds1 as sm1 on sm1.ingred_id=ing_nums.ingred_id INNER JOIN NaiveIngreds on ing_nums.ingred_id=NaiveIngreds.ingred_id order by cnt desc;""")

    all_ingred_times = cursor.fetchall()

    #print(all_ingred_times[0:10])

    runtimes = [row['runtime'] for row in all_ingred_times]
    ingred_names = [row['ingred_text'] for row in all_ingred_times]
    total_runtime = sum(runtimes)
    
    print("Top "+str(num_ingreds_to_print)+" ingredient runtimes:")
    print('\n'.join("{}: {} CPU days".format(ingred_name,runtime)
                    for ingred_name,runtime
                     in zip(ingred_names[0:num_ingreds_to_print],
                            runtimes[0:num_ingreds_to_print])))
    
    print("Total estimated runtime "
          "for single ingred clusters: {} CPU days".format(total_runtime))
    
    return total_runtime # Measured in CPU days.




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

    estimate_run_time(db)
    
    
