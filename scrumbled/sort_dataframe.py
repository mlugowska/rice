def slice_dataframe(df, column_name, value):
    return df.loc[df[column_name] == value]


# get next column that is not equal to previous
def get_next_column_name_to_sort_1(df, first_column_name, sorted_columns, rejected, skipped):
    df = slice_dataframe(df, first_column_name, 1)
    for (index, colname) in enumerate(df):
        if colname in rejected:
            continue
        elif colname == first_column_name:
            rejected.append(colname)
            continue
        elif 1 not in df[colname].values:
            rejected.append(colname)
            continue
        elif df[colname].equals(df[df.columns[index - 1]]):
            skipped.append(colname)
            rejected.append(colname)
            continue
        else:
            sorted_columns.append(colname)
            return colname, rejected, skipped


# get next column that is not equal to previous
def slice_interim_dataframe_with_0(df, first_column_name, next_main_column):
    df_with_1 = slice_dataframe(df, first_column_name, 1)
    for (index, colname) in enumerate(df_with_1):
        if 0 in df_with_1[colname].values:
            if df_with_1[next_main_column].value_counts()[0] >= 2:
                return df_with_1.loc[df_with_1[next_main_column] == 0]

            df_inter = slice_dataframe(df_with_1, next_main_column, 0)
            for column_inter in df_inter.iloc[:, df.columns.get_loc(next_main_column):]:
                if 1 in df_inter[column_inter].values:
                    return df_inter.loc[df_inter[column_inter] == 1]


def sort_rows_by_random_number(df):
    new_df = df[df.index != 'freq'].sort_values(by='random', ascending=True)
    new_df.loc['freq'] = df.loc[:, df.columns != 'random'].mean(axis=0)
    new_df = new_df.fillna(0)
    return new_df