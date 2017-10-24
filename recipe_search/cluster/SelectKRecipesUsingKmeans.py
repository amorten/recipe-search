
import MySQLdb
import time
from sklearn.cluster import KMeans
import numpy as np
from scipy.sparse import *
from GetRandomRecipesFromDB import *

# The follow URL discusses using sparse matrices with KMeans:
# http://dev.bizo.com/2012/01/clustering-of-sparse-data-using-python.html
# It seems that KMeans only works with CSR type sparse matrices

def SelectKRecipesUsingKmeans(k,rec_ids,cursor):


    X = ConstructSparseXfromRecIds(rec_ids,cursor)
    
    labeler = KMeans(n_clusters=k)

    time_before = time.time()
    labeler.fit(X)
    print("Time to do KMeans: {} seconds".format(time.time()-time_before))

    for (row,label) in enumerate(labeler.labels_):
        print (row,label)
    
    return labeler


def ConstructSparseXfromRecIds(rec_ids,cursor):

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

    print("Time to fetch data: {} seconds".format(time.time()-time_before))
    
    
    #rec_ingred_rows = [{'rec_id':17,'ingred_id':100},
    #                   {'rec_id':17,'ingred_id':117},
    #                   {'rec_id':42,'ingred_id':100},
    #                   {'rec_id':42,'ingred_id':142}]
    
    rec_ids_idx = {rec_id:rec_ids.index(rec_id) for rec_id in rec_ids}

    num_recs = len(rec_ids)
    #max_rec_id = max(rec_ids) #Don't need this
    max_ingred_id = 10000 # Temporary value

    time_before = time.time()
    
    #Use lil_matrix to construct X efficiently
    #Actually, dok_matrix is 8 times faster than lil_matrix!
    #Matrix construction is the bottleneck.
    X = dok_matrix((num_recs,max_ingred_id+1)) #Plus 1, because
                                                 #we index starting at 1.
    for rec_ingred in rec_ingred_rows:
        X[rec_ids_idx[rec_ingred['rec_id']],rec_ingred['ingred_id']] = 1.0

    print("Time to construct matrix: {} seconds".format(time.time()-time_before))

    time_before = time.time()
    # Convert to csr_matrix for use by KMeans
    X = X.tocsr()
    print("Time to convert matrix: {} seconds".format(time.time()-time_before))
    
    #print X.count_nonzero()    

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


    num_recipes = 20
    print("Number of recipes: {} ".format(num_recipes))
    
    time_before = time.time()
    
    rand_recipes = GetRandomRecipesFromDB(cursor,num_recipes,'recipes','recipesasdf')

    print("Time to choose random recipes: {} seconds".format(time.time()-time_before))

    
    rec_ids = [rec['rec_id'] for rec in rand_recipes]

    time_before = time.time()
    
    SelectKRecipesUsingKmeans(5,rec_ids,cursor)

    print("Total run time: {} seconds".format(time.time()-time_start))
