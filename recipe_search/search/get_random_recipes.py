
import random
from ..cluster import get_rec_ids_for_ingred

def get_random_recipes(cursor,ingred,num_recipes_list):

    # First, handle the case where the user sets
    # num_recipes_list as an integer instead of
    # a list of integers.  In that case, we will
    # return a single list of recipes (rather than
    # a list containing a list of recipes).
    if isinstance(num_recipes_list, (int,long) ):
        return_unnested_single_list = True
        num_recipes_list = [num_recipes_list]
    else:
        return_unnested_single_list = False

        
    rec_ids = get_rec_ids_for_ingred(cursor,ingred)

    max_num_recipes = max(num_recipes_list)

    rand_rec_ids = random.sample(rec_ids,max_num_recipes) #sample w/o replace

    rand_rec_ids_list = [ rand_rec_ids[:num_recipes]
                          for num_recipes in num_recipes_list ]

    if return_unnested_single_list:
        return rand_rec_ids_list[0]
    else:
        return rand_rec_ids_list
