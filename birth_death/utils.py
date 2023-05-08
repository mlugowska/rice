import numpy as np
import pandas as pd
from ete3 import TreeStyle, Tree, NodeStyle, TextFace
from numpy import log

from tree import BDTree
PATH = '/Users/magdalena/PycharmProjects/rice/birth_death/results'


def generate_tree(bd, b_0, b_1, b_2, T, k_i, k, t_1, t_2):
    tree = BDTree(bd=bd, b_0=b_0, b_1=b_1, b_2=b_2, T=T, t_1=t_1, t_2=t_2)
    if tree.tree:
        tree.write_tree(k_i=k_i, k=k)
    return tree


def show_tree(tree, k=None, k_i=None, N=None, outfile=None, from_bd_process=True):
    if isinstance(tree, str):
        tree = Tree(tree)
    ts = TreeStyle()
    ts.show_branch_length = True
    ts.branch_vertical_margin = 60
    ts.scale = 10
    ts.rotation = 90
    ts.force_topology = False

    colors = {'0': 'blue', '1': "green", '2': 'red'}

    if from_bd_process:
        for node in tree.traverse():
            # node.add_face(TextFace(f'clone: {node.clone}', tight_text=True, fsize=4), column=1, position="branch-bottom")

            node.img_style['hz_line_color'] = colors[f'{node.clone}']  # horizontal line color
            node.img_style['vt_line_color'] = colors[f'{node.clone}']  # vertical line color
            node.img_style['hz_line_width'] = 8  # vertical line color
            node.img_style['vt_line_width'] = 8  # vertical line color

            node.img_style['fgcolor'] = colors[f'{node.clone}']

            # if node.own_mu:
            #     face = TextFace(node.own_mu, tight_text=True, fsize=3)
            #     face.margin_top = 3
            #     face.margin_right = 3
            #     face.margin_left = 3
            #     face.margin_bottom = 3
            #     node.add_face(face, column=0, position='branch-top')
    else:
        for node in tree.iter_leaves():
            node.add_face(TextFace(f'clone: {node.clone}', tight_text=True, fsize=4), column=1,
                          position="branch-bottom")

            node.img_style['size'] = 8

            node.img_style['fgcolor'] = colors[f'{node.clone}']

    # tree.show(tree_style=ts)
    if not outfile:
        outfile = f'{PATH}/N-{N}.pdf'
    tree.render(outfile, tree_style=ts, dpi=500)


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
