# recipe-search2

This repository contains the code for the module [recipe_search](../master/recipe_search/).

Within the [recipe_search](../master/recipe_search/) module there are five submodules:

1) The "[database](../master/recipe_search/database/)" submodule handles the creation and updating of the MySQL recipe database using recipe files assumed to be stored locally. 
2) The "[cluster](../master/recipe_search/cluster/)" submodule handles the creation of hierarchical clustering of the recipe data.
3) The "[search](../master/recipe_search/search/)" submodule handles search functionality to find recipes both directly from the database and through the heirarchical clusters.
4) The "[analyze](../master/recipe_search/analyze/)" submodule helps investigate the structure of the database and hierarchical clustering.
5) The "[web](../master/recipe_search/web/)" submodule will handle the web interface to the search functions, but is currently not implemented.

The following Jupyter notebooks highlight some of the above functionality of the five submodules:

1) [test_database.ipynb](../master/test_database.ipynb)
2) [test_cluster.ipynb](../master/test_cluster.ipynb)
3) [test_search.ipynb](../master/test_search.ipynb)
4) [test_analyze.ipynb](../master/test_analyze.ipynb) and [test_analyze_big_database.ipynb](../master/test_analyze_big_database.ipynb)

At the moment, several files named quick_\[something\].py exist to help me quickly test the code and try out new ideas.

