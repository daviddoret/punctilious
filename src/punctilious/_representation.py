from __future__ import annotations
# other packages
import abc
import collections
import collections.abc
import yaml
import jinja2
import typing

from click import option

# punctilious packages
import punctilious._util as _util
import punctilious._identifiers as _identifiers


def ensure_option(o) -> Option:
    """Ensure that `o` is of type Option, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Option):
        return o
    elif isinstance(o, tuple) and len(o) == 2:
        label: str = o[0]
        value: str = o[1]
        o = Option(label=label, value=value)
        return o
    else:
        raise TypeError(f'Option validation failure. Type: {type(o)}. Object: {o}.')


def ensure_options_assignment(o) -> OptionsAssignment:
    """Ensure that `o` is of type OptionsAssignment, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, OptionsAssignment):
        return o
    elif isinstance(o, dict):
        options = tuple(ensure_option(i) for i in o.items())
        o = OptionsAssignment(*options)
        return o
    else:
        raise TypeError(f'OptionsAssignment validation failure. Type: {type(o)}. Object: {o}.')


def ensure_options_preferences(o) -> OptionsPreferences:
    """Ensure that `o` is of type OptionsPreferences, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, OptionsPreferences):
        return o
    elif isinstance(o, dict):
        o_typed = OptionsPreferences()
        for i in o.items():
            option = ensure_option(i[0])
            value = i[1]  # TODO: define a OptionPreferenceValue class and apply validation
            o_typed[option] = value
        return o_typed
    elif o is None:
        return OptionsPreferences()
    else:
        raise TypeError(f'OptionsPreferences validation failure. Type: {type(o)}. Object: {o}.')


def ensure_renderer(o) -> Renderer:
    """Ensure that `o` is of type Renderer, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Renderer):
        return o
    elif isinstance(o, dict):
        # conversion from dict structure.
        implementation: str = o.get('implementation', '')
        if implementation == 'string_constant':
            string_constant: str = o.get('string_constant', '')
            options: OptionsAssignment = ensure_options_assignment(o.get('options', []))
            o = RendererForStringConstant(string_constant=string_constant, options=options)
            return o
        elif implementation == 'string_template':
            string_template: str = o.get('string_template', '')
            options: OptionsAssignment = ensure_options_assignment(o.get('options', {}))
            o = RendererForStringTemplate(string_template=string_template, options=options)
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


def ensure_abstract_representation(o) -> AbstractRepresentation:
    """Ensure that `o` is of type AbstractRepresentation, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, AbstractRepresentation):
        return o
    elif isinstance(o, dict):
        # conversion from dict structure.
        uid = o['uid']
        uid = _identifiers.ensure_unique_identifier(uid)
        renderers = ensure_renderers(o=o.get('renderers', []))
        o = AbstractRepresentation(uid=uid, renderers=renderers)
        return o
    else:
        raise TypeError(f'Representation validation failure. Type: {type(o)}. Object: {o}.')


def ensure_abstract_representations(o) -> AbstractRepresentations:
    """Ensure that `o` is of type Representations, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, AbstractRepresentations):
        return o
    elif isinstance(o, collections.abc.Iterable):
        o = AbstractRepresentations(*o)
        return o
    else:
        raise TypeError(f'Representations validation failure. Type: {type(o)}. Object: {o}.')


class AbstractRepresentation(_identifiers.UniqueIdentifiable):
    """An AbstractRepresentation is an object that, given the expected input parameters,
    has the capability to generate ConcreteRepresentations.
    """

    def __init__(self, uid: _identifiers.FlexibleUniqueIdentifier,
                 renderers: tuple[Renderer, ...]):
        self._renderers: tuple[Renderer, ...] = renderers
        super().__init__(uid=uid)

    def __repr__(self):
        return f'{self.uid.slug} ({self.uid.uuid}) representation builder'

    def __str__(self):
        return f'{self.uid.slug} representation builder'

    def optimize_renderer(self, config: OptionsPreferences = None):
        """Given preferences, return the optimal renderer.

        :param config:
        :return:
        """
        if config is None:
            config = OptionsPreferences()
        best_score = 0
        optimal_renderer = self.renderers[0]
        for current_renderer in self.renderers:
            current_score = config.score_options(options=current_renderer.options)
            if current_score > best_score:
                optimal_renderer = current_renderer
                best_score = current_score
        return optimal_renderer

    @property
    def renderers(self):
        """A tuple of renderers configured for this representation.

        This is a mutable property, renderers can be reloaded.
        """
        return self._renderers

    @renderers.setter
    def renderers(self, renderers: FlexibleRenderers):
        renderers = ensure_renderers(renderers)
        self._renderers = renderers

    def rep(self, variables: dict[str, str] = None, config: OptionsPreferences = None):
        config = ensure_options_preferences(config)
        if variables is None:
            # TODO: Use a RepresentationVariable class and apply proper validation
            variables = {}
        renderer: Renderer = self.optimize_renderer(config=config)
        return renderer.rep(config=config, variables=variables)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


