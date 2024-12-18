from __future__ import annotations
# other packages
import abc
import collections
import collections.abc
import yaml
import jinja2
# punctilious packages
import _util
import _identifiers


def ensure_tag(o) -> Tag:
    """Ensure that `o` is of type Tag, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Tag):
        return o
    elif isinstance(o, tuple) and len(o) == 2:
        label: str = o[0]
        value: str = o[1]
        o = Tag(label=label, value=value)
        return o
    else:
        raise TypeError(f'Tag validation failure. Type: {type(o)}. Object: {o}.')


def ensure_tags_assignment(o) -> TagsAssignment:
    """Ensure that `o` is of type TagsAssignment, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, TagsAssignment):
        return o
    elif isinstance(o, dict):
        tags = tuple(ensure_tag(i) for i in o.items())
        o = TagsAssignment(*tags)
        return o
    else:
        raise TypeError(f'TagsAssignment validation failure. Type: {type(o)}. Object: {o}.')


def ensure_tags_preferences(o) -> TagsPreferences:
    """Ensure that `o` is of type TagsPreferences, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, TagsPreferences):
        return o
    elif isinstance(o, dict):
        o_typed = TagsPreferences()
        for i in o.items():
            tag = ensure_tag(i[0])
            value = i[1]  # TODO: define a TagPreferenceValue class and apply validation
            o_typed[tag] = value
        return o_typed
    elif o is None:
        return TagsPreferences()
    else:
        raise TypeError(f'TagsPreferences validation failure. Type: {type(o)}. Object: {o}.')


def ensure_renderer(o) -> Renderer:
    """Ensure that `o` is of type Renderer, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Renderer):
        return o
    elif isinstance(o, dict):
        # conversion from dict structure.
        implementation: str = o.get('implementation', '')
        if implementation == 'string_constant':
            string_constant: str = o.get('string_constant', '')
            tags: TagsAssignment = ensure_tags_assignment(o.get('tags', []))
            o = RendererForStringConstant(string_constant=string_constant, tags=tags)
            return o
        elif implementation == 'string_template':
            string_template: str = o.get('string_template', '')
            tags: TagsAssignment = ensure_tags_assignment(o.get('tags', {}))
            o = RendererForStringTemplate(string_template=string_template, tags=tags)
            return o
    else:
        raise TypeError(f'Representation validation failure. Type: {type(o)}. Object: {o}.')


def ensure_renderers(o) -> Renderers:
    """Ensure that `o` is of type Renderers, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Renderers):
        return o
    elif isinstance(o, collections.abc.Iterable):
        renderers = tuple(ensure_renderer(i) for i in o)
        o = Renderers(*renderers)
        return o
    else:
        raise TypeError(f'Renderers validation failure. Type: {type(o)}. Object: {o}.')


def ensure_representation(o) -> Representation:
    """Ensure that `o` is of type Representation, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Representation):
        return o
    elif isinstance(o, dict):
        # conversion from dict structure.
        uid = o['uid']
        uid = _identifiers.ensure_unique_identifier(uid)
        syntactic_rules = None
        renderers = ensure_renderers(o=o.get('renderers', []))
        o = Representation(uid=uid, syntactic_rules=syntactic_rules, renderers=renderers)
        return o
    else:
        raise TypeError(f'Representation validation failure. Type: {type(o)}. Object: {o}.')


