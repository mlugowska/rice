import pandas as pd
from ete3 import Tree

from birth_death.tree import BDTree


def get_mutations_list(leaves):
    leaf_mu = list()
    for leaf in leaves:
        leaf_mu += f'{leaf.inherited_mu.replace("|", ",")},{leaf.own_mu.replace("|", ",")}'.split(',')
    return list(set(map(int, list(filter(None, leaf_mu)))))


def create_dataframe(leaves, mutations):
    df = pd.DataFrame(index=[leaf.name for leaf in leaves], columns=mutations)
    df = df.fillna(0)
    return df


def get_leaf_mutations(leaf):
    leaf_mu = f'{leaf.inherited_mu.replace("|", ",")},{leaf.own_mu.replace("|", ",")}'.split(',')
    return list(set(map(int, list(filter(None, leaf_mu)))))


def add_mutations_to_dataframe(df, mutations, leaves):
    for mu in mutations:
        for leaf in leaves:
            leaf_mu = get_leaf_mutations(leaf)
            if mu in leaf_mu:
                df.at[leaf.name, mu] = 1

    return df


def create_dataframe_from_tree(tree):
    bd_tree = BDTree()
    bd_tree.tree = tree
    leaves = tree.get_leaves()
    mutations = get_mutations_list(leaves)
    df = create_dataframe(leaves, mutations)
    df = add_mutations_to_dataframe(df, mutations, leaves)
    return df
