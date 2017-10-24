
def get_recipe_info(cursor,rec_ids,db_col_names):

    # db_col_names is either a string or array of strings
    # In both cases, create db_col_names_str as the
    # comma-separated string of column names
    if isinstance(db_col_names,basestring):
        db_col_names_str = db_col_names
    else:
        db_col_names_str = ','.join(db_col_names)

    # Get the corresponding columns from the recipe database
    cursor.execute("SELECT "
                   +" rec_id, "+db_col_names_str
                   +""" FROM recipes 
                        WHERE rec_id
                        IN ("""+str(rec_ids).replace('L','')[1:-1]+")"
    )
    rec_rows = cursor.fetchall()

    # Each row of rec_rows is a dictionary of the form
    # {'rec_id':#, 'column name 1':'...', 'column name 2':'...', etc. }

    # Because MySQL returns results in arbitrary order,
    #  the order of rec_rows won't be the same as the
    #  order of rec_ids.
    # Therefore, let's re-order rec_rows so that they match:

    rec_ids_unordered = [rec_row['rec_id'] for rec_row in rec_rows]
    rec_rows_ordered = [rec_rows[rec_ids_unordered.index(rec_id)]
                        for rec_id in rec_ids]
    
    return rec_rows_ordered
