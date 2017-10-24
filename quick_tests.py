
import recipe_search
import recipe_search.database
import recipe_search.cluster
import recipe_search.search

import MySQLdb

rs = recipe_search

db = rs.database.get_db("localhost","root","pwd4recDB","recipes")
cursor = rs.database.get_cursor(db)

num_ingreds_to_print=100
#tot_runtime = rs.cluster.estimate_run_time(cursor,num_ingreds_to_print)

ingred = 'mushrooms'
#ingred = 'carrots' # takes about 4 min (fits in memory)
#ingred = 'ears'
#ingred = 'couscous'
#ingred = 'rice' # takes about 40 min (doesn't fit in memory; should be 8 min)
metric = 'jaccard'
rs.cluster.cluster_by_ingred(cursor,ingred,metric)


num_clusters_list = [5,10,15]
ingred = 'mushrooms'
#ingred = 'ears'
#ingred = 'couscous'
metric = 'jaccard'

rand_rec_ids_list = rs.search.get_distributed_recipes(ingred,metric,num_clusters_list)

#print rand_rec_ids_list

for idx in range(len(num_clusters_list)):

    rec_ids = rand_rec_ids_list[idx]
    rec_rows = rs.database.get_recipe_info(cursor,rec_ids,'rec_name')
    
    print("Search results, first {} recipes:".format(len(rec_ids)))
    print('\t'+'\n\t'.join([rec_row['rec_name'] for rec_row in rec_rows]))

    #print rec_rows
    




