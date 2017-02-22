
import MySQLdb
import time
import numpy as np
import fastcluster
from HierarchyClusterRecipesSmart1 import *


def GetRecIdsForIngred(db,cursor,ingred_text):

    cursor.execute("""SELECT ingred_id FROM NaiveIngreds
                              WHERE ingred_text='"""+ingred_text+"""';""")

    ingred_id = cursor.fetchone()['ingred_id']

    cursor.execute("""SELECT rec_id FROM Recipes_NaiveIngreds
                              WHERE ingred_id='"""+str(ingred_id)+"""';""")

    all_rows = cursor.fetchall()
    rec_ids = [row['rec_id'] for row in all_rows]
    return rec_ids

    
if __name__ == "__main__":


    time_start = time.time()
    
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

    ingred_text = "mushrooms"
    
    rec_ids = GetRecIdsForIngred(db,cursor,ingred_text)

    #rec_ids = rec_ids[0:1000]
    
    print(len(rec_ids))

    np.save('HClusters/jaccard/rec_ids_'+ingred_text+'.npy',np.array(rec_ids,dtype=np.int64),allow_pickle=False)
    
    #X = ConstructXfromRecIds(db,cursor,rec_ids)
    #print X.shape
        
    H = HierarchyClusterRecipes(db,cursor,rec_ids)

    np.save('HClusters/jaccard/hc_'+ingred_text+'.npy',H,allow_pickle=False)
    
    print("Total run time: {} seconds".format(time.time()-time_start))

    #print H.nbytes

    
    
