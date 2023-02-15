import numpy as np
import pandas as pd
from ete3 import TreeStyle, Tree, NodeStyle, TextFace, AttrFace
from numpy import log

from tree import BDTree


def generate_tree(bd, T, k_i, k, Ki):
    tree = BDTree(bd=bd, T=T, Ki=Ki)
    # if tree.tree:
    #     tree.write_tree(bd=bd, k_i=k_i, k=k)
    return tree


def show_tree(tree, k, k_i, N):
    if isinstance(tree, str):
        tree = Tree(tree)
    ts = TreeStyle()
    ts.scale = 120
    ts.rotation = 90
    ts.force_topology = False

    lstyle = NodeStyle()
    lstyle["fgcolor"] = "green"
    lstyle["size"] = 1.5

    nstyle = NodeStyle()
    nstyle["fgcolor"] = "brown"
    nstyle["size"] = 0.5

    for node in tree.traverse():
        if node.is_leaf():
            node.set_style(lstyle)
        else:
            node.add_face(TextFace(node.name, tight_text=True, fsize=3), column=0, position="branch-bottom")
            node.set_style(nstyle)

        if node.own_mu:
            face = TextFace(node.own_mu, tight_text=True, fsize=3)
            face.margin_top = 3
            face.margin_right = 3
            face.margin_left = 3
            face.margin_bottom = 3
            node.add_face(face, column=0, position='branch-top')

        node.add_face(TextFace(round(node.dist, 3), tight_text=True, fsize=2), column=0, position="float")

    tree.show(tree_style=ts)
    tree.render(f'/Users/magdalena/PycharmProjects/rice/birth-death/results/{k}x/trees/{k_i}-N-{N}.pdf')


def count_extinct_bd(bd_list):
    return sum([bd.extinct() for bd in bd_list])


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
