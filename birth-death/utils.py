import numpy as np
import pandas as pd
from numpy import log

from tree import BDTree


def generate_tree(bd, T, k_i):
    tree = BDTree(bd, T)
    tree.write_tree(bd, k_i)
    return tree


def count_extinct_bd(bd_list):
    return sum([bd.extinct() for bd in bd_list])


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

