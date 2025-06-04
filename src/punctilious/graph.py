from __future__ import annotations
import typing
import collections
import util


def is_all_distinct_elements(t: tuple) -> bool:
    """Returns `True` if all elements of tuple `t` are distinct elements."""
    return len(set(map(id, t))) == len(t)


def data_validate_edge(o: FlexibleEdge) -> Edge:
    if isinstance(o, Edge):
        return o
    if isinstance(o, collections.abc.Iterable):
        o: tuple = tuple(o)
        if len(o) == 2:
            return Edge(o[0], o[1])
    raise util.PunctiliousException('Edge data validation failure', o=o)


def data_validate_edge_collection(o: FlexibleEdgeFiniteOrderedSet) -> EdgeFiniteOrderedSet:
    if isinstance(o, EdgeFiniteOrderedSet):
        return o
    if isinstance(o, collections.abc.Iterable):
        return EdgeFiniteOrderedSet(*o)
    if isinstance(o, collections.abc.Generator):
        return EdgeFiniteOrderedSet(*o)
    if o is None:
        return EdgeFiniteOrderedSet()
    raise util.PunctiliousException('EdgeFiniteOrderedSet data validation failure', o=o)


def data_validate_vertex(o: FlexibleVertex) -> Vertex:
    if isinstance(o, Vertex):
        return o
    raise util.PunctiliousException('Vertex data validation failure', o=o)


def data_validate_vertex_collection(o: FlexibleVertexFiniteOrderedSet) -> VertexFiniteOrderedSet:
    if isinstance(o, VertexFiniteOrderedSet):
        return o
    if isinstance(o, collections.abc.Iterable):
        return VertexFiniteOrderedSet(*o)
    if isinstance(o, collections.abc.Generator):
        return VertexFiniteOrderedSet(*o)
    if o is None:
        return VertexFiniteOrderedSet()
    raise util.PunctiliousException('VertexFiniteOrderedSet data validation failure', o=o)


def data_validate_graph(o: FlexibleGraph) -> Graph:
    if isinstance(o, Graph):
        return o
    if isinstance(o, collections.abc.Iterable):
        o: tuple = tuple(o)
        if len(o) == 2:
            return Graph(o[0], o[1])
    raise util.PunctiliousException('Digraph data validation failure', o=o)


class EdgeFiniteOrderedSet(tuple):
    """A finite (computable) ordered set of digraph edges."""

    def __init__(self, *elements: FlexibleEdgeFiniteOrderedSet):
        super(EdgeFiniteOrderedSet, self).__init__()

    def __new__(cls, *elements: FlexibleEdgeFiniteOrderedSet):
        if isinstance(elements, collections.abc.Generator):
            elements: tuple[FlexibleEdge, ...] = tuple(elements)
        elements: tuple[Edge, ...] = tuple(data_validate_edge(element) for element in elements)
        if not is_all_distinct_elements(elements):
            raise util.PunctiliousException(
                'EdgeFiniteOrderedSet data validation failure, not all elements are distinct',
                elements=elements)
        return super(EdgeFiniteOrderedSet, cls).__new__(cls, elements)


class VertexFiniteOrderedSet(tuple):
    """A finite (computable) ordered set of digraph vertices."""

    def __init__(self, *elements: FlexibleVertexFiniteOrderedSet):
        super(VertexFiniteOrderedSet, self).__init__()

    def __new__(cls, *elements: FlexibleVertexFiniteOrderedSet):
        if isinstance(elements, collections.abc.Generator):
            elements: tuple[FlexibleVertex, ...] = tuple(elements)
        elements: tuple[Vertex, ...] = tuple(data_validate_vertex(element) for element in elements)
        if not is_all_distinct_elements(elements):
            raise util.PunctiliousException(
                'VertexFiniteOrderedSet data validation failure, not all elements are distinct',
                elements=elements)
        return super(VertexFiniteOrderedSet, cls).__new__(cls, elements)


