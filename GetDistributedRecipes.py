
#from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import fcluster
import numpy as np
import time
import MySQLdb
import random



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

    ingred = "mushrooms"
    metric='jaccard'

    Z = np.load('HClusters/'+metric+'/hc_'+ingred+'.npy',allow_pickle=False)

    num_clusters = 5
    
    cluster_nums = fcluster(Z,t=num_clusters,criterion='maxclust')

    rec_ids = np.load('HClusters/'+metric+'/rec_ids_'+ingred+'.npy',allow_pickle=False)
    

    
    cluster_dict = {}
    for cluster_num,rec_id in zip(cluster_nums,rec_ids):
        cluster_dict.setdefault(cluster_num,[]).append(rec_id)

    # cluster_dict now has the form
    #  (key,value)=(cluster_num,list of rec_ids in cluster)
        
    # Get a random recipe from each cluster

    rand_rec_ids=[random.choice(rec_ids_subset) for rec_ids_subset in cluster_dict.values()]

    #print rand_rec_ids

    # Now get random recipes incrementally in groups,
    # Where each time you increase the number of clusters
    #  you still keep the old recipes

    time_before = time.time()
    
    num_clusters_list = [5,10,15]
    rand_rec_ids_list = [[],[],[],[]]
    
    for idx in range(len(num_clusters_list)):
        num_clusters = num_clusters_list[idx]
        cluster_nums = fcluster(Z,t=num_clusters,criterion='maxclust')
        cluster_dict = {}
        for cluster_num,rec_id in zip(cluster_nums,rec_ids):
            cluster_dict.setdefault(cluster_num,[]).append(rec_id)
        #Now find out which clusters previous rec_ids were in
        if idx>0:
            prev_rand_rec_ids = rand_rec_ids_list[idx-1]
            for rec_id in prev_rand_rec_ids:
                cluster_num = cluster_nums[rec_ids.tolist().index(rec_id)]
                cluster_dict[cluster_num] = [rec_id]
        rand_rec_ids=[random.choice(rec_ids_subset)
                      for rec_ids_subset in cluster_dict.values()]
        # Re-order rand_rec_ids so that the first elements are the
        #  same as prev_rand_rec_ids
        if idx>0:
            for idx_prev in range(len(prev_rand_rec_ids)):
                rec_id_prev = prev_rand_rec_ids[idx_prev]
                #rec_id_temp = rand_rec_ids[idx]
                rand_rec_ids[rand_rec_ids.index(rec_id_prev)] = rand_rec_ids[idx_prev]
                rand_rec_ids[idx_prev] = rec_id_prev
            
        rand_rec_ids_list[idx] = rand_rec_ids
        #print "num_clusters = {}: {}".format(num_clusters,rand_rec_ids)
        
    print("Calculations: {} seconds".format(time.time()-time_before))
    print("Total run time: {} seconds".format(time.time()-time_start))
