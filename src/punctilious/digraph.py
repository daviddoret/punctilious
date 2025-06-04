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


def data_validate_digraph(o: FlexibleDigraph) -> Digraph:
    if isinstance(o, Digraph):
        return o
    if isinstance(o, collections.abc.Iterable):
        o: tuple = tuple(o)
        if len(o) == 2:
            return Digraph(o[0], o[1])
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
        pass


class Edge(set):
    """A digraph edge."""

    def __init__(self, u: FlexibleVertex, v: FlexibleVertex):
        super(Edge, self).__init__()

    def __new__(cls, u: FlexibleVertex, v: FlexibleVertex):
        u = data_validate_vertex(u)
        v = data_validate_vertex(v)
        return super(Edge, cls).__new__(cls, (u, v,))

    @property
    def head(self) -> Vertex:
        return self[1]

    @property
    def tail(self) -> Vertex:
        return self[0]


class Digraph(tuple):
    """A finite (computable) digraph."""

    def __init__(self, v: FlexibleVertexFiniteOrderedSet, e: FlexibleEdgeFiniteOrderedSet):
        super(Digraph, self).__init__()

    def __new__(cls, v: FlexibleVertexFiniteOrderedSet, e: FlexibleEdgeFiniteOrderedSet):
        v = data_validate_vertex_collection(v)
        e = data_validate_vertex_collection(e)
        return super(Digraph, cls).__new__(cls, (v, e,))

    @property
    def edges(self) -> EdgeFiniteOrderedSet:
        return self[1]

    @property
    def vertices(self) -> VertexFiniteOrderedSet:
        return self[0]


FlexibleEdge = typing.Union[Edge]
FlexibleEdgeFiniteOrderedSet = typing.Union[
    EdgeFiniteOrderedSet, tuple[FlexibleEdge, ...], collections.abc.Generator[FlexibleEdge], None]
FlexibleVertex = typing.Union[Vertex]
FlexibleVertexFiniteOrderedSet = typing.Union[
    VertexFiniteOrderedSet, tuple[FlexibleVertex, ...], collections.abc.Generator[FlexibleVertex], None]
FlexibleDigraph = typing.Union[
    Digraph, tuple[FlexibleVertexFiniteOrderedSet, FlexibleEdgeFiniteOrderedSet]]
