import pandas as pd


class Cells:
    def __init__(self, tree, bd) -> None:
        self.bd = bd
        self.tree = tree
        self.about = {x.name: {} for x in self.tree.get_all_nodes()}

    def add_cells_path(self):
        paths, nodes = self.tree.get_all_nodes_path()
        for key, value in paths.items():
            self.about[key].update({'path': value})

    def get_birthtime(self, node):
        if node.is_root():
            return 0.0
        paths, nodes = self.tree.get_all_nodes_path()

        node_path = nodes.get(node)[1:]
        return sum(ancestor.dist for ancestor in node_path)

    @staticmethod
    def get_deathtime(node, birthtime, T):
        time = birthtime + node.dist
        return time if time < T else 0.0

    @staticmethod
    def get_lifetime(birthtime, deathtime):
        return deathtime - birthtime if deathtime else 0.0

    def add_lifetimes(self, T):
        nodes = self.tree.get_all_nodes()

        for node in nodes:
            birthtime = self.get_birthtime(node)
            deathtime = self.get_deathtime(node, birthtime, T)
            self.about[node.name].update({'birthtime': birthtime})
            self.about[node.name].update({'deathtime': deathtime})
            self.about[node.name].update({'lifetime': self.get_lifetime(birthtime, deathtime)})

    def add_mutations(self):
        nodes = self.tree.get_all_nodes()

        for node in nodes:
            self.about[node.name].update({'own_mu': node.own_mu})
            self.about[node.name].update({'inherited_mu': node.inherited_mu})

    def add_clone(self):
        nodes = self.tree.get_all_nodes()

        for node in nodes:
            self.about[node.name].update({'clone': node.clone})

    def check_cell_is_alive(self, df):
        leaves = self.tree.extant(self.tree.tree)
        leaf_names = [leaf.name for leaf in leaves]
        return df.assign(
            is_alive=[cell_index in leaf_names for cell_index in df.index]
        )

    def create_dataframe(self):
        df = pd.DataFrame(self.about).transpose()
        return self.check_cell_is_alive(df)

    @staticmethod
    def get_mutations_number(leaves):
        mu_index = []
        for leaf in leaves:
            mu_index.extend(iter(leaf.inherited_mu))
            mu_index.extend(iter(leaf.own_mu))
        # if self.tree.get_root_node().own_mu:
        #     return list(set(mu_index).difference(self.tree.get_root_node().own_mu))

        return list(set(mu_index))

    def calculate_mutation_frequency(self):
        leaves = self.tree.extant(self.tree.tree)
        mu_index = self.get_mutations_number(leaves)

        df = pd.DataFrame(columns=['Number of cells', 'clone 0', 'clone 1', 'clone 2'], index=mu_index).fillna(0)

        for mu in mu_index:
            for leaf in leaves:
                if mu in leaf.inherited_mu or mu in leaf.own_mu:
                    df.at[mu, 'Number of cells'] += 1
                    df.at[mu, f'clone {leaf.clone}'] = True

        df = df.replace(0, False)
        return df

    @staticmethod
    def sfs(df):
        clone_0 = df.loc[df['clone 0'] == True].value_counts().sort_index()
        clone_1 = df.loc[df['clone 1'] == True].value_counts().sort_index()
        clone_2 = df.loc[df['clone 2'] == True].value_counts().sort_index()

        clone_0 = clone_0.reset_index(level=[1, 2, 3]).drop(columns=['clone 0', 'clone 1', 'clone 2'], axis=1)
        clone_1 = clone_1.reset_index(level=[1, 2, 3]).drop(columns=['clone 0', 'clone 1', 'clone 2'], axis=1)
        clone_2 = clone_2.reset_index(level=[1, 2, 3]).drop(columns=['clone 0', 'clone 1', 'clone 2'], axis=1)

        return clone_0, clone_1, clone_2

    def create_mutation_table(self):
        leaves = self.tree.extant(self.tree.tree)
        mu_index = self.get_mutations_number(leaves)

        df = pd.DataFrame(columns=mu_index, index=[leaf.name for leaf in leaves]).fillna(0)

        for index, row in df.iterrows():
            leaf = self.tree.tree.get_leaves_by_name(index)[0]
            for colname in df.columns:
                if colname in leaf.own_mu or colname in leaf.inherited_mu:
                    df.at[index, colname] = 1

        return df
