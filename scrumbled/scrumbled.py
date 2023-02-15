import sys

sys.path.append('/Users/magdalena/PycharmProjects/rice/scrumbled')

import numpy as np
import pandas as pd
from ete3 import Tree

from create_mutation_dafaframe import create_dataframe_from_tree
from sort_dataframe import sort_rows_by_random_number, get_next_column_name_to_sort_1, \
    slice_interim_dataframe_with_0
from styler import styler

# ==================== dataframe from tree ==============================================
# ==================== create dataframe with mutations ==================================
tree = Tree('/Users/magdalena/PycharmProjects/rice/scrumbled/sample_tree.txt', format=0)
df = create_dataframe_from_tree(tree)

# ==================== OR ================================================================

# ==================== read dataframe from file ==========================================
# df = pd.read_excel('/Users/magdalena/PycharmProjects/rice/scrumbled/tree_2.xlsx', engine='openpyxl', index_col=0)
# df = pd.read_excel('/Users/magdalena/Documents/PhD/RU/sortowanie/HCC9-T.xlsx', engine='openpyxl', index_col=0)
# df = df.apply(lambda row: row.fillna(row.value_counts().index[0]), axis=1)

# ==================== generate random number for each row/cell ==========================
np.random.seed(10)
df['random'] = 0

for ind in df.index:
    df['random'][ind] = np.random.random()

# ==================== add average mutation frequency among all cells ====================
df.loc['freq'] = df.loc[:, df.columns != 'random'].mean(axis=0)

# ==================== SORT 1 rows by random number ======================================
df_sorted_by_random = sort_rows_by_random_number(df)

# ==================== SORT 2 columns by max freq ========================================
df_sorted_by_freq = df_sorted_by_random.sort_values(df_sorted_by_random.last_valid_index(), ascending=False, axis=1,
                                                    kind='mergesort')

# ==================== SORT 3 column with max freq =======================================
first_column_name = df_sorted_by_freq.columns[0]
df_sorted = df_sorted_by_freq[df_sorted_by_freq.index != 'freq'].sort_values(by=first_column_name, kind='mergesort')

sorted_columns = [first_column_name]

# df_4 = styler(df_4, first_column_name, '#dbf0de', name='styled')

# ==================== SORT 4 next columns ===============================================
# i = 0
# colors = ['#eaf2ed', '#abcbb8', '#bbd4c6', '#caded3', '#dae8e0']
rejected = []
skipped = []
while True:
    try:
        next_column_name, rejected, skipped = get_next_column_name_to_sort_1(
            df=df_sorted, first_column_name=first_column_name, sorted_columns=sorted_columns, rejected=rejected, skipped=skipped)

        df_sorted_next = df_sorted[df_sorted.index != 'freq'].sort_values(by=sorted_columns, kind='mergesort')
        df_sorted = df_sorted_next
        first_column_name = next_column_name

        # df_styled = styler(df_sorted_next, first_column_name, colors[i], name=f'{next_column_name}')
        # i += 1
    except TypeError:
        print(f'first mutation line: {sorted_columns + skipped}')
        # df_sorted_next.loc['freq'] = df_sorted_by_freq.loc[:, df_sorted_by_freq.columns != 'random'].mean(axis=0)
        # df_sorted_next = df_sorted_next.fillna(0)
        # df_sorted_next.to_excel('final.xlsx')
        break

# df_sorted.to_excel('/Users/magdalena/Documents/PhD/RU/sortowanie/HCC9-T-sorted-once.xlsx')
df_sorted.to_excel('/Users/magdalena/PycharmProjects/rice/scrumbled/tree_2_sorted.xlsx')
# ========= SORT inside sorted ================

for index, column in enumerate(sorted_columns):
    print(f'-------- start {column}')
    first_column_name = column
    mutation_line = [first_column_name]

    try:
        next_main_column = sorted_columns[index + 1]
    except IndexError:
        next_main_column = column

    try:
        interim_df = slice_interim_dataframe_with_0(df_sorted, first_column_name, next_main_column)
    except KeyError:
        print('Dataframe sorted')

    if interim_df is None:
        continue

    rejected_inter = []
    skipped_inter = []
    while True:
        try:
            next_column_name, rejected_inter, skipped_inter = get_next_column_name_to_sort_1(
                df=interim_df, first_column_name=first_column_name, sorted_columns=mutation_line, rejected=rejected_inter, skipped=skipped_inter)

            interim_df_next = interim_df[interim_df.index != 'freq'].sort_values(by=mutation_line[-1], kind='mergesort')
            interim_df = interim_df_next
            first_column_name = next_column_name
        except TypeError:
            print(f'mutation line: {list(set(mutation_line + skipped_inter))}')

            index = df_sorted.loc[df_sorted.index.isin(interim_df.index)].index
            start = df_sorted.loc[df_sorted.index.isin(interim_df.index)].index[0]
            start_id = df_sorted.index.get_loc(start)
            before_start = df_sorted.index[start_id-1]

            stop = df_sorted.loc[df_sorted.index.isin(interim_df.index)].index[-1]
            stop_id = df_sorted.index.get_loc(stop)
            after_stop = df_sorted.index[stop_id+1]

            df = df_sorted.drop(index=index)
            df_sorted = df.loc[:before_start].append(interim_df).append(df.loc[after_stop:])
            print(f'-------- end {column}')
            break


df_sorted.to_excel('df_2.xlsx')
