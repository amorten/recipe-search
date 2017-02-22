
import MySQLdb
import time
import numpy as np
from GetRandomRecipesFromDB import *
import fastcluster
import scipy.sparse

def pdist_sparse(X):

    #assumes X is sparse

    N = X.shape[0]
    print N
    print X
    
    P = np.zeros((N*(N-1)/2),dtype=np.double)
    
    P_idx = 0
    for i in range(0,N):
        print i
        u = X[i,:]
        for j in range(i+1,N):
            #Use binary arithmetic to calculate Kulsinski distance
            v = X[j,:]
            uandv = u.multiply(v)
            a = float(uandv.count_nonzero())
            b = float((u-uandv).count_nonzero())
            c = float((v-uandv).count_nonzero())
            P[P_idx] = (b/(a+b)+c/(a+c))/2.0
            P_idx += 1
    return P


#@profile
def HierarchyClusterRecipes(db,cursor,rec_ids):

    X = ConstructXfromRecIds(db,cursor,rec_ids)

    #H = fastcluster.linkage_vector(X,method='single',metric='kulsinski',)
    #H = fastcluster.linkage(X,method='single',metric='kulsinski',)
    #del H

    X = scipy.sparse.csr_matrix(X)
    
    time_before = time.time()
    X = pdist_sparse(X)
    #X = scipy.spatial.distance.pdist(X,'kulsinski')
    print("Time to calc pdist: {} seconds".format(time.time()-time_before))

    time_before = time.time()
    H = fastcluster.linkage(X,method='complete')
    #H = fastcluster.linkage(X,method='complete',metric='kulsinski')
    print("Time to calc H: {} seconds".format(time.time()-time_before))

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

    print("Time to fetch data: {} seconds".format(time.time()-time_before))
        
    rec_ids_idx = {rec_id:rec_ids.index(rec_id) for rec_id in rec_ids}

    num_recs = len(rec_ids)
    max_ingred_id = 5000 # Temporary value

    time_before = time.time()

    # max_ingred_id+1 so that we can index starting at 1
    X = np.zeros((num_recs,max_ingred_id+1),dtype='bool')
    
    for rec_ingred in rec_ingred_rows:
        X[rec_ids_idx[rec_ingred['rec_id']],rec_ingred['ingred_id']] = True

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


    num_recipes = int(1000.0)
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

    
