
import MySQLdb
import time
import numpy as np
from GetRandomRecipesFromDB import *
import fastcluster
import scipy


#@profile
def HierarchyClusterRecipes(db,cursor,rec_ids):

    X = ConstructXfromRecIds(db,cursor,rec_ids)

    #H = fastcluster.linkage_vector(X,method='single',metric='kulsinski',)
    #H = fastcluster.linkage(X,method='single',metric='kulsinski',)
    #del H
    #X = scipy.spatial.distance.pdist(X,'kulsinski')
    X = scipy.spatial.distance.pdist(X,'jaccard')
    np.save('HClusters/jaccard/pdist_'+'mushrooms'+'.npy',X,allow_pickle=False)
    H = fastcluster.linkage(X,method='complete',)
    #H = fastcluster.linkage(X,method='complete',metric='kulsinski')

    
    return H


def ConstructXfromRecIds(db,cursor,rec_ids):

    # First get a table of with entries (rec_id,ingred_id).
    # Fetchall into rec_ingred_rows.

    # Note that in Python 2.7 each rec_id is a LONG
    # so the printed version appends L to the end of it.
    # That's a problem for sending it to MySQL (need to remove L).
    #   print str(rec_ids)
    #   print str(rec_ids).replace('L','')

    time_before = time.time()
    cursor.execute("""
      SELECT rec_id, ingred_id FROM Recipes_NaiveIngreds 
        WHERE rec_id
         IN ("""+str(rec_ids).replace('L','')[1:-1]+""")"""
    )
    rec_ingred_rows = cursor.fetchall()

    cursor.execute("""
      SELECT ingred_id FROM SmartIngreds1""" 
    )
    all_rows = cursor.fetchall()
    ingred_ids = [row['ingred_id'] for row in all_rows]

    print("Time to fetch data: {} seconds".format(time.time()-time_before))
        
    rec_ids_idx = {rec_id:rec_ids.index(rec_id) for rec_id in rec_ids}
    ingred_ids_idx = {ingred_id:ingred_ids.index(ingred_id)
                        for ingred_id in ingred_ids}

    #print ingred_ids
    
    num_recs = len(rec_ids)
    num_ingreds = len(ingred_ids)

    time_before = time.time()

    X = np.zeros((num_recs,num_ingreds),dtype='bool')
    
    for rec_ingred in rec_ingred_rows:
        if rec_ingred['ingred_id'] in ingred_ids:
            X[rec_ids_idx[rec_ingred['rec_id']],ingred_ids_idx[rec_ingred['ingred_id']]] = True

    print("Time to construct matrix: {} seconds".format(time.time()-time_before))
    print X.nbytes
    
    return X





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


    num_recipes = int(4000.0)
    print("Number of recipes: {} ".format(num_recipes))
    
    #time_before = time.time()
    
    #rand_recipes = GetRandomRecipesFromDB(cursor,num_recipes,'recipes','recipesasdf')

    #print("Time to choose random recipes: {} seconds".format(time.time()-time_before))
    
    #rec_ids = [rec['rec_id'] for rec in rand_recipes]

    rec_ids = range(1,num_recipes+1)

    
    time_before = time.time()
    
    H = HierarchyClusterRecipes(db,cursor,rec_ids)
    
    print("Total run time: {} seconds".format(time.time()-time_start))

    print H.nbytes

    # Formulas for memory usage (MiB),
    # when num_recipes=1000*n, max_ingred_id=5000
    #
    # linkage_vector, single: 24 + 17*n + 0.2*n 
    #
    # linkage, complete:      24 + 17*n + 0.2*n + 4*n^2 ???
    #
    # linkage, complete:  max(24 + 17n , 4*n^2) ???
    # (n,max MiB) = (1,45), (2,74), (4,154), (8,152), (8*1.414,212)
    #                (32,540)
    #
    # Hmm, the report by memory_profiler is very wrong compared to using
    # My mac's activity moniter.
    #
    # linkage, complete, activity moniter: (n,t_sec,max MiB)
    #  note that total memory is (memory)+(compressed memory)
    #   (1,4,?), (2,15,>68), (4,60,>146), (8,250,~400+100)
    #   (32,4000,>5000)

    
