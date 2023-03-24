"""
http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#trees
https://github.com/tresoldi/ngesh/blob/866b90003019a34eb297a543e22d2aea8ddffc31/src/ngesh/random_tree.py#L26
"""
import random
from typing import List

import numpy as np
from ete3 import Tree, TreeNode


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

    def create_tree(self, T, t_1, t_2):
        random.seed(1)

        mu_i = 0  # mutations counter

        tree = Tree()

        tree.dist = 0.0
        tree.add_feature('extinct', False)
        tree.add_feature('own_mu', [])
        tree.add_feature('inherited_mu', [])
        tree.add_feature('time_mu', [])
        tree.add_feature('clone', 0)
        tree.name = f'{0}'

        while True:
            print(f'Current simulation time: {self.bd.t}')
            print(f'Current population size: {self.bd.N}')
            if self.bd.N == 0:  # population is extinct
                break

            if self.bd.t > T:
                leaf_nodes = self.extant(tree)
                for leaf in leaf_nodes:
                    leaf.dist += (T - self.bd.t_history[-1])
                break

            nodes_c2 = [node for node in self.sort_nodes(tree) if node.clone == 2]
            nodes_c1 = [node for node in self.sort_nodes(tree) if node.clone == 1]
            nodes_c0 = [node for node in self.sort_nodes(tree) if node.clone == 0]

            self.N_0 = len(nodes_c0)
            self.N_1 = len(nodes_c1)
            self.N_2 = len(nodes_c2)

            if not nodes_c1:
                self.clone_1_exsists = False
            if not nodes_c2:
                self.clone_2_exsists = False

            if self.clone_1_exsists:
                clone_1 = {'b': self.b_1, 'N': len(nodes_c1), 'd': self.bd.d, 't': t_clone_1}
                # clone_2 = None
            else:
                clone_1 = None

            if self.clone_2_exsists:
                clone_2 = {'b': self.b_2, 'N': len(nodes_c2), 'd': self.bd.d, 't': t_clone_2}
            else:
                clone_2 = None

            t_i, event, c_i, clone = self.bd.next_event(clone_1=clone_1, clone_2=clone_2)  # draw next event

            if clone == 0:
                node = nodes_c0[c_i - 1]
            elif clone == 1:
                node = nodes_c1[c_i - 1]
            elif clone == 2:
                node = nodes_c2[c_i - 1]

            self.bd.t += t_i  # update current time

            leaf_nodes = self.extant(tree)

            for leaf in leaf_nodes:
                leaf.dist += t_i

            if self.create_clone_1 and self.bd.t >= t_1 and event == 2 and node.clone == 0:
                if len(node.name) > 2:

                    print(f'=========================================================== clone 1 from {node.name} !!!!!!!!')
                    node.clone = min(node.clone + 1, 2)
                    clone_1_name = node.name
                    t_clone_1 = self.bd.t - node.dist
                    self.mu_clone_1 = self.bd.t
                    print(f'=========================================================== t clone 1 {t_clone_1} !!!!!!!!')
                    self.create_clone_1 = False
                    self.clone_1_exsists = True

            if self.clone_1_exsists and self.create_clone_2 and self.bd.t >= t_2 and event == 2 and node.clone == 1 and node.name != clone_1_name:
                print(f'=========================================================== clone 2 from {node.name} !!!!!!!!')
                node.clone = min(node.clone + 1, 2)
                clone_2_name = node.name
                t_clone_2 = self.bd.t - node.dist
                self.mu_clone_2 = self.bd.t
                print(f'=========================================================== t clone 2 {t_clone_2} !!!!!!!!')
                self.create_clone_2 = False
                self.clone_2_exsists = True

            print(f'=========================================================== event for clone: {clone}')
            print(f'=========================================================== event for node clone: {node.clone}')
            if event == 0:
                self.bd.N += 1

                for _ in range(2):
                    child_node = Tree()
                    child_node.dist = 0.0
                    child_node.add_feature('extinct', False)
                    child_node.add_feature('own_mu', [])
                    child_node.add_feature('inherited_mu', [])
                    child_node.add_feature('time_mu', [])
                    child_node.add_feature('clone', node.clone)
                    child_node.name = f'{node.name}{_}'

                    if node.inherited_mu:
                        for mutation in node.inherited_mu:
                            child_node.inherited_mu.append(mutation)
                            # child_node.time_mu.append(t_i)

                    if node.own_mu:
                        for mutation in node.own_mu:
                            child_node.inherited_mu.append(mutation)

                    node.add_child(child_node)

            elif event == 1:
                self.bd.N -= 1
                node.name += ' x'
                node.extinct = True
            else:
                mu_i += 1
                print(f'cell: {node.name}, mutation: {mu_i}')
                node.own_mu.append(mu_i)
                node.time_mu.append(t_i)

            self.bd.t_history.append(self.bd.t)  # record time of event
            self.bd.t_events.append(t_i)  # record time point of event (dt(i))
            self.bd.N_history.append(self.bd.N)  # record population size after event
            self.bd.c.append(c_i)
            self.bd.events.append(event)

        if not self.bd.events.count(0):
            return None
        print(f"clone 0: {self.N_0}, clone 1: {self.N_1}, clone 2: {self.N_2}")
        return tree

    def write_tree(self, k_i, k):
        self.tree.write(features=['name', 'dist', 'own_mu', 'inherited_mu', 'clone'], format_root_node=True, format=1,
                        outfile=f'results/{k}x/trees/{k_i}-N-{self.bd.N}.txt')

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
