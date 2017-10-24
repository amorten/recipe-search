
import recipe_search
import recipe_search.database
import recipe_search.cluster
import recipe_search.search
import recipe_search.analyze

import MySQLdb

rs = recipe_search

db = rs.database.get_db("localhost","root","pwd4recDB","recipes_small")
cursor = rs.database.get_cursor(db)

num_ingreds_to_print=100
#tot_runtime = rs.cluster.estimate_run_time(cursor,num_ingreds_to_print)

#ingred = 'mushrooms'
#ingred = 'carrots' 
#ingred = 'chocolate'
ingred = 'raisins'
#ingred = 'ears'
#ingred = 'couscous'
#ingred = 'rice' 
metric = 'jaccard'
data_dir = ("/Users/amorten/Projects/RecipeSearch/Data/"
            "recipes_small/HClusters/")
#rs.cluster.cluster_by_ingred(cursor,ingred,metric,data_dir)



num_clusters_list = [5,10,15]
#ingred = 'mushrooms'
#ingred = 'carrots'
#ingred = 'chocolate'
ingred = 'raisins'
#ingred = 'ears'
#ingred = 'couscous'
metric = 'jaccard'
data_dir = ("/Users/amorten/Projects/RecipeSearch/Data/"
            "recipes_small/HClusters/")
rand_rec_ids_list = rs.search.get_distributed_recipes(
    ingred,metric,num_clusters_list,
    data_dir)


#print rand_rec_ids_list

for idx in range(len(num_clusters_list)):

    rec_ids = rand_rec_ids_list[idx]
    rec_rows = rs.database.get_recipe_info(cursor,rec_ids,'rec_name')
    
    #print("Search results (using clusters), first {} recipes:".format(len(rec_ids)))
    #print('\t'+'\n\t'.join([rec_row['rec_name'] for rec_row in rec_rows]))

    #print rec_rows


num_recipes_list = [5,10,15]
ingred = 'mushrooms'
rand_rec_ids_list = rs.search.get_random_recipes(cursor,ingred,num_recipes_list)

for idx in range(len(num_recipes_list)):

    rec_ids = rand_rec_ids_list[idx]
    rec_rows = rs.database.get_recipe_info(cursor,rec_ids,'rec_name')    
    #print("Search results (random), first {} recipes:".format(len(rec_ids)))
    #print('\t'+'\n\t'.join([rec_row['rec_name'] for rec_row in rec_rows]))


ingred = 'mushrooms'
metric = 'jaccard'
inc=5
max_num_recipes = 15
num_trials = 2
data_dir = ("/Users/amorten/Projects/RecipeSearch/Data/"
            "recipes_small/HClusters/")
rs.analyze.compare_cluster_vs_random(cursor,ingred,metric,
                          inc,max_num_recipes,num_trials,
                          data_dir)



