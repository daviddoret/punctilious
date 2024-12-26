"""

The meta-language module requires 1) formal-language and 2) interpretation.

"""

# special features
from __future__ import annotations

# external modules
import collections.abc
import typing
import yaml

# punctilious modules
import punctilious.identifiers as _identifiers
import punctilious.formal_language as _formal_language
import punctilious.interpretation as _interpretation
import punctilious.meta_operators_1 as _meta_operators_1


class Statement(_identifiers.UniqueIdentifiable):
    """
    TODO: A Statement should be both a proper object, e.g. when we load it from a YAML file,
        but also a formula, i.e. of the form `statement(variables(x(),y(),z()),premises(...),conclusion(...))`.
        This means that the meta operators must be pre-loaded.
    """

    def __init__(self, uid=None, variables=None, premises=None, conclusion=None, justifications=None):
        # Immutable properties
        self._variables = variables
        self._premises = premises
        self._conclusion = conclusion
        # Mutable properties
        self._justifications = justifications
        super().__init__(uid=uid)

    def __repr__(self):
        return f'{self.uid} statement'

    def __str__(self):
        return f'{self.uid.slug} statement'

    @property
    def conclusion(self):
        return self._conclusion

    @property
    def justifications(self):
        return self._justifications

    @property
    def premises(self):
        return self._premises

    @property
    def uid(self):
        return self._uid

    @property
    def variables(self):
        return self._variables

    def to_dict(self):
        d = {}
        if self.uid is not None:
            d['uid'] = self.uid
        if self.variables is not None:
            d['variables'] = self.variables
        if self.premises is not None:
            d['premises'] = self.premises
        if self.conclusion is not None:
            d['conclusion'] = self.conclusion
        if self.justifications is not None:
            d['justifications'] = self.justifications
        return d

    def to_yaml(self, default_flow_style):
        return yaml.dump(self.to_dict(), default_flow_style=default_flow_style)


def load_statement(o: typing.Mapping, overwrite_mutable_properties: bool = False) -> Statement:
    """Receives a raw Statement, typically from a YAML file, and returns a typed Statement instance.

    :param overwrite_mutable_properties: if `o` is already loaded in memory, overwrite its mutable properties:
        `connector_representation`, and `formula_representation`.
    :param o: a raw Connector.
    :return: a typed Connector instance.
    """
    statement: Statement | None = _identifiers.load_unique_identifiable(o)
    if statement is None:
        # The connector does not exist in memory.
        statement: Statement = ensure_statement(o)
    else:
        # The connector exists in memory.
        if overwrite_mutable_properties:
            pass
    return statement


def load_statements(o: typing.Iterable | None, overwrite_mutable_properties: bool = False) -> Statements:
    """Receives a raw Statements collection, typically from a YAML file,
    and returns a typed Statements instance.

    :param overwrite_mutable_properties: if statements are already loaded in memory, overwrite their mutable properties:
        `connector_representation`, and `formula_representation`.
    :param o: a raw Statements collection.
    :return: a typed Statements instance.
    """
    if o is None:
        o = []
    statements: list[Statement] = []
    for i in o:
        statement: Statement = load_statement(i, overwrite_mutable_properties=overwrite_mutable_properties)
        statements.append(statement)
    return Statements(*statements)


class Justifications(tuple):
    __slots__ = ()

    def __init__(self, *args):
        pass

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, args)

    def __repr__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.slug for e in self) + ')'

    @classmethod
    def instantiate_from_list(cls, l: list | None):
        if l is None:
            l = []
        typed_l = []
        for d in l:
            o = ensure_justification(o=d)
            typed_l.append(o)
        return _formal_language.Connectors(*typed_l)

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)


class Variable(_formal_language.Formula):
    """

    Global definition: formula of the form v().

    Local definition: a formula of the form v() with the following statement:
    is_variable(v()).
    """

    def __init__(self, c):
        """

        :param c: A connector.
        """
        super().__init__(c=c, a=None)


_conclusion_connector: _formal_language.Connector | None = None


def _get_conclusion_connector() -> _formal_language.Connector:
    """Return the `conclusion` meta-operator.
    """
    global _conclusion_connector
    if _conclusion_connector is None:
        _conclusion_connector = _identifiers.load_unique_identifiable(
            {'uid': {'slug': 'conclusion', 'uuid': '3dccc8f5-81cf-446a-9f3c-7673514f2117'},
             'syntactic_rules': {}}
        )
    return _conclusion_connector


