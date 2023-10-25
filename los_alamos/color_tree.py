import pandas as pd
from ete3 import Tree

from birth_death.utils import show_tree

# ========== files from Andrew
# # ---------- read newick tree
# tree = Tree('/Users/magdalena/PycharmProjects/rice/los_alamos/trees/Batch4_Sim4A.nh')
#
# # ---------- read clone info
# df = pd.read_csv('/Users/magdalena/Documents/PhD/RU/sortowanie/For_Magda_Anonymous/Batch4_Sim4A.csv')
# df.drop(columns=['Row', 'Marker', 'hclust_index'], inplace=True)
# clone = df.loc[0]
#
# # ---------- add clone info to node
# tree.add_feature('clone', 0)
#
# for node in tree.iter_leaves():
#     node.clone = str(clone[node.name])
#
# # ---------- show tree
# show_tree(tree, N=len(df.columns), outfile='/Users/magdalena/PycharmProjects/rice/los_alamos/trees/Batch4_Sim4A.pdf',
# from_bd_process=False)


# ========== files from bd process
# ---------- read newick tree
tree = Tree('/Users/magdalena/PycharmProjects/rice/birth_death/results/T=260/los_alamos/4-N-443.nh')

# ---------- read clone info
N = 1118
df = pd.read_excel('/Users/magdalena/PycharmProjects/rice/birth_death/results/40/N-709-stats.xlsx',
                   index_col=0, dtype=str)
mu = pd.read_excel('/Users/magdalena/PycharmProjects/rice/birth_death/results/40/N-709-mu-occur.xlsx',
                   dtype=str)
mu = mu.set_index(keys=['Unnamed: 0'])
clone = df['clone']

for index in mu.index:
    mu.at[index, 'clone'] = int(clone[index])
mu = mu.astype(int)
mu.to_excel('/Users/magdalena/PycharmProjects/rice/birth_death/results/40/N-709--mutation-table-clones.xlsx')

# ---------- add clone info to node
tree.add_feature('clone', 0)

for node in tree.iter_leaves():
    node.clone = str(clone[node.name])

# ---------- show tree
show_tree(tree, N=len(tree.get_leaves()),
          outfile='/Users/magdalena/PycharmProjects/rice/birth_death/results/T=260/los_alamos/4-N-443.pdf',
          from_bd_process=False)