def load_abstract_representation(o: typing.Mapping,
                                 append_representation_renderers: bool = False) -> AbstractRepresentation:
    """Receives a raw Representation, typically from a YAML file, and returns a typed Representation instance.

    :param append_representation_renderers: if the representation is already loaded in memory,
        append new renderers to it.
    :param o: a raw Representation.
    :return: a typed Representation instance.
    """
    representation: AbstractRepresentation | None = _identifiers.load_unique_identifiable(o)
    if representation is None:
        # The representation does not exist in memory.
        representation = ensure_abstract_representation(o)
    else:
        # The representation exists in memory.
        if append_representation_renderers:
            # Overwrite the mutable properties.
            if 'renderers' in o.keys():
                new_renderers = ensure_renderers(o['renderers'])
                _util.get_logger().debug('new_renderers: {new_renderers}')
                merged_renderers = set(representation.renderers + new_renderers)
                merged_renderers = Renderers(*merged_renderers)
                representation.renderers = merged_renderers
    return representation


class AbstractRepresentations(tuple[AbstractRepresentation, ...]):
    """A tuple of AbstractRepresentation instances."""

    def __getitem__(self, key) -> AbstractRepresentation:
        if isinstance(key, int):
            # Default behavior for integer keys
            return super().__getitem__(key)
        if isinstance(key, _identifiers.FlexibleUUID):
            # Custom behavior for uuid keys
            item: AbstractRepresentation | None = self.get_from_uuid(uuid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        if isinstance(key, _identifiers.FlexibleUniqueIdentifier):
            # Custom behavior for UniqueIdentifier keys
            item: AbstractRepresentation | None = self.get_from_uid(uid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        else:
            raise TypeError(f'Unsupported key type: {type(key).__name__}')

    def __init__(self, *args):
        self._index = tuple(i.uid for i in self)
        super().__init__()

    def __new__(cls, *args):
        typed_representations = tuple(ensure_abstract_representation(r) for r in args)
        return super().__new__(cls, typed_representations)

    def __repr__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def get_from_uid(self, uid: _identifiers.FlexibleUniqueIdentifier,
                     raise_error_if_not_found: bool = False) -> AbstractRepresentation | None:
        """Return a representation by its UniqueIdentifier.

        :param uid: a UniqueIdentifier.
        :param raise_error_if_not_found:
        :return:
        """
        uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(uid)
        item: AbstractRepresentation | None = next((item for item in self if item.uid == uid), None)
        if item is None and raise_error_if_not_found:
            raise IndexError(f'Representation not found. UID: "{uid}".')
        else:
            return item

    def get_from_uuid(self, uuid: _identifiers.FlexibleUUID,
                      raise_error_if_not_found: bool = False) -> AbstractRepresentation | None:
        """Return a representation by its UUID.

        :param uuid: a UUID.
        :param raise_error_if_not_found:
        :return:
        """
        uuid: _identifiers.uuid_pkg.UUID = _identifiers.ensure_uuid(uuid)
        if uuid in self._index:
            identifier_index = self._index.index(uuid)
            return self[identifier_index]
        elif raise_error_if_not_found:
            raise IndexError(f'Representation not found. UUID: "{uuid}".')
        else:
            return None

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


def load_abstract_representations(o: typing.Iterable | None,
                                  append_representation_renderers: bool = False) -> AbstractRepresentations:
    """Receives a raw Representations collection, typically from a YAML file,
    and returns a typed Representations instance.

    :param append_representation_renderers: if representations are already loaded in memory,
        append new renderers to the existing representations.
    :param o: a raw Representations collection.
    :return: a typed Representations instance.
    """
    if o is None:
        o = []
    representations: list[AbstractRepresentation] = []
    for i in o:
        representation: AbstractRepresentation = load_abstract_representation(
            i, append_representation_renderers=append_representation_renderers)
        representations.append(representation)
    return AbstractRepresentations(*representations)


class Renderer(abc.ABC):
    """A renderer is an object that has the capability to generate the output of a presentation."""

    def __init__(self, options: OptionsAssignment | collections.abc.Iterable | None = None):
        """

        :param options: The options for which this renderer is optimal.
        """
        if options is None:
            options = OptionsAssignment()
        if not isinstance(options, OptionsAssignment):
            options: OptionsAssignment = OptionsAssignment(*options)
        self._options: OptionsAssignment = options

    def __repr__(self):
        raise NotImplementedError('This method is abstract.')

    def __str__(self):
        raise NotImplementedError('This method is abstract.')

    @abc.abstractmethod
    def rep(self, config: OptionsPreferences | None = None, variables=None):
        raise NotImplementedError('This method is abstract.')

    @property
    def options(self):
        return self._options


class RendererForStringConstant(Renderer):
    """A renderer that generates a string from a constant."""

    def __init__(self, string_constant: str, options: OptionsAssignment | collections.abc.Iterable | None = None):
        super().__init__(options)
        self._string_constant = string_constant

    def __repr__(self):
        return f'"{self._string_constant}" string constant.'

    def __str__(self):
        return f'"{self._string_constant}" string constant.'

    @property
    def string_constant(self):
        return self._string_constant

    def rep(self, config: OptionsPreferences | None = None, variables=None):
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

    def __init__(self, string_template: str, options: OptionsAssignment | collections.abc.Iterable | None = None):
        super().__init__(options)
        self._string_template = string_template
        self._jinja2_template: jinja2.Template = jinja2.Template(string_template)

    def __repr__(self):
        return f'"{self._string_template}" string template.'

    def __str__(self):
        return f'"{self._string_template}" string template.'

    def rep(self, config: OptionsPreferences = None, variables: dict[str, str] | None = None):
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


FlexibleRenderer = typing.Union[Renderer, collections.abc.Mapping, collections.abc.Iterable]
FlexibleRenderers = typing.Union[Renderers, collections.abc.Iterable]


class OptionLabel(str):
    """A option label is a category used to organize labels in groups."""

    def __init__(self, label: str):
        super().__init__()

    def __new__(cls, label: str):
        if not isinstance(label, str):
            # implicit conversion to assure proper equality between equal labels.
            label: str = str(label)
        return super().__new__(cls, label)


class OptionValue(str):
    """A option value is a option used to denote options in a option category."""

    def __init__(self, value: str):
        super().__init__()

    def __new__(cls, value: str):
        if not isinstance(value, OptionValue):
            value: str = str(value)
        return super().__new__(cls, value)


class Option(tuple):
    """A option is pair which comprises a label and a value."""

    def __init__(self, label: OptionLabel | str, value: OptionValue | str):
        super().__init__()

    def __new__(cls, label: OptionLabel | str, value: OptionValue | str):
        if not isinstance(label, OptionLabel):
            label: OptionLabel = OptionLabel(label)
        if not isinstance(value, OptionValue):
            value: OptionValue = OptionValue(value)
        return super().__new__(cls, [label, value])

    @property
    def label(self):
        return self[0]

    @property
    def value(self):
        return self[1]


class OptionsAssignment(tuple):
    """A canonically sorted tuple of options whose labels are unique."""

    def __init__(self, *options: tuple[Option, ...]):
        super().__init__()

    def __new__(cls, *options: tuple[Option, ...]):
        # validate that every label is unique
        labels = tuple(sub[0] for sub in options)
        unique_labels = tuple(set(labels))
        if not len(labels) == len(unique_labels):
            raise ValueError('some labels are not unique')
        # sort the tuple
        options_sorted = tuple(sorted(options, key=lambda option: option.label))
        return super().__new__(cls, options_sorted)

    def labels(self) -> collections.abc.Iterable:
        return (option.label for option in self)

    def values(self) -> collections.abc.Iterable:
        return (option.value for option in self)


class OptionsPreferences(dict):
    """User preferences for options.

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
        if not isinstance(key, Option):
            raise TypeError(f"Key must be of type Option, got {type(key).__name__} instead.")
        if not isinstance(value, int):
            raise TypeError(f"Value must be of type int, got {type(value).__name__} instead.")

    def score_options(self, options: OptionsAssignment | collections.abc.Iterable):
        """Returns the preference score of a collection of options.

        :param options:
        :return:
        """
        if not isinstance(options, OptionsAssignment):
            options: OptionsAssignment = OptionsAssignment(*options)
        return sum(self.get(option, 0) for option in options)


# Common labels and values.
symbol = Option('connector_presentation', 'symbol', )
en = Option('language', 'en', )
fr = Option('language', 'fr', )
unicode_basic = Option('technical_language', 'unicode_basic', )
unicode_extended = Option('technical_language', 'unicode_extended', )
latex_math = Option('technical_language', 'latex_math', )
parenthesized = Option('parenthesization', 'parenthesized', )