_statement_connector: _formal_language.Connector | None = None


def _get_statement_connector() -> _formal_language.Connector:
    """Return the `statement` meta-operator.
    """
    global _statement_connector
    if _statement_connector is None:
        _statement_connector = _identifiers.load_unique_identifiable(
            {'uid': {'slug': 'statement', 'uuid': 'c138b200-111a-4a40-ac3c-c8afa8e615fb'},
             'syntactic_rules': {'fixed_arity': 3}}
        )
    return _statement_connector


_variables_connector: _formal_language.Connector | None = None


def _get_variables_connector() -> _formal_language.Connector:
    """Return the `variables` meta-operator.
    """
    global _variables_connector
    if _variables_connector is None:
        _variables_connector = _identifiers.load_unique_identifiable(
            {'uid': {'slug': 'variables', 'uuid': '0489e6f7-022e-48a4-82bf-dcb5907653b7'},
             'syntactic_rules': {'fixed_arity': 3}}
        )
    return _variables_connector


_premises_connector: _formal_language.Connector | None = None


def _get_premises_connector() -> _formal_language.Connector:
    """Return the `premises` meta-operator.
    """
    global _premises_connector
    if _premises_connector is None:
        _premises_connector = _identifiers.load_unique_identifiable(
            {'uid': {'slug': 'premises', 'uuid': 'b78ed901-37d2-4a97-a7a8-588b69dab20a'},
             'syntactic_rules': {}}
        )
    return _premises_connector


def ensure_statement(o) -> Statement:
    """Assure that `o` is of type Statement, converting as necessary, or raise an error."""
    if isinstance(o, Statement):
        return o
    elif isinstance(o, dict):
        uid = o['uid']
        variables = o.get('variables', None)
        premises = o.get('premises', None)
        conclusion = o.get('conclusion', None)
        justifications = None
        o = Statement(uid=uid, variables=variables, premises=premises, conclusion=conclusion,
                      justifications=justifications)
        return o
    else:
        raise TypeError('Statement assurance failure.')


def ensure_statements(o=None) -> Statements:
    if isinstance(o, Statements):
        return o
    elif isinstance(o, collections.abc.Iterable):
        return Statements(*o)
    elif o is None:
        return Statements()
    else:
        raise ValueError(f'o cannot be constrained into Statements: {o}. {type(o)}')


class Statements(tuple):
    """A tuple of Statement instances."""

    def __getitem__(self, key) -> Statement:
        if isinstance(key, int):
            # Default behavior for integer keys
            return super().__getitem__(key)
        if isinstance(key, _identifiers.FlexibleUUID):
            # Custom behavior for uuid keys
            item: Statement | None = self.get_from_uuid(uuid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        if isinstance(key, _identifiers.FlexibleUniqueIdentifier):
            # Custom behavior for UniqueIdentifier keys
            item: Statement | None = self.get_from_uid(uid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        else:
            raise TypeError(f'Unsupported key type: {type(key).__name__}')

    def __init__(self, *args):
        self._index = tuple(i.uid for i in self)
        super().__init__()

    def __new__(cls, *args):
        typed_statements = tuple(ensure_statement(r) for r in args)
        return super().__new__(cls, typed_statements)

    def __repr__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def get_from_uid(self, uid: _identifiers.FlexibleUniqueIdentifier,
                     raise_error_if_not_found: bool = False) -> Statement | None:
        """Return a Statement by its UniqueIdentifier.

        :param uid: a UniqueIdentifier.
        :param raise_error_if_not_found:
        :return:
        """
        uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(uid)
        item: Statement | None = next((item for item in self if item.uid == uid), None)
        if item is None and raise_error_if_not_found:
            raise IndexError(f'Statement not found. UID: "{uid}".')
        else:
            return item

    def get_from_uuid(self, uuid: _identifiers.FlexibleUUID,
                      raise_error_if_not_found: bool = False) -> Statement | None:
        """Return a Statement by its UUID.

        :param uuid: a UUID.
        :param raise_error_if_not_found:
        :return:
        """
        uuid: _identifiers.uuid_pkg.UUID = _identifiers.ensure_uuid(uuid)
        if uuid in self._index:
            identifier_index = self._index.index(uuid)
            return self[identifier_index]
        elif raise_error_if_not_found:
            raise IndexError(f'Statement not found. UUID: "{uuid}".')
        else:
            return None

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)
