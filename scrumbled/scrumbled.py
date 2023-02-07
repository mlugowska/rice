import numpy as np
from ete3 import Tree

from create_mutation_dafaframe import create_dataframe_from_tree
from sort_dataframe import sort_rows_by_random_number, get_next_column_name_to_sort
from styler import styler
import sys
sys.path.append('/Users/magdalena/PycharmProjects/rice/scrumbled')
# ==================== create dataframe with mutations ==================================
tree = Tree('/Users/magdalena/PycharmProjects/rice/scrumbled/sample_tree.txt', format=0)
df = create_dataframe_from_tree(tree)

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
df_sorted_by_freq = df_sorted_by_random.sort_values(df_sorted_by_random.last_valid_index(), ascending=False, axis=1)

# ==================== SORT 3 column with max freq =======================================
first_column_name = df_sorted_by_freq.columns[0]
df_sorted_first = df_sorted_by_freq[df_sorted_by_freq.index != 'freq'].sort_values(by=first_column_name)

# df_4 = styler(df_4, first_column_name, '#dbf0de', name='styled')

# ==================== SORT 4 next columns ===============================================
# i = 0
# colors = ['#eaf2ed', '#abcbb8', '#bbd4c6', '#caded3', '#dae8e0']
while True:
    try:
        next_column_name, rejected = get_next_column_name_to_sort(df_sorted_first, first_column_name=first_column_name)
        df_sorted_next = df_sorted_first[df_sorted_first.index != 'freq'].sort_values(by=next_column_name)
        df_sorted_first = df_sorted_next
        first_column_name = next_column_name

        # df_styled = styler(df_sorted_next, first_column_name, colors[i], name=f'{next_column_name}')
        # i += 1
        print(next_column_name)
    except TypeError:
        print('DataFrame is sorted')
        df_sorted_next.loc['freq'] = df_sorted_by_freq.loc[:, df_sorted_by_freq.columns != 'random'].mean(axis=0)
        df_sorted_next = df_sorted_next.fillna(0)
        df_sorted_next.to_excel('final.xlsx')
        break
