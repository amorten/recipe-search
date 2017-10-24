
import numpy as np
import recipe_search
import recipe_search.database
import recipe_search.cluster
import recipe_search.search
import recipe_search.analyze
rs = recipe_search
import MySQLdb



db = rs.database.get_db("localhost","root","pwd4recDB","recipes_small")
cursor = rs.database.get_cursor(db)

ingred = 'mushrooms'
#ingred = 'carrots'
#ingred = 'chocolate'
#ingred = 'raisins'
#ingred = 'ears'
#ingred = 'couscous'

metric = 'jaccard'
#num_recipes_list = range(2,10)+range(10,100,10)+range(100,1000,100)
num_recipes_list = [10,20,30,40,50,60,70,80,90,100]
#num_recipes_list = [100,200,300,400,500,600,700,800,900,1000]
num_trials = 1
data_dir = ("/Users/amorten/Projects/RecipeSearch/Data/"
            "recipes_small/HClusters/")

# The following three lines calculate and save the pdist matrix (only do once):
#rec_ids = rs.cluster.get_rec_ids_for_ingred(cursor,ingred)
#np.save(data_dir+metric+'/rec_ids_'+ingred+'.npy',np.array(rec_ids,dtype=np.int64),allow_pickle=False)
#rs.cluster.save_pdist(cursor,ingred,metric,rec_ids,data_dir)


#rs.analyze.compare_cluster_vs_random(cursor,ingred,metric,
#                          num_recipes_list,num_trials,
#                          data_dir)

#ylim=[0.94,1.0]
#rs.analyze.plot_dendrogram(ingred,metric,data_dir=data_dir,ylim=ylim)

