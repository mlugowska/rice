"""
http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#trees
https://github.com/tresoldi/ngesh/blob/866b90003019a34eb297a543e22d2aea8ddffc31/src/ngesh/random_tree.py#L26
"""
from typing import List

import numpy as np
import pandas as pd
from ete3 import Tree, TreeNode


class BDTree:
    def __init__(self, bd, T):
        self.tree = self.create_tree(bd, T)

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

    def _create_tree(self, T: float, t_history: List[float], N_history: List[float], events: List[int],
                     event_times: List[float], cells: List[int]) -> TreeNode:

        # add last timestep til end of simulation run
        # (no event happend in this time, but we need to extend node length because
        # cell where still alive in this time til next event will happen after simulation time)
        event_times.append(T - t_history[-1])

        # Create the tree root as a node. Given that the root is at first set as
        # non-extinct and with a branch length of 0.0, it will be immediately
        # subject to either a speciation or extinction event.
        tree = Tree()
        tree.dist = event_times[0]
        tree.add_feature('extinct', False)
        tree.name = f'{0}'

        for idx in range(len(events)):

            if N_history[idx] == 0:
                break

            # Get node based on cell index
            node = self.sort_nodes(tree)[cells[idx] - 1]

            if events[idx] == 0:
                # The event will be a birth with two children.
                for _ in range(2):
                    child_node = Tree()
                    child_node.add_feature('extinct', False)
                    child_node.dist = 0
                    child_node.extinct = False
                    child_node.name = f'{node.name}{_}'
                    node.add_child(child_node)

            elif events[idx] == 1:
                node.name += ' x'
                node.extinct = True

            leaf_nodes = self.extant(tree)

            # Extend the branch length of all extant leaves by the event_time
            for leaf in leaf_nodes:
                new_leaf_dist = leaf.dist + event_times[idx + 1]
                leaf.dist = min(new_leaf_dist, (T or new_leaf_dist))

        return tree

    def create_tree(self, bd, T: float):
        return self._create_tree(T, t_history=bd.t_history, N_history=bd.N_history, cells=bd.c,
                                 events=bd.events, event_times=bd.t_events)

    def write_tree(self, bd, k_i):
        self.tree.write(features=['name', 'dist'], format_root_node=True,
                        outfile=f'/Users/magdalena/PycharmProjects/rice/birth-death/{k_i + 1}-N-{bd.N}.txt')

    def get_leaves_path(self, leaves, paths, leaf_nodes):
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
        print(f'leaf nodes paths: {leaf_paths}')

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





    # def get_birth_death_times(self):
    #     paths, nodes = self.get_leaves_path()
    #     print(paths)
    #
    #     nodes_list = []
    #     for node_path in nodes.values():
    #         nodes_list.append(list(map(lambda x: x, node_path)))
    #
    #     flat_list = [item for sublist in nodes_list for item in sublist]
    #     unique = sorted(list(set(flat_list)), key=lambda x: x.name, reverse=False)
    #
    #     bd_times = {x.name: dict() for x in unique}
    #
    #     for node in unique:
    #         dict_row = bd_times.get(node.name)
    #         dict_row['birth'] = 0.0 if node.is_root() else node.up.dist
    #         dict_row['death'] = dict_row['birth'] + node.dist
    #
    #     df = pd.DataFrame(bd_times).transpose()
    #     df['is_alive'] = np.where(df.index.str.contains('x') == False, True, False)
    #     return df
