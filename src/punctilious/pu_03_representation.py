# special features
from __future__ import annotations

# external modules
import abc
import collections
import collections.abc
import yaml
import jinja2
import typing

# punctilious modules
import punctilious.pu_01_utilities as _utl
import punctilious.pu_02_identifiers as _ids


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
        raise _utl.PunctiliousError(f'Option validation failure.', o=o)


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


def ensure_options_preferences(o) -> Preferences:
    """Ensure that `o` is of type OptionsPreferences, converting it if necessary, or raise an error if it fails."""
    if isinstance(o, Preferences):
        return o
    elif isinstance(o, dict):
        o_typed = Preferences()
        for i in o.items():
            option = ensure_option(i[0])
            value = i[1]  # TODO: define a OptionPreferenceValue class and apply validation
            o_typed[option] = value
        return o_typed
    elif o is None:
        return Preferences()
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
        uid = _ids.ensure_unique_identifier(uid)
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


class AbstractRepresentation(_ids.UniqueIdentifiable):
    """An AbstractRepresentation is an object that, given the expected input parameters,
    has the capability to generate ConcreteRepresentations.
    """

    def __init__(self, uid: _ids.FlexibleUniqueIdentifier,
                 renderers: tuple[Renderer, ...] | tuple[()] | None):
        if renderers is None:
            renderers = tuple()
        self._renderers: tuple[Renderer, ...] = renderers
        super().__init__(uid=uid)
        _utl.get_logger().debug(f'AbstractRepresentation: `{repr(self)}`')

    def __repr__(self):
        return f'{self.uid.slug} ({self.uid.uuid})'

    def __str__(self):
        return f'{self.uid.slug}'

    def optimize_renderer(self, prefs: Preferences = None):
        """Given some preferences, return the optimal renderer.

        :param prefs:
        :return:
        """
        if prefs is None:
            prefs = Preferences()
        best_score = 0
        optimal_renderer = self.renderers[0]
        for current_renderer in self.renderers:
            value, forbidden = prefs.score_options(options=current_renderer.options)
            if forbidden == 0 and value > best_score:
                optimal_renderer = current_renderer
                best_score = value
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

    def rep(self, variables: dict[str, str] = None, prefs: Preferences = None):
        prefs = ensure_options_preferences(prefs)
        if variables is None:
            # TODO: Use a RepresentationVariable class and apply proper validation
            variables = {}
        renderer: Renderer = self.optimize_renderer(prefs=prefs)
        return renderer.rep(prefs=prefs, variables=variables)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class AbstractRepresentations(tuple[AbstractRepresentation, ...]):
    """A tuple of AbstractRepresentation instances."""

    def __getitem__(self, key) -> AbstractRepresentation:
        if isinstance(key, int):
            # Default behavior for integer keys
            return super().__getitem__(key)
        if isinstance(key, _ids.FlexibleUUID):
            # Custom behavior for uuid keys
            item: AbstractRepresentation | None = self.get_from_uuid(uuid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        if isinstance(key, _ids.FlexibleUniqueIdentifier):
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

    def get_from_uid(self, uid: _ids.FlexibleUniqueIdentifier,
                     raise_error_if_not_found: bool = False) -> AbstractRepresentation | None:
        """Return a representation by its UniqueIdentifier.

        :param uid: a UniqueIdentifier.
        :param raise_error_if_not_found:
        :return:
        """
        uid: _ids.UniqueIdentifier = _ids.ensure_unique_identifier(uid)
        item: AbstractRepresentation | None = next((item for item in self if item.uid == uid), None)
        if item is None and raise_error_if_not_found:
            raise IndexError(f'Representation not found. UID: "{uid}".')
        else:
            return item

    def get_from_uuid(self, uuid: _ids.FlexibleUUID,
                      raise_error_if_not_found: bool = False) -> AbstractRepresentation | None:
        """Return a representation by its UUID.

        :param uuid: a UUID.
        :param raise_error_if_not_found:
        :return:
        """
        uuid: _ids.uuid_pkg.UUID = _ids.ensure_uuid(uuid)
        if uuid in self._index:
            identifier_index = self._index.index(uuid)
            return self[identifier_index]
        elif raise_error_if_not_found:
            raise IndexError(f'Representation not found. UUID: "{uuid}".')
        else:
            return None

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


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
    def rep(self, config: Preferences | None = None, variables=None, prefs=None):
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

    def rep(self, config: Preferences | None = None, variables=None, prefs=None):
        """Represent the string constant.

        For RendererForStringConstant, parameters have no effect.

        :param prefs:
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

    def rep(self, config: Preferences = None, variables: dict[str, str] | None = None, prefs=None):
        """

        :param prefs:
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
    """An option label is a category used to organize labels in groups."""

    def __init__(self, label: str):
        super().__init__()

    def __new__(cls, label: str):
        if not isinstance(label, str):
            # implicit conversion to assure proper equality between equal labels.
            label: str = str(label)
        return super().__new__(cls, label)


class OptionValue(str):
    """An option value is an option used to denote options in an option category."""

    def __init__(self, value: str):
        super().__init__()

    def __new__(cls, value: str):
        if not isinstance(value, OptionValue):
            value: str = str(value)
        return super().__new__(cls, value)


class Option(tuple):
    """An option is pair which comprises a label and a value."""

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


class BasePriority(tuple):
    """An abstract class to store option priorities."""

    def __new__(cls, o: collections.abc.Iterable):
        return super().__new__(cls, o)

    @property
    def is_forbidden(self) -> bool | None:
        return self[1]

    @property
    def value(self) -> int | None:
        return self[0]


class Preferences(dict[Option, BasePriority]):
    """A set of option preferences.

    """

    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        key = ensure_option(key)
        value = ensure_base_priority(value)
        super().__setitem__(key, value)

    def update(self, **kwargs):
        for key, value in dict(**kwargs).items():
            self[key] = value

    def score_options(self, options: OptionsAssignment | collections.abc.Iterable):
        """Returns the preference score of a collection of options.

        :param options:
        :return:
        """
        if not isinstance(options, OptionsAssignment):
            options: OptionsAssignment = OptionsAssignment(*options)

        value: int = sum(v.value for k, v in self.items() if isinstance(v, Priority) and k in options)
        forbidden: int = sum(1 for k, v in self.items() if isinstance(v, Forbidden) and k in options)

        return value, forbidden


_forbidden: Forbidden | None = None


# _mandatory: Mandatory | None = None


class Forbidden(BasePriority):
    """A class to store the forbidden option priority.

    This priority means that the option is unconditionally filtered out when looking for the best option."""

    def __new__(cls):
        global _forbidden
        if _forbidden is None:
            _forbidden = super().__new__(cls, (None, True,))
        return _forbidden

    def __repr__(self):
        return f'forbidden'

    def __str__(self):
        return f'forbidden'


def get_forbidden() -> Forbidden:
    return Forbidden()


class Priority(BasePriority):
    """A priority value for an option."""

    def __int__(self):
        return self.value

    def __new__(cls, value: int):
        instance = super().__new__(cls, (value, False,))
        return instance

    def __repr__(self):
        return f'priority #{self.value}'

    def __str__(self):
        return f'priority #{self.value}'


FlexiblePriority = typing.Union[Priority, int]
FlexibleForbidden = typing.Union[Forbidden, str]
FlexibleBasePriority = typing.Union[Priority, Forbidden]


def ensure_priority(o: FlexiblePriority) -> Priority:
    if isinstance(o, Priority):
        return o
    elif isinstance(o, int):
        return Priority(o)
    else:
        raise TypeError(f'Priority validation failure. Type: {type(o)}. Object: {o}.')


def ensure_forbidden(o: FlexibleForbidden) -> Forbidden:
    if isinstance(o, Forbidden):
        return o
    elif str(o) == 'forbidden':
        return get_forbidden()
    else:
        raise TypeError(f'Forbidden validation failure. Type: {type(o)}. Object: {o}.')


def ensure_base_priority(o: FlexibleBasePriority) -> BasePriority:
    if isinstance(o, Priority):
        return o
    elif isinstance(o, int):
        return Priority(o)
    elif isinstance(o, Forbidden):
        return o
    elif str(o) == 'forbidden':
        return get_forbidden()
    else:
        raise TypeError(f'BasePriority validation failure. Type: {type(o)}. Object: {o}.')


def load_abstract_representation(o: [typing.Mapping | str | uuid_pkg.UUID],
                                 raise_error_if_not_found: bool = True) -> AbstractRepresentation:
    """Load a UniqueIdentifiable of type AbstractRepresentation from the general UID index.

    :param o:
    :param raise_error_if_not_found:
    :return:
    """
    o: _ids.UniqueIdentifiable = _ids.load_unique_identifiable(o=o, raise_error_if_not_found=True)
    if not isinstance(o, AbstractRepresentation):
        raise TypeError(f'`o` ({o}) of type `{str(type(o))}` is not of type `AbstractRepresentation`.')
    o: AbstractRepresentation
    return o
