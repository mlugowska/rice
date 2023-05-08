"""
http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#trees
https://github.com/tresoldi/ngesh/blob/866b90003019a34eb297a543e22d2aea8ddffc31/src/ngesh/random_tree.py#L26
"""
import logging
import os
import random
from typing import List

import numpy as np
from ete3 import Tree, TreeNode
PATH = '/Users/magdalena/PycharmProjects/rice/birth_death/results'

logging.basicConfig(filename=f'{PATH}/bd_run.txt', level=logging.INFO)
logger = logging.getLogger(__name__)

# PATH = '/net/ascratch/people/plgmlugowska/rice'


class BDTree:
    def __init__(self, bd, b_0, b_1, b_2, T=0, t_1=0, t_2=0):
        self.N_2 = None
        self.N_1 = None
        self.N_0 = None
        self.mu_clone_1 = None
        self.mu_clone_2 = None
        self.bd = bd
        self.b_0 = b_0
        self.b_1 = b_1
        self.b_2 = b_2
        self.clone_1_exsists = False
        self.clone_2_exsists = False
        self.create_clone_1 = True
        self.create_clone_2 = True
        self.tree = self.create_tree(T=T, t_1=t_1, t_2=t_2)

    @staticmethod
    def extant(tree: Tree) -> List[TreeNode]:
        """
        Internal function returning a list of non-extinct leaves in a tree.
        :param tree: The tree whose nodes will be checked.
        :return: List of extant leaves.
        """
        return [leaf for leaf in tree.get_leaves() if leaf.extinct is False]

    def sort_nodes(self, tree: TreeNode):
        leaf_nodes = self.extant(tree)
        leaf_names = [leaf.name for leaf in leaf_nodes]
        sorted_names = sorted(leaf_names, key=len)
        return [tree.get_leaves_by_name(name)[0] for name in sorted_names]

    @staticmethod
    def add_node(clone, name):
        tree = Tree()
        tree.dist = 0.0
        tree.add_feature('extinct', False)
        tree.add_feature('own_mu', [])
        tree.add_feature('inherited_mu', [])
        tree.add_feature('time_mu', [])
        tree.add_feature('clone', clone)
        tree.name = name
        return tree

    def add_child_node(self, node):
        for _ in range(2):
            child_node = self.add_node(clone=node.clone, name=f'{node.name}{_}')
            self.add_mutations(node, child_node, own=True)
            self.add_mutations(node, child_node, own=False)
            node.add_child(child_node)

    def get_clone_nodes(self, tree: TreeNode, clone: int):
        nodes = [node for node in self.sort_nodes(tree) if node.clone == clone]
        len_nodes = len(nodes)
        return nodes, len_nodes

    def get_clone_data(self, clone, nodes):
        if clone == 1 and self.clone_1_exsists:
            return {'b': self.b_1, 'N': len(nodes), 'd': self.bd.d}
        if clone == 2 and self.clone_2_exsists:
            return {'b': self.b_2, 'N': len(nodes), 'd': self.bd.d}
        return None

    @staticmethod
    def add_mutations(node, child_node, own: bool):
        node_mutations = node.own_mu if own else node.inherited_mu
        if node_mutations:
            for mutation in node_mutations:
                child_node.inherited_mu.append(mutation)

    @staticmethod
    def select_node_to_next_event(clone, c_i, nodes_c0, nodes_c1, nodes_c2):
        if clone == 0:
            return nodes_c0[c_i - 1]
        elif clone == 1:
            return nodes_c1[c_i - 1]
        return nodes_c2[c_i - 1]

    def check_if_create_new_clone(self, node, event, t_1, t_2, mu_i):
        if self.create_clone_1 and self.bd.t >= t_1 and event == 2 and node.clone == 0 and len(node.name)>=3:
            logger.debug(f'=========================================================== clone 1 from {node.name} !!!!!!!!')
            logger.debug(f'=========================================================== mu id {mu_i} !!!!!!!!')

            node.clone = min(node.clone + 1, 2)
            self.mu_clone_1 = self.bd.t
            self.create_clone_1 = False
            self.clone_1_exsists = True

        if self.clone_1_exsists and self.create_clone_2 and self.bd.t >= t_2 and event == 2 and node.clone == 1 and len(node.name)>=3:
            logger.debug(f'=========================================================== clone 2 from {node.name} !!!!!!!!')
            logger.debug(f'=========================================================== mu id {mu_i} !!!!!!!!')

            node.clone = min(node.clone + 1, 2)
            self.mu_clone_2 = self.bd.t
            self.create_clone_2 = False
            self.clone_2_exsists = True

    def create_tree(self, T, t_1, t_2):
        # sourcery skip: remove-redundant-fstring, simplify-fstring-formatting
        random.seed(1)
        mu_i = 0  # mutations counter
        tree = self.add_node(clone=0, name='0')

        while True:
            print(f'Current simulation time: {self.bd.t}')
            print(f'Current population size: {self.bd.N}')
            print(f"clone 0: {self.N_0}, clone 1: {self.N_1}, clone 2: {self.N_2}")
            logger.debug(f'Current simulation time: {self.bd.t}')
            logger.debug(f'Current population size: {self.bd.N}')
            if self.bd.N == 0:  # population is extinct
                break

            leaf_nodes = self.extant(tree)

            # if self.bd.t > T:
            if self.bd.N >= 500:
                for leaf in leaf_nodes:
                    leaf.dist += (self.bd.t - self.bd.t_history[-1])
                break

            nodes_c2, self.N_2 = self.get_clone_nodes(tree, 2)
            nodes_c1, self.N_1 = self.get_clone_nodes(tree, 1)
            nodes_c0, self.N_0 = self.get_clone_nodes(tree, 0)

            self.clone_1_exsists = bool(nodes_c1)
            self.clone_2_exsists = bool(nodes_c2)

            clone_1 = self.get_clone_data(clone=1, nodes=nodes_c1)
            clone_2 = self.get_clone_data(clone=2, nodes=nodes_c2)

            t_i, event, c_i, clone = self.bd.next_event(clone_1=clone_1, clone_2=clone_2)  # draw next event
            logger.debug(f'=========================================================== event for clone: {clone}')

            node = self.select_node_to_next_event(clone=clone, c_i=c_i, nodes_c0=nodes_c0, nodes_c1=nodes_c1,
                                                  nodes_c2=nodes_c2)

            self.bd.t += t_i  # update current time

            for leaf in leaf_nodes:
                leaf.dist += t_i

            self.check_if_create_new_clone(node=node, event=event, t_1=t_1, t_2=t_2, mu_i=mu_i)

            if event == 0:
                self.bd.N += 1
                self.add_child_node(node)
            elif event == 1:
                self.bd.N -= 1
                node.name += ' x'
                node.extinct = True
            else:
                mu_i += 1
                # print(f'cell: {node.name}, mutation: {mu_i}')
                node.own_mu.append(mu_i)
                node.time_mu.append(t_i)

            self.bd.t_history.append(self.bd.t)  # record time of event
            self.bd.t_events.append(t_i)  # record time point of event (dt(i))
            self.bd.N_history.append(self.bd.N)  # record population size after event
            self.bd.c.append(c_i)
            self.bd.events.append(event)

        if self.bd.events.count(0) == 0:
            return None

        print(f"clone 0: {self.N_0}, clone 1: {self.N_1}, clone 2: {self.N_2}")
        return tree

    def write_tree(self, k_i, k):
        os.mkdir(f'{PATH}/N-{self.bd.N}')
        self.tree.write(features=['name', 'dist', 'own_mu', 'inherited_mu', 'clone'], format_root_node=True, format=1,
                        outfile=f'{PATH}/N-{self.bd.N}/N-{self.bd.N}-tree.txt')

    @staticmethod
    def get_leaves_path(leaves, paths, leaf_nodes):
        """
        get all the nodes up to the last one
        :return:
        """
        for leaf in leaves:
            if leaf.is_root():
                continue
            moving_node = leaf

            while not moving_node.is_root():
                paths[leaf.name].append(moving_node.name)
                leaf_nodes[leaf].append(moving_node)
                moving_node = moving_node.up

            paths[leaf.name].append(moving_node.name)
            leaf_nodes[leaf].append(moving_node)

        return paths, leaf_nodes

    def create_leave_paths(self):
        leaves = self.tree.get_leaves()
        paths = {x.name: [] for x in leaves}
        leaf_nodes = {x: [] for x in leaves}
        return self.get_leaves_path(leaves, paths, leaf_nodes)

    def get_all_nodes(self):
        leaf_paths, leaf_nodes = self.create_leave_paths()

        nodes_list = [
            list(map(lambda x: x, node_path)) for node_path in leaf_nodes.values()
        ]
        return list({item for sublist in nodes_list for item in sublist})

    def get_interim_nodes(self):
        all_nodes = self.get_all_nodes()
        leaves = self.tree.get_leaves()

        return [node for node in all_nodes if node not in leaves]

    def get_all_nodes_path(self):
        leaf_paths, leaf_nodes = self.create_leave_paths()
        interim_nodes = self.get_interim_nodes()

        for node in interim_nodes:
            leaf_nodes[node] = []
            leaf_paths[node.name] = []

        return self.get_leaves_path(interim_nodes, leaf_paths, leaf_nodes)

    def expected_mutations_number(self):
        nodes = self.get_all_nodes()
        return np.around(sum(node.dist for node in nodes) * self.bd.mu)

    def get_root_node(self):
        return self.tree.get_tree_root()