def ensure_representations(o) -> Representations:
    """Ensure that `o` is of type Representations, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Representations):
        return o
    elif isinstance(o, collections.abc.Iterable):
        o = Representations(*o)
        return o
    else:
        raise TypeError(f'Representations validation failure. Type: {type(o)}. Object: {o}.')


class Representation(_identifiers.UniqueIdentifiable):

    def __init__(self, uid: _identifiers.FlexibleUniqueIdentifier,
                 renderers: tuple[Renderer, ...],
                 syntactic_rules=None):
        self._syntactic_rules = syntactic_rules
        self._renderers: tuple[Renderer, ...] = renderers
        super().__init__(uid=uid)

    def __repr__(self):
        return f'{self.uid.slug} ({self.uid.uuid}) representation'

    def __str__(self):
        return f'{self.uid.slug} representation'

    def optimize_renderer(self, config: TagsPreferences = None):
        """Given preferences, return the optimal renderer.

        :param config:
        :return:
        """
        if config == None:
            config = TagsPreferences()
        best_score = 0
        optimal_renderer = self.renderers[0]
        for current_renderer in self.renderers:
            current_score = config.score_tags(tags=current_renderer.tags)
            if current_score > best_score:
                optimal_renderer = current_renderer
                best_score = current_score
        return optimal_renderer

    @property
    def renderers(self):
        """A tuple of renderers configured for this representation."""
        return self._renderers

    def rep(self, variables: dict[str, str] = None, config: TagsPreferences = None):
        config = ensure_tags_preferences(config)
        if variables is None:
            # TODO: Use a RepresentationVariable class and apply proper validation
            variables = {}
        renderer: Renderer = self.optimize_renderer(config=config)
        return renderer.rep(config=config, variables=variables)

    @property
    def syntactic_rules(self):
        return self._syntactic_rules

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Representations(tuple):
    """A tuple of Representation instances."""

    def __init__(self, *args):
        self._index = tuple(i.uid for i in self)
        super().__init__()

    def __new__(cls, *args):
        typed_representations = tuple(ensure_representation(r) for r in args)
        return super().__new__(cls, typed_representations)

    def __repr__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def get_from_identifier(self, identifier: _identifiers.FlexibleUniqueIdentifier):
        identifier: _identifiers.UniqueIdentifier = _identifiers.ensure_identifier(identifier)
        if identifier in self._index:
            identifier_index = self._index.index(identifier)
            return self[identifier_index]
        else:
            raise IndexError(f'Representation identifier not found: "{identifier}".')

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Renderer(abc.ABC):
    """A renderer is an object that has the capability to generate the output of a presentation."""

    def __init__(self, tags: TagsAssignment | collections.abc.Iterable | None = None):
        """

        :param tags: The tags for which this renderer is optimal.
        """
        if tags is None:
            tags = TagsAssignment()
        if not isinstance(tags, TagsAssignment):
            tags: TagsAssignment = TagsAssignment(*tags)
        self._tags: TagsAssignment = tags

    def __repr__(self):
        raise NotImplementedError('This method is abstract.')

    def __str__(self):
        raise NotImplementedError('This method is abstract.')

    @abc.abstractmethod
    def rep(self, config: TagsPreferences | None = None, variables=None):
        raise NotImplementedError('This method is abstract.')

    @property
    def tags(self):
        return self._tags


class RendererForStringConstant(Renderer):
    """A renderer that generates a string from a constant."""

    def __init__(self, string_constant: str, tags: TagsAssignment | collections.abc.Iterable | None = None):
        super().__init__(tags)
        self._string_constant = string_constant

    def __repr__(self):
        return f'"{self._string_constant}" string constant.'

    def __str__(self):
        return f'"{self._string_constant}" string constant.'

    @property
    def string_constant(self):
        return self._string_constant

    def rep(self, config: TagsPreferences | None = None, variables=None):
        """Represent the string constant.

        For RendererForStringConstant, parameters have no effect.

        :param config: this parameter has no effect.
        :param variables: this parameter has no effect.
        :return: the string representation of the string constant.
        """
        return self._string_constant


class RendererForStringTemplate(Renderer):
    """A renderer that generates a string from a template.

    """

    def __init__(self, string_template: str, tags: TagsAssignment | collections.abc.Iterable | None = None):
        super().__init__(tags)
        self._string_template = string_template
        self._jinja2_template: jinja2.Template = jinja2.Template(string_template)

    def __repr__(self):
        return f'"{self._string_template}" string template.'

    def __str__(self):
        return f'"{self._string_template}" string template.'

    def rep(self, config: TagsPreferences = None, variables: dict[str, str] | None = None):
        """

        :param config:
        :param variables: Variables are passed to the jinja2 template.
        :return:
        """
        # TODO: Implement a custom dict class which implements __missing__ to have a default
        #  value for missing keys.
        if variables is None:
            variables = {}
        # Alternative approach with str.format_map(). Pros: lightweight + performance.
        # return self._string_template.format_map(variables)
        # Approach with jinja2 template. Pros: expressiveness + escaping + security.
        return self._jinja2_template.render(variables)

    @property
    def string_template(self):
        return self._string_template


class Renderers(tuple):
    """A tuple of Renderer instances."""

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __new__(cls, *args, **kwargs):
        renderers = tuple(ensure_renderer(i) for i in args)
        return super().__new__(cls, renderers)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


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


# Common labels and values.
symbol = Tag('connector_presentation', 'symbol', )
en = Tag('language', 'en', )
fr = Tag('language', 'fr', )
unicode_basic = Tag('technical_language', 'unicode_basic', )
unicode_extended = Tag('technical_language', 'unicode_extended', )
latex_math = Tag('technical_language', 'latex_math', )
parenthesized = Tag('parenthesization', 'parenthesized', )