class Vertex:
    """A digraph vertex."""

    def __init__(self):
        self._graph: None = None
        self._neighbours: None = None

    @property
    def graph(self) -> Graph | None:
        """The graph of the vertex. `None` if this vertex is not linked to a graph.

        :return:
        """
        return self._graph

    @graph.setter
    def graph(self, graph: Graph):
        graph = data_validate_graph(graph)
        if self.graph is None:
            self._graph = graph
        else:
            raise util.PunctiliousException('Vertex is already linked to a graph.', current_graph=self.graph,
                                            new_graph=graph)

    @property
    def neighbours(self) -> VertexFiniteOrderedSet:
        """

        This is a lazy property, i.e. it is only computed the first time it is accessed.

        :return:
        """
        if self._neighbours is None:
            # lazy computation of the property value.
            neighbours: set[Vertex] = set()
            if self.graph is None:
                raise util.PunctiliousException('Vertex is not linked to a graph.', current_graph=self.graph)
            for e in self.graph.edges:
                if self is e.endpoint_u:
                    neighbours.add(e.endpoint_v)
                if self is e.endpoint_v:
                    neighbours.add(e.endpoint_u)
            self._neighbours = VertexFiniteOrderedSet(*neighbours)
        return self._neighbours


class Edge(tuple):
    """A digraph edge."""

    def __init__(self, u: FlexibleVertex, v: FlexibleVertex):
        super(Edge, self).__init__()
        self._graph: None = None

    def __new__(cls, u: FlexibleVertex, v: FlexibleVertex):
        u = data_validate_vertex(u)
        v = data_validate_vertex(v)
        return super(Edge, cls).__new__(cls, (u, v,))

    @property
    def endpoint_u(self) -> Edge:
        return self[0]

    @property
    def endpoint_v(self) -> Edge:
        return self[1]

    @property
    def graph(self) -> Graph | None:
        """The graph of the edge. `None` if this edge is not linked to a graph.

        :return:
        """
        return self._graph

    @graph.setter
    def graph(self, graph: Graph):
        graph = data_validate_graph(graph)
        if self.graph is None:
            self._graph = graph
        else:
            raise util.PunctiliousException('Edge is already linked to a graph.', current_graph=self.graph,
                                            new_graph=graph)


class Graph(tuple):
    """A finite (computable) digraph."""

    def __init__(self, v: FlexibleVertexFiniteOrderedSet, e: FlexibleEdgeFiniteOrderedSet):
        super(Graph, self).__init__()
        for vertex in v:
            vertex.graph = self
        for edge in e:
            edge.graph = self
        self._is_connected: None = None

    def __new__(cls, v: FlexibleVertexFiniteOrderedSet, e: FlexibleEdgeFiniteOrderedSet):
        v = data_validate_vertex_collection(v)
        e = data_validate_vertex_collection(e)
        return super(Graph, cls).__new__(cls, (v, e,))

    @property
    def edges(self) -> EdgeFiniteOrderedSet:
        return self[1]

    @property
    def is_connected(self) -> bool:
        """

        If the graph is an empty graph, it is considered not connected.

        :return:
        """
        if self._is_connected is None:
            # Lazy computation of the property value.
            if self.is_empty:
                self._is_connected = False
            else:
                visited: set[Vertex] = set()

                def depth_first_search(v: Vertex) -> None:
                    visited.add(v)
                    for neighbour in v.neighbours:
                        if neighbour not in visited:
                            depth_first_search(neighbour)

                depth_first_search(self.vertices[0])
                self._is_connected = len(visited) == self.order
        return self._is_connected

    @property
    def is_empty(self) -> bool:
        """A graph is empty if it contains no vertices."""
        return self.order == 0

    @property
    def order(self) -> int:
        """The `order` of a graph is the total number of vertices it contains."""
        return len(self.vertices)

    @property
    def size(self) -> int:
        """The `size` of a graph is the total number of edges it contains."""
        return len(self.edges)

    @property
    def vertices(self) -> VertexFiniteOrderedSet:
        return self[0]


FlexibleEdge = typing.Union[Edge]
FlexibleEdgeFiniteOrderedSet = typing.Union[
    EdgeFiniteOrderedSet, tuple[FlexibleEdge, ...], collections.abc.Generator[FlexibleEdge], None]
FlexibleVertex = typing.Union[Vertex]
FlexibleVertexFiniteOrderedSet = typing.Union[
    VertexFiniteOrderedSet, tuple[FlexibleVertex, ...], collections.abc.Generator[FlexibleVertex], None]
FlexibleGraph = typing.Union[
    Graph, tuple[FlexibleVertexFiniteOrderedSet, FlexibleEdgeFiniteOrderedSet]]
