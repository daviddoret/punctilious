# import networkx as nx
# import matplotlib.pyplot as plt
# import pygraphviz
# import pydot
import pyvis
import textwrap
import punctilious as pu
import theories.tao_2006_the_peano_axioms as tao_2006

t = tao_2006.Tao2006ThePeanoAxioms().develop()
pu.configuration.encoding = pu.encodings.plaintext
pu.configuration.echo_default = False


class NewConf:
    def __init__(self):
        self.axiom_inclusion_args = {'shape': 'box', 'color': '#ddee00'}
        self.inferred_statement_args = {'shape': 'box', 'color': '#eedd00'}
        self.label_wrap_size = 16


new_conf = NewConf()


def export_pyvis_graph(pyvis_graph, o: pu.TheoreticalObject,
                       parent: (None, pu.TheoreticalObject) = None,
                       encoding: (None, pu.Encoding) = None,
                       label_wrap_size: (None, int) = None) -> None:
    pyvis_graph = pu.prioritize_value(pyvis_graph, pyvis.network.Network())
    label_wrap_size = pu.prioritize_value(label_wrap_size, new_conf.label_wrap_size)
    pyvis_graph: pyvis.network.Network
    node_id = o.rep_symbol(encoding=pu.encodings.plaintext)
    if node_id not in pyvis_graph.get_nodes():
        kwargs = None
        if pu.is_in_class(o, pu.classes.axiom_inclusion):
            o: pu.AxiomInclusion
            kwargs = new_conf.axiom_inclusion_args
            node_label = o.rep_symbol(encoding=encoding)
            pyvis_graph.add_node(node_id, label=node_label, **kwargs)
        elif pu.is_in_class(o, pu.classes.inferred_proposition):
            o: pu.InferredStatement
            kwargs = new_conf.inferred_statement_args
            ref = '' if o.ref is None else f'({o.rep_ref(encoding=encoding)}) '
            labelHighlightBold = True if ref != '' else False
            node_label = f'{o.rep_symbol(encoding=encoding)} {ref}: {o.rep_formula(encoding=encoding)}'
            if label_wrap_size is not None:
                node_label = '\n'.join(textwrap.wrap(text=node_label, width=label_wrap_size))
            pyvis_graph.add_node(node_id, label=node_label,
                                 labelHighlightBold=labelHighlightBold, **kwargs)
            for parameter in o.parameters:
                export_pyvis_graph(pyvis_graph=pyvis_graph, o=parameter, parent=o,
                                   encoding=encoding,
                                   label_wrap_size=label_wrap_size)
                parameter_node_id = parameter.rep_symbol(encoding=pu.encodings.plaintext)
                if parameter_node_id in pyvis_graph.get_nodes():
                    pyvis_graph.add_edge(source=node_id, to=parameter_node_id)
        else:
            node_label = o.rep_symbol(encoding=encoding)
            pyvis_graph.add_node(node_id, label=node_label)
    if parent is not None:
        parent: pu.TheoreticalObject
        parent_node_id = parent.rep_symbol(encoding=pu.encodings.plaintext)
        if parent_node_id not in pyvis_graph.get_nodes():
            if not pu.is_in_class(parent, pu.classes.theory_elaboration):
                pyvis_graph.add_edge(parent_node_id, node_id)
    if pu.is_in_class(o, pu.classes.theory_elaboration):
        o: pu.TheoryElaborationSequence
        for statement in o.statements:
            export_pyvis_graph(pyvis_graph=pyvis_graph, o=statement, parent=o, encoding=encoding,
                               label_wrap_size=label_wrap_size)


# g = nx.Graph()
# graph_symbolic_object(g, t)

g = pyvis.network.Network()
export_pyvis_graph(pyvis_graph=g, o=t, encoding=pu.encodings.unicode)
g.toggle_physics(True)
g.show_buttons(filter_=['physics'])
g.show('test.html', notebook=False)
# subax1 = plt.subplot(121)
# nx.draw(g, with_labels=True, font_weight='bold')
# plt.show()

# pg = nx.nx_pydot.to_pydot(g)
# output_graphviz_svg = pg.create_svg()

# a = nx.nx_agraph.to_agraph(g)
# a.draw("file.png")
