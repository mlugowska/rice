import numpy as np
import pandas as pd


class Cells:
    def __init__(self, bd, tree) -> None:
        self.bd_process = bd
        self.tree = tree
        self.about = {x.name: {} for x in self.tree.get_all_nodes()}

    def add_cells_path(self):
        paths, nodes = self.tree.get_all_nodes_path()
        for key, value in paths.items():
            self.about[key].update({'path': value})

    def get_cell_birth_time(self, node):
        if node.is_root():
            return 0.0
        paths, nodes = self.tree.get_all_nodes_path()

        node_path = nodes.get(node)[1:]
        return sum(ancestor.dist for ancestor in node_path)

    @staticmethod
    def get_cell_death_time(node, birth_time):
        return birth_time + node.dist

    def add_cells_birth_death_time(self):
        nodes = self.tree.get_all_nodes()

        for node in nodes:
            birth_time = self.get_cell_birth_time(node)
            self.about[node.name].update({'birth_time': birth_time})
            self.about[node.name].update({'death_time': self.get_cell_death_time(node, birth_time)})

    def add_mutations(self):
        nodes = self.tree.get_all_nodes()

        for node in nodes:
            self.about[node.name].update({'mutations': node.mutations})

    def check_cell_is_alive(self, df):
        leaves = self.tree.extant(self.tree.tree)
        leaf_names = [leaf.name for leaf in leaves]
        return df.assign(is_alive=[True if cell_index in leaf_names else False for cell_index in df.index])

    def create_dataframe(self):
        df = pd.DataFrame(self.about).transpose()
        df['birth_time'] = df['birth_time'].astype(np.float64)
        df['death_time'] = df['death_time'].astype(np.float64)
        return self.check_cell_is_alive(df)
