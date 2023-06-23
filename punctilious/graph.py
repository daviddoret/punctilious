
import punctilious as pu
import networkx as nx
import sample.pet_theory_1 as pet

t = pet.t1


def graph(target: pu.TheoryElaborationSequence):
        


"""
    def add_to_graph(self, g):
        " ""Add this theoretical object as a node in the target graph g.
        Recursively add directly linked objects unless they are already present in g.
        NetworkX automatically and quietly ignores nodes and edges that are already present." ""
        super().add_to_graph(g=g, )
        g.add_node(self.repr_as_symbol())
  