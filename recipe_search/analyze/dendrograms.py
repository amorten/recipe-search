
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5

def plot_dendrogram(ingred,metric,
                    data_dir="/Users/amorten/Projects/"
                    "RecipeSearch/Database/HClusters/",
                    ylim=[0.9,1.0]):

    
    Z = np.load(data_dir+metric+'/hc_'+ingred+'.npy',allow_pickle=False)
    
    plt.title('Truncated Hierarchical Clustering Dendrogram'
              '(ingred='+ingred+', num_clusters=50, metric='+metric+', method=complete)')
    plt.xlabel('sample index or (cluster size)',fontsize=14)
    plt.ylabel(metric+' distance',fontsize=14)
    
    dendrogram(
        Z,
        truncate_mode='lastp',  # show only the last p merged clusters
        p=50,  # show only the last p merged clusters
        leaf_rotation=90.,
        leaf_font_size=12.,
        #show_contracted=True,  # to get a distribution impression in truncated branches
        count_sort='descendant',
        ax=plt.gca()
    )
    #plt.ylim([0.978,1.0])
    plt.ylim(ylim)

    fig = plt.gcf()
    #fig.set_size_inches(10, 5, forward=True)
    #fig.savefig('HClusters/'+metric+'/dend_50_'+ingred+'.png', dpi=100)

    plt.show()
    
