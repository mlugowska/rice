import sys

sys.path.append('/Users/magdalena/PycharmProjects/rice/scrumbled')

from excel_writer import write_to_excel

import numpy as np
import pandas as pd

from sort_dataframe import sort_rows_by_random_number, get_next_column_name_to_sort_1

# ==================== dataframe from tree ==============================================
# ==================== create dataframe with mutations ==================================
# tree = Tree('/Users/magdalena/PycharmProjects/rice/scrumbled/sample_tree.txt', format=0)
# df = create_dataframe_from_tree(tree)

# ==================== OR ================================================================

# ==================== read dataframe from file ==========================================
df = pd.read_excel('/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/stats/0-N-151-mu-occur.xlsx',
                   engine='openpyxl', index_col=0)
# df = pd.read_excel('/Users/magdalena/Documents/PhD/RU/sortowanie/HCC9-T.xlsx', engine='openpyxl', index_col=0)
# df = pd.read_excel('/Users/magdalena/Documents/PhD/RU/sortowanie/łamigłówka/SCRAMBLED 2.xlsx', engine='openpyxl', index_col=0)
# df = pd.read_excel('/Users/magdalena/Documents/PhD/RU/sortowanie/Ivan Drivers LC18 120222 - to sort.xlsx', engine='openpyxl', index_col=0)
# df = df.transpose()
# df = df.replace([3], np.nan)
df = df.apply(lambda row: row.fillna(row.value_counts().index[0]), axis=1)


# ==================== permutation of row values in each column ==========================


def shuffle(df):
    rows = df.index
    columns = df.columns
    df_perm = pd.DataFrame(columns=columns, index=rows)

    for col in columns:
        sampler = np.random.permutation(df.shape[0])
        new_vals = df[col].take(sampler).values
        df_perm[col] = new_vals
    return df_perm


# df = shuffle(df)


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

# ==================== SORT 4 next columns ===============================================
rejected = []
skipped = []
while True:
    try:
        next_column_name, rejected, skipped = get_next_column_name_to_sort_1(
            df=df_sorted, first_column_name=first_column_name, sorted_columns=sorted_columns, rejected=rejected,
            skipped=skipped)

        df_sorted_next = df_sorted[df_sorted.index != 'freq'].sort_values(by=sorted_columns, kind='mergesort',
                                                                          ascending=True)
        df_sorted = df_sorted_next
        first_column_name = next_column_name
    except TypeError:
        print(f'first mutation line: {sorted_columns + skipped}')
        break

# ========= SORT upper rows ================
first_column_name = df_sorted.columns[0]
sorted_columns_upper = [first_column_name]
df_sorted_upper = df_sorted.loc[df_sorted[first_column_name] == 0]

rejected_upper = []
skipped_upper = []
while True:
    try:
        next_column_name, rejected_upper, skipped_upper = get_next_column_name_to_sort_1(
            df=df_sorted_upper, first_column_name=first_column_name, sorted_columns=sorted_columns_upper,
            rejected=rejected_upper, skipped=skipped_upper,
            pdb=True)

        df_sorted_next = df_sorted_upper[df_sorted_upper.index != 'freq'].sort_values(by=sorted_columns_upper,
                                                                                      kind='mergesort',
                                                                                      ascending=True)
        df_sorted_upper = df_sorted_next
        first_column_name = next_column_name

    except TypeError:
        print(f'first mutation line: {sorted_columns_upper + skipped_upper}')
        df_sorted = df_sorted_upper.append(df_sorted.loc[df_sorted[df_sorted.columns[0]] == 1])
        break

df_sorted.loc['freq'] = df_sorted_by_freq.loc['freq']

write_to_excel(df_sorted,
               '/birth_death/results/1x/old/stats/0-N-151-mu-occur sorted orig.xlsx')
