

def GetSortedRecipes(ingred,method):

    import numpy as np
    import scipy.spatial

    
    P = np.load('HClusters/'+method+'/pdist_'+ingred+'.npy',allow_pickle=False)
    P = scipy.spatial.distance.squareform(P)
    n = P.shape[0]
    P[range(n),range(n)] = 1.0
    Pamin0 = np.amin(P,axis=0)
    Pamin0argsort = np.argsort(Pamin0)

    rec_ids = np.load('HClusters/'+method+'/rec_ids_'+ingred+'.npy',allow_pickle=False)

    rec_ids_sorted = rec_ids[Pamin0argsort]
    distances_sorted = np.sort(Pamin0)

    return {'rec_ids_sorted':rec_ids_sorted,'distances_sorted':distances_sorted}

if __name__ == '__main__':

    method = 'jacaar'
    #method = 'kulsinski'

    ingred = 'mushrooms'

    rec_ids = GetSortedRecipes(ingred,method)
