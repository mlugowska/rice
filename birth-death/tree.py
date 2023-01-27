"""
http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#trees
https://github.com/tresoldi/ngesh/blob/866b90003019a34eb297a543e22d2aea8ddffc31/src/ngesh/random_tree.py#L26
"""
import random
from typing import List

import numpy as np
from ete3 import Tree, TreeNode


class BDTree:
    def __init__(self, bd, T):
        self.bd = bd
        self.tree = self._create_tree(T)

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

    def _create_tree(self, T: float):
        # random.seed(1)

        mu_i = 0  # mutations counter

        tree = Tree()

        tree.dist = 0.0
        tree.add_feature('extinct', False)
        tree.add_feature('mutations', list())
        tree.name = f'{0}'

        while True:
            print(f'Current simulation time: {self.bd.t}')
            if self.bd.N == 0:  # population is extinct
                break

            t_i, event, c_i = self.bd.next_event()  # draw next even
            self.bd.t += t_i  # update current time

            if self.bd.t > T:
                leaf_nodes = self.extant(tree)
                for leaf in leaf_nodes:
                    leaf.dist += (T - self.bd.t_history[-1])
                break

            leaf_nodes = self.extant(tree)

            for leaf in leaf_nodes:
                leaf.dist += t_i

            node = self.sort_nodes(tree)[c_i - 1]

            if event == 0:
                self.bd.N += 1

                for _ in range(2):
                    child_node = Tree()
                    child_node.dist = 0.0
                    child_node.add_feature('extinct', False)
                    child_node.add_feature('mutations', list())
                    child_node.name = f'{node.name}{_}'

                    if node.mutations:
                        for mutation in node.mutations:
                            child_node.mutations.append(mutation)

                    node.add_child(child_node)

            elif event == 1:
                self.bd.N -= 1
                node.name += ' x'
                node.extinct = True
            else:
                mu_i += 1
                print(f'cell: {node.name}, mutation: {mu_i}')
                node.mutations.append(mu_i)

            self.bd.t_history.append(self.bd.t)  # record time of event
            self.bd.t_events.append(t_i)  # record time point of event (dt(i))
            self.bd.N_history.append(self.bd.N)  # record population size after event
            self.bd.c.append(c_i)
            self.bd.events.append(event)



            # for leaf in leaf_nodes:
            #     new_leaf_dist = leaf.dist + t_i
            #     leaf.dist = min(new_leaf_dist, (T or new_leaf_dist))


        return tree

    def write_tree(self, bd, k_i):
        self.tree.write(features=['name', 'dist'], format_root_node=True,
                        outfile=f'/Users/magdalena/PycharmProjects/rice/birth-death/{k_i + 1}-N-{bd.N}.txt')

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
        paths = {x.name: list() for x in leaves}
        leaf_nodes = {x: list() for x in leaves}
        return self.get_leaves_path(leaves, paths, leaf_nodes)

    def get_all_nodes(self):
        leaf_paths, leaf_nodes = self.create_leave_paths()

        nodes_list = []
        for node_path in leaf_nodes.values():
            nodes_list.append(list(map(lambda x: x, node_path)))
        return list(set([item for sublist in nodes_list for item in sublist]))

    def get_interim_nodes(self):
        all_nodes = self.get_all_nodes()
        leaves = self.tree.get_leaves()

        return [node for node in all_nodes if node not in leaves]

    def get_all_nodes_path(self):
        leaf_paths, leaf_nodes = self.create_leave_paths()
        interim_nodes = self.get_interim_nodes()

        for node in interim_nodes:
            leaf_nodes[node] = list()
            leaf_paths[node.name] = list()

        return self.get_leaves_path(interim_nodes, leaf_paths, leaf_nodes)

    def expected_mutations_number(self):
        nodes = self.get_all_nodes()
        return np.around(sum([node.dist for node in nodes]) * self.bd.mu)
