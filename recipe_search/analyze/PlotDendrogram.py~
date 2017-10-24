
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5

def PlotDendrogram(ingred,method,Z):

    
    #Z = np.load('HClusters/'+method+'/hc_'+ingred+'.npy',allow_pickle=False)
    
    plt.title('Truncated Hierarchical Clustering Dendrogram (ingred=mushrooms, num_clusters=50, method=complete)')
    plt.xlabel('sample index or (cluster size)')
    plt.ylabel('jaccard distance')
    
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
    plt.ylim([0.978,1.0])

    fig = plt.gcf()
    #fig.set_size_inches(10, 5, forward=True)
    fig.savefig('HClusters/'+method+'/dend_50_'+ingred+'.png', dpi=100)

    plt.show()
    
