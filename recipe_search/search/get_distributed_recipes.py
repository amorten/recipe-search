
#from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import fcluster
import numpy as np
import time
import MySQLdb
import random

def get_distributed_recipes(ingred,metric,num_clusters_list,
                            data_dir="/Users/amorten/Projects/"
                                      "RecipeSearch/Database/HClusters/"):

    time_start = time.time()
    
    # Needs some error checking here
    # i.e. need to check if the following files exist
    Z = np.load(data_dir+metric+'/hc_'+ingred+'.npy',allow_pickle=False)
    rec_ids = np.load(data_dir+metric+'/rec_ids_'+ingred+'.npy',allow_pickle=False)

    # Now get random recipes incrementally in groups,
    # Where each time you increase the number of clusters
    #  you still keep the old recipes

    time_before = time.time()
    
    rand_rec_ids_list = [ [] for _ in range(len(num_clusters_list)) ] 
    
    for idx in range(len(num_clusters_list)):
        num_clusters = num_clusters_list[idx]
        cluster_nums = fcluster(Z,t=num_clusters,criterion='maxclust')
        cluster_dict = {}
        for cluster_num,rec_id in zip(cluster_nums,rec_ids):
            cluster_dict.setdefault(cluster_num,[]).append(rec_id)
        # cluster_dict now has the form
        #  (key,value)=(cluster_num,list of rec_ids in cluster)
        
        # Now find out which clusters previous rec_ids were in
        if idx>0:
            prev_rand_rec_ids = rand_rec_ids_list[idx-1]
            for rec_id in prev_rand_rec_ids:
                cluster_num = cluster_nums[rec_ids.tolist().index(rec_id)]
                # Make the previously selected rec_id the only choice
                #  in the new cluster.
                cluster_dict[cluster_num] = [rec_id]
        # Get a random recipe from each new cluster
        rand_rec_ids=[random.choice(rec_ids_subset)
                      for rec_ids_subset in cluster_dict.values()]
        # Re-order rand_rec_ids so that the first elements are the
        #  same as prev_rand_rec_ids
        if idx>0:
            for idx_prev in range(len(prev_rand_rec_ids)):
                # rec_id_prev is the rec_id at index idx_prev
                rec_id_prev = prev_rand_rec_ids[idx_prev]
                idx_curr = rand_rec_ids.index(rec_id_prev)
                rand_rec_ids[idx_curr] = rand_rec_ids[idx_prev]
                rand_rec_ids[idx_prev] = rec_id_prev
            
        rand_rec_ids_list[idx] = rand_rec_ids
        #print "num_clusters = {}: {}".format(num_clusters,rand_rec_ids)
        
    #print("Calculations: {} seconds".format(time.time()-time_before))
    #print("Total run time: {} seconds".format(time.time()-time_start))

    return rand_rec_ids_list
