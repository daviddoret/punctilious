import networkx as nx
import sample as pet

# import pygraphviz

t = pet.t1
u = pet.u


def graph_symbolic_object(g: nx.MultiDiGraph, o: pu.SymbolicObject):
    if pu.is_in_class(o, pu.classes.simple_objct):
        graph_simpl_objct(g, o)
    elif pu.is_in_class(o, pu.classes.theory_elaboration):
        graph_theory(g, o)
    elif pu.is_in_class(o, pu.classes.relation):
        graph_relation(g, o)
    elif pu.is_in_class(o, pu.classes.free_variable):
        graph_free_variable(g, o)
    elif pu.is_in_class(o, pu.classes.formula):
        graph_formula(g, o)
    elif pu.is_in_class(o, pu.classes.formula_statement):
        graph_formula_statement(g, o)


def graph_theory(g: nx.MultiDiGraph, t: pu.TheoryElaborationSequence):
    g.add_node(t.rep_name())
    for s in t.statements:
        graph_symbolic_object(g, s)


def graph_formula_statement(g: nx.MultiDiGraph, s: pu.TheoryElaborationSequence):
    g.add_node(t.rep_name())
    graph_symbolic_object(g, s.valid_proposition)
    g.add_edge(s.valid_proposition.rep_name(), t.rep_name())


def graph_free_variable(g: nx.MultiDiGraph, x: pu.FreeVariable):
    g.add_node(x.rep_name())


def graph_simple_objct(g: nx.MultiDiGraph, o: pu.Formula):
    g.add_node(o.rep_name())


def graph_relation(g: nx.MultiDiGraph, r: pu.Relation):
    g.add_node(r.rep_name())


def graph_formula(g: nx.MultiDiGraph, f: pu.Formula):
    g.add_node(f.rep_name())
    if f.relation.arity == 1:
        graph_symbolic_object(g, f.relation)
        g.add_edge(f.relation.rep_name(), f.rep_name())
        graph_symbolic_object(g, f.parameters[0])
        g.add_edge(f.parameters[0].rep_name(), f.rep_name())
    if f.relation.arity == 2:
        graph_symbolic_object(g, f.relation)
        g.add_edge(f.relation.rep_name(), f.rep_name())
        graph_symbolic_object(g, f.parameters[0])
        g.add_edge(f.parameters[0].rep_name(), f.rep_name())
        graph_symbolic_object(g, f.parameters[1])
        g.add_edge(f.parameters[1].rep_name(), f.rep_name())


g = nx.Graph()
graph_theory(g, t)
# subax1 = plt.subplot(121)
# nx.draw(g, with_labels=True, font_weight='bold')
# plt.show()
pg = nx.nx_pydot.to_pydot(g)
output_graphviz_svg = pg.create_svg()
# a = nx.nx_agraph.to_agraph(g)
# a.draw("file.png")
"""
    def add_to_graph(self, g):
        " ""Add this theoretical object as a node in the target graph g.
        Recursively add directly linked objects unless they are already present in g.
        NetworkX automatically and quietly ignores nodes and edges that are already present." ""
        super().add_to_graph(g=g, )
        g.add_node(self.repr_as_symbol())
"""
