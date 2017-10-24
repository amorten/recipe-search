
import numpy as np
import scipy.spatial.distance
import scipy.stats as st
import matplotlib.pyplot as plt
from ..search import get_distributed_recipes
from ..search import get_random_recipes


def compare_cluster_vs_random(cursor,ingred,metric,
                              num_recipes_list=[10,20,30],num_trials=10,
                              data_dir="/Users/amorten/Projects/"
                                      "RecipeSearch/Database/HClusters/"):

    # Load and convert the saved pdist to squareform.
    pdist = scipy.spatial.distance.squareform(
        np.load(data_dir+metric+'/pdist_'+ingred+'.npy',allow_pickle=False)
        )
    # Load the rec_ids that index pdist
    pdist_rec_ids = np.load(data_dir+metric+'/rec_ids_'+ingred+'.npy',allow_pickle=False).tolist()
    
    num_clusters_list = num_recipes_list
     
    data_shape = (len(num_recipes_list),num_trials)
    
    # collective_distances[][] is a 2d numpy array
    collective_distances = {'random':
                            {'nearest':np.empty(data_shape),
                             'average':np.empty(data_shape)},
                            'cluster':
                            {'nearest':np.empty(data_shape),
                             'average':np.empty(data_shape)}}
    # e.g. collective_distances['random']['nearest'][num_rec_idx,trial_num]
    #       equals the nearest distance between randomly selected recipes
    #       when the number of recipes is num_recipes_list[num_rec_idx]
    #       for trial number trial_num.
    means = {'random':
             {'nearest':np.empty(data_shape[0]),
              'average':np.empty(data_shape[0])},
             'cluster':
             {'nearest':np.empty(data_shape[0]),
              'average':np.empty(data_shape[0])}}
    
    
    for trial_num in range(num_trials):

        random_recipes_list = get_random_recipes(cursor,ingred,num_recipes_list)

        cluster_recipes_list = get_distributed_recipes(ingred,metric,num_clusters_list,data_dir)

        # might want to find a more Python-fu way to do the following
        random_collective_distance_list = [
            collective_distance(rec_list,pdist,pdist_rec_ids)
            for rec_list in random_recipes_list ]
        cluster_collective_distance_list = [
            collective_distance(rec_list,pdist,pdist_rec_ids)
            for rec_list in cluster_recipes_list ]

        collective_distances['random']['nearest'][:,trial_num] = np.array(
            [ distance_dict['nearest']
              for distance_dict in random_collective_distance_list ] )
        collective_distances['cluster']['nearest'][:,trial_num] = np.array(
            [ distance_dict['nearest']
              for distance_dict in cluster_collective_distance_list ] )
        collective_distances['random']['average'][:,trial_num] = np.array(
            [ distance_dict['average']
              for distance_dict in random_collective_distance_list ] )
        collective_distances['cluster']['average'][:,trial_num] = np.array(
            [ distance_dict['average']
              for distance_dict in cluster_collective_distance_list ] )
        

    #print collective_distances['random']['nearest']
    #print collective_distances['cluster']['nearest']
    #print collective_distances['random']['average']
    #print collective_distances['cluster']['average']


    for select_method,distance_method in [(x,y) for x in ['random','cluster']
                                          for y in ['nearest','average']]:
        means[select_method][distance_method] = (
            collective_distances[select_method][distance_method].mean(axis=1))
        # I should calculate confidence intervals
        #conf_intervals[select_method][distance_method] = (
        #    st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a)))
        

    #print means

    label_fontsize = 14
    title_fontsize = 18
    
    plt.figure(1,figsize=(15,6))
    plt.subplot(1,2,1)
    plt.title('Recipe distances (smallest of nearest)',fontsize=title_fontsize)
    plt.plot(num_recipes_list,means['cluster']['nearest'],'bs',
             label='cluster',linewidth=2)
    plt.plot(num_recipes_list,means['random']['nearest'],'r^',
             label='random',linewidth=2)
    #plt.xscale('log') 
    plt.axis([0,num_recipes_list[-1],0,1.0])
    plt.ylabel('smallest of nearest distance',fontsize=label_fontsize)
    plt.xlabel('number of recipes',fontsize=label_fontsize)
    plt.legend()
    plt.subplot(1,2,2)
    plt.title('Recipe distances (average of nearest)',fontsize=title_fontsize)
    plt.plot(num_recipes_list,means['cluster']['average'],'bs',
             label='cluster',linewidth=2)
    plt.plot(num_recipes_list,means['random']['average'],'r^',
             label='random',linewidth=2)
    #plt.xscale('log')
    plt.axis([0,num_recipes_list[-1],0,1.0])
    plt.ylabel('average of nearest distance',fontsize=label_fontsize)
    plt.xlabel('number of recipes',fontsize=label_fontsize)
    plt.legend()
    plt.show()
    
    
def collective_distance(rec_list,pdist,pdist_rec_ids):

    rec_list_idxs = [pdist_rec_ids.index(rec_id) for rec_id in rec_list]

    pdist_slice = pdist[rec_list_idxs,:][:,rec_list_idxs]

    #print pdist_slice

    n = pdist_slice.shape[0]
    pdist_slice[range(n),range(n)] = 1.0
    distance_to_nearest_recipe = np.amin(pdist_slice,axis=0)

    #print {'nearest': np.amin(distance_to_nearest_recipe),
    #        'average': np.mean(distance_to_nearest_recipe)}

    return {'nearest': np.amin(distance_to_nearest_recipe),
            'average': np.mean(distance_to_nearest_recipe)}


