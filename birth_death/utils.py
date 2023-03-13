import numpy as np
import pandas as pd
from ete3 import TreeStyle, Tree, NodeStyle, TextFace
from numpy import log

from tree import BDTree


def generate_tree(bd, b_0, b_1, b_2, T, k_i, k, s):
    tree = BDTree(bd=bd, b_0=b_0, b_1=b_1, b_2=b_2, T=T, s=s)
    if tree.tree:
        tree.write_tree(k_i=k_i, k=k)
    return tree


def show_tree(tree, k=None, k_i=None, N=None):
    if isinstance(tree, str):
        tree = Tree(tree)
    ts = TreeStyle()
    ts.show_branch_length = True
    ts.branch_vertical_margin = 20
    ts.scale = 10
    ts.rotation = 90
    ts.force_topology = False

    lstyle = NodeStyle()
    lstyle["size"] = 2

    nstyle = NodeStyle()
    nstyle["fgcolor"] = "brown"
    nstyle["size"] = 0.5

    colors = {'0': 'blue', '1': "green", '2': 'red'}

    for node in tree.traverse():
        if node.is_leaf():
            lstyle["fgcolor"] = colors[f'{node.clone}']
            node.set_style(lstyle)
        else:
            # node.add_face(TextFace(f'name: {node.name}', tight_text=True, fsize=3), column=0, position="branch-bottom")
            node.set_style(nstyle)

        if node.own_mu:
            face = TextFace(node.own_mu, tight_text=True, fsize=3)
            face.margin_top = 3
            face.margin_right = 3
            face.margin_left = 3
            face.margin_bottom = 3
            node.add_face(face, column=0, position='branch-top')

        node.add_face(TextFace(f'clone: {node.clone}', tight_text=True, fsize=4), column=1, position="branch-bottom")

    # tree.show(tree_style=ts)
    tree.render(f'/Users/magdalena/PycharmProjects/rice/birth_death/results/1x/trees/0-N-{N}.pdf', tree_style=ts, dpi=500)


# # TODO Rename this here and in `show_tree`
def _extracted_from_show_tree_9(arg0, arg1):
    result = NodeStyle()
    result["fgcolor"] = arg0
    result["size"] = arg1

    return result


def count_extinct_bd(bd_list):
    return sum(bd.extinct() for bd in bd_list)


def remove_extinct_bd(bd_list):
    for bd in bd_list:
        if bd.extinct():
            bd_list.remove(bd)
    return bd_list


def calculate_mean_bd(df: pd.DataFrame):
    return df.mean(axis=0).apply(np.floor)


def calculate_median_bd(df: pd.DataFrame):
    return df.median(axis=0)


def calculate_mean_log_bd(df: pd.DataFrame):
    mean_N_in_m_dt = calculate_mean_bd(df)
    return log(mean_N_in_m_dt)


def calculate_median_log_bd(df: pd.DataFrame):
    median_N_in_m_dt = calculate_median_bd(df)
    return log(median_N_in_m_dt)


def get_tree_paths(tree):
    return tree.get_leaves_path()


def calculate_mean_birthtime(df):
    return df["birthtime"].mean(axis=0)


def calculate_mean_deathtime(df):
    return df.loc[df["deathtime"] != 0.0]["deathtime"].mean(axis=0)


def calculate_mean_lifetime(df):
    return df.loc[df["lifetime"] != 0.0]["lifetime"].mean(axis=0)


def mean_sfs(df_list):
    df_concat = pd.concat(df_list)
    by_row_index = df_concat.groupby(df_concat.index)
    return by_row_index.mean().apply(np.floor).astype(int)
