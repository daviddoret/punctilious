from __future__ import annotations

import abc
import collections
import collections.abc


class Representation:
    def __init__(self, renderers: tuple[Renderer, ...]):
        self._renderers: tuple[Renderer, ...] = renderers

    def optimize_renderer(self, prefs: TagsPreferences):
        """Given preferences, return the optimal renderer.

        :param prefs:
        :return:
        """
        best_score = 0
        optimal_renderer = self.renderers[0]
        for current_renderer in self.renderers:
            current_score = prefs.score_tags(tags=current_renderer.tags)
            if current_score > best_score:
                optimal_renderer = current_renderer
                best_score = current_score
        return optimal_renderer

    @property
    def renderers(self):
        """A tuple of renderers configured for this representation."""
        return self._renderers

    def rep(self, *args, prefs: TagsPreferences, **kwargs):
        renderer: Renderer = self.optimize_renderer(prefs=prefs)
        return renderer.rep()


class Renderer(abc.ABC):
    """A renderer is an object that has the capability to generate the output of a presentation."""

    def __init__(self, tags: TagsAssignment | collections.abc.Iterable):
        """

        :param tags: The tags for which this renderer is optimal.
        """
        if not isinstance(tags, TagsAssignment):
            tags: TagsAssignment = TagsAssignment(*tags)
        self._tags: TagsAssignment = tags

    def rep(self, *args, **kwargs):
        raise NotImplementedError('This method is abstract.')

    @property
    def tags(self):
        return self._tags


class RendererForStringConstant(Renderer):
    """A renderer that generates a string from a constant."""

    def __init__(self, string_constant: str, tags: TagsAssignment | collections.abc.Iterable):
        super().__init__(tags)
        self._string_constant = string_constant

    @property
    def string_constant(self):
        return self._string_constant

    def rep(self, *args, **kwargs):
        return self._string_constant


class RendererForStringTemplate(Renderer):
    """A renderer that generates a string from a template.

    """

    def __init__(self, string_template: str, tags: TagsAssignment | collections.abc.Iterable):
        super().__init__(tags)
        self._string_template = string_template

    def rep(self, *args, **kwargs):
        # TODO: Add variable substitution logic here.
        return self._string_template

    @property
    def string_template(self):
        return self._string_template


class TagLabel(str):
    """A tag label is a category used to organize labels in groups."""

    def __init__(self, label: str):
        super().__init__()

    def __new__(cls, label: str):
        if not isinstance(label, str):
            # implicit conversion to assure proper equality between equal labels.
            label: str = str(label)
        return super().__new__(cls, label)


class TagValue(str):
    """A tag value is a tag used to denote tags in a tag category."""

    def __init__(self, value: str):
        super().__init__()

    def __new__(cls, value: str):
        if not isinstance(value, TagValue):
            value: str = str(value)
        return super().__new__(cls, value)


class Tag(tuple):
    """A tag is pair which comprises a label and a value."""

    def __init__(self, label: TagLabel | str, value: TagValue | str):
        super().__init__()

    def __new__(cls, label: TagLabel | str, value: TagValue | str):
        if not isinstance(label, TagLabel):
            label: TagLabel = TagLabel(label)
        if not isinstance(value, TagValue):
            value: TagValue = TagValue(value)
        return super().__new__(cls, [label, value])

    @property
    def label(self):
        return self[0]

    @property
    def value(self):
        return self[1]


class TagsAssignment(tuple):
    """A canonically sorted tuple of tags whose labels are unique."""

    def __init__(self, *tags: tuple[Tag, ...]):
        super().__init__()

    def __new__(cls, *tags: tuple[Tag, ...]):
        # validate that every label is unique
        labels = tuple(sub[0] for sub in tags)
        unique_labels = tuple(set(labels))
        if not len(labels) == len(unique_labels):
            raise ValueError('some labels are not unique')
        # sort the tuple
        tags_sorted = tuple(sorted(tags, key=lambda tag: tag.label))
        return super().__new__(cls, tags_sorted)

    def labels(self) -> collections.abc.Iterable:
        return (tag.label for tag in self)

    def values(self) -> collections.abc.Iterable:
        return (tag.value for tag in self)


class TagsPreferences(dict):
    """User preferences for tags.

    """

    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        self._validate_key_value(key, value)
        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        for key, value in dict(*args, **kwargs).items():
            self._validate_key_value(key, value)
        super().update(*args, **kwargs)

    def _validate_key_value(self, key, value):
        if not isinstance(key, Tag):
            raise TypeError(f"Key must be of type Tag, got {type(key).__name__} instead.")
        if not isinstance(value, int):
            raise TypeError(f"Value must be of type int, got {type(value).__name__} instead.")

    def score_tags(self, tags: TagsAssignment | collections.abc.Iterable):
        """Returns the preference score of a collection of tags.

        :param tags:
        :return:
        """
        if not isinstance(tags, TagsAssignment):
            tags: TagsAssignment = TagsAssignment(*tags)
        return sum(self.get(tag, 0) for tag in tags)
