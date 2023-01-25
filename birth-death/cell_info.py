class Cells:
    def __init__(self, bd, tree) -> None:
        self.bd_process = bd
        self.tree = tree
        self.about = {x.name: {} for x in self.tree.get_all_nodes()}

    def add_cells_path(self):
        paths, nodes = self.tree.get_all_nodes_path()
        for key, value in paths.items():
            self.about[key].update({'path': value})

    @staticmethod
    def get_cell_birth_time(node):
        return 0.0 if node.is_root() else node.up.dist

    @staticmethod
    def get_cell_death_time(node, birth_time):
        return birth_time + node.dist

    def add_cells_birth_death_time(self):
        nodes = self.tree.get_all_nodes()

        for node in nodes:
            birth_time = self.get_cell_birth_time(node)
            self.about[node.name].update({'birth_time': birth_time})
            self.about[node.name].update({'death_time': self.get_cell_death_time(node, birth_time)})

    # TODO: add mutations to each cell
    def add_mutations(self):
        for key in self.about.keys():
            self.about[key].update({'mutations': list()})
