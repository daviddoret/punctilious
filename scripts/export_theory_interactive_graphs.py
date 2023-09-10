# import networkx as nx
# import matplotlib.pyplot as plt
# import pygraphviz
# import pydot


t1 = theory.package.tao_2006_2_1_the_peano_axioms.Tao2006ThePeanoAxioms().develop()
pu.configuration.encoding = pu.encodings.plaintext
pu.configuration.echo_default = False

# g = nx.Graph()
# graph_symbolic_object(g, t)

# g = pyvis.network.Network(directed=True)
output_path = 'build/tao_2006_2_1_the_peano_axioms_interactive_graph_plaintext.html'
t1.export_interactive_graph(encoding=pu.encodings.plaintext, output_path=output_path)
output_path = 'build/tao_2006_2_1_the_peano_axioms_interactive_graph_unicode.html'
t1.export_interactive_graph(encoding=pu.encodings.unicode,
    output_path=output_path)  # g.show('../build/tao_2006_the_peano_axioms_interactive_graph_statement_dependencies.html',notebook=False)  # subax1 = plt.subplot(121)  # nx.draw(g, with_labels=True, font_weight='bold')  # plt.show()

# pg = nx.nx_pydot.to_pydot(g)
# output_graphviz_svg = pg.create_svg()

# a = nx.nx_agraph.to_agraph(g)
# a.draw("file.png")
