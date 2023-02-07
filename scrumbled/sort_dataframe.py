def slice_dataframe(df, column_name):
    return df.loc[df[column_name] == 1]


# get next column that is not equal to previous
def get_next_column_name_to_sort(df, first_column_name, rejected=[]):
    df = slice_dataframe(df, first_column_name)
    for (index, colname) in enumerate(df):
        if colname in rejected:
            continue
        elif colname == first_column_name:
            rejected.append(colname)
            continue
        elif df[colname].equals(df[df.columns[index - 1]]):
            rejected.append(colname)
            continue
        elif 1 not in df[colname].values:
            rejected.append(colname)
            continue
        else:
            return colname, rejected


def sort_rows_by_random_number(df):
    new_df = df[df.index != 'freq'].sort_values(by='random', ascending=True)
    new_df.loc['freq'] = df.loc[:, df.columns != 'random'].mean(axis=0)
    new_df = new_df.fillna(0)
    return new_df