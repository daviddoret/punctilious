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


def data_validate_edge_ordered_set(o: FlexibleEdgeFiniteOrderedSet) -> EdgeOrderedSet:
    if isinstance(o, EdgeOrderedSet):
        return o
    if isinstance(o, collections.abc.Iterable):
        return EdgeOrderedSet(*o)
    if isinstance(o, collections.abc.Generator):
        return EdgeOrderedSet(*o)
    if o is None:
        return EdgeOrderedSet()
    raise util.PunctiliousException('EdgeFiniteOrderedSet data validation failure', o=o)


def data_validate_vertex(o: FlexibleVertex) -> Vertex:
    if isinstance(o, Vertex):
        return o
    raise util.PunctiliousException('Vertex data validation failure', o=o)


def data_validate_vertex_ordered_set(o: FlexibleVertexOrderedSet) -> VertexOrderedSet:
    if isinstance(o, VertexOrderedSet):
        return o
    if isinstance(o, collections.abc.Iterable):
        return VertexOrderedSet(*o)
    if isinstance(o, collections.abc.Generator):
        return VertexOrderedSet(*o)
    if o is None:
        return VertexOrderedSet()
    raise util.PunctiliousException('VertexFiniteOrderedSet data validation failure', o=o)


def data_validate_digraph(o: FlexibleRootedPlaneTree) -> RootedPlaneTree:
    if isinstance(o, RootedPlaneTree):
        return o
    if isinstance(o, collections.abc.Iterable):
        o: tuple = tuple(o)
        if len(o) == 2:
            return RootedPlaneTree(o[0], o[1])
    raise util.PunctiliousException('RootedPlaneTree data validation failure', o=o)


class EdgeOrderedSet(tuple):
    """A finite (computable) ordered set of digraph edges."""

    def __init__(self, *elements: FlexibleEdgeFiniteOrderedSet):
        super(EdgeOrderedSet, self).__init__()

    def __new__(cls, *elements: FlexibleEdgeFiniteOrderedSet):
        if isinstance(elements, collections.abc.Generator):
            elements: tuple[FlexibleEdge, ...] = tuple(elements)
        elements: tuple[Edge, ...] = tuple(data_validate_edge(element) for element in elements)
        if not is_all_distinct_elements(elements):
            raise util.PunctiliousException(
                'EdgeFiniteOrderedSet data validation failure, not all elements are distinct',
                elements=elements)
        return super(EdgeOrderedSet, cls).__new__(cls, elements)


class VertexOrderedSet(tuple):
    """A finite (computable) ordered set of digraph vertices."""

    def __init__(self, *elements: FlexibleVertexOrderedSet):
        super(VertexOrderedSet, self).__init__()

    def __new__(cls, *elements: FlexibleVertexOrderedSet):
        if isinstance(elements, collections.abc.Generator):
            elements: tuple[FlexibleVertex, ...] = tuple(elements)
        elements: tuple[Vertex, ...] = tuple(data_validate_vertex(element) for element in elements)
        if not is_all_distinct_elements(elements):
            raise util.PunctiliousException(
                'VertexFiniteOrderedSet data validation failure, not all elements are distinct',
                elements=elements)
        return super(VertexOrderedSet, cls).__new__(cls, elements)


class Vertex:
    """A digraph vertex."""

    def __init__(self, composite_rooted_plane_tree: FlexibleRootedPlaneTree):
        self._composite_rooted_plane_tree = composite_rooted_plane_tree

    @property
    def composite_rooted_plane_tree(self) -> FlexibleRootedPlaneTree:
        return self._composite_rooted_plane_tree

    @property
    def vertices(self) -> EdgeOrderedSet:
        pass
        # return self.edges


class Edge(tuple):
    """A digraph edge."""

    def __init__(self, rooted_plane_tree: FlexibleRootedPlaneTree, u: FlexibleVertex, v: FlexibleVertex):
        self._rooted_plane_tree = rooted_plane_tree
        super(Edge, self).__init__()

    def __new__(cls, rooted_plane_tree: FlexibleRootedPlaneTree, u: FlexibleVertex, v: FlexibleVertex):
        u = data_validate_vertex(u)
        v = data_validate_vertex(v)
        return super(Edge, cls).__new__(cls, (u, v,))

    @property
    def rooted_plane_tree(self) -> FlexibleRootedPlaneTree:
        return self._rooted_plane_tree

    @property
    def head(self) -> Vertex:
        return self[1]

    @property
    def tail(self) -> Vertex:
        return self[0]


def compose_rooted_plane_tree(*rooted_plane_tree) -> RootedPlaneTree:
    """Given a collection S of RPTs, compose a new RPT such that its level 1 vertices are those RPTs.

    :param rooted_plane_tree:
    :return:
    """


class RootedPlaneTree(tuple):
    """A model of immutable finite (computable) rooted plane tree.
    """

    def __init__(self, v, e):
        super(RootedPlaneTree, self).__init__()

    def __new__(cls, v, e):
        if from_iterable_structure is not None:
            children_vertices = (Vertex)
            for source_child in from_iterable_structure:
                vertex = Vertex(composite_rooted_plane_tree)
            root = Vertex(children_vertices=children_vertices)

        v = data_validate_vertex_ordered_set(v)
        e = data_validate_vertex_ordered_set(e)
        return super(RootedPlaneTree, cls).__new__(cls, (v, e,))

    @property
    def edges(self) -> EdgeOrderedSet:
        return self[1]

    def to_vertex(self) -> Vertex:
        """Convert this RPT to a vertex, which can then be used for the composition of new RPTs.
        """
        pass

    @property
    def vertices(self) -> VertexOrderedSet:
        return self[0]


FlexibleEdge = typing.Union[Edge]
FlexibleEdgeFiniteOrderedSet = typing.Union[
    EdgeOrderedSet, tuple[FlexibleEdge, ...], collections.abc.Generator[FlexibleEdge], None]
FlexibleVertex = typing.Union[Vertex]
FlexibleVertexOrderedSet = typing.Union[
    VertexOrderedSet, tuple[FlexibleVertex, ...], collections.abc.Generator[FlexibleVertex], None]
FlexibleRootedPlaneTree = typing.Union[
    RootedPlaneTree, tuple[FlexibleVertexOrderedSet, FlexibleEdgeFiniteOrderedSet]]
