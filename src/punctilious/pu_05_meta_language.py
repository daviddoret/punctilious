"""The formal meta-language of the punctilious package.

The meta-language module requires 1) formal-language and 2) interpretation.

"""

# special features
from __future__ import annotations

# external modules
import collections.abc
import typing
import yaml

# punctilious modules
import punctilious.pu_02_identifiers as _identifiers
import punctilious.pu_04_formal_language as _formal_language


class Statement(_formal_language.Formula, _identifiers.UniqueIdentifiable):
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


statement_connector: _formal_language.Connector = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='statement',
                                      uuid='c138b200-111a-4a40-ac3c-c8afa8e615fb')
    # TODO: Pass syntactic_rules = { fixed_arity: 3 }
)

variables_connector: _formal_language.Connector = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='variables',
                                      uuid='0489e6f7-022e-48a4-82bf-dcb5907653b7')
    # TODO: Pass syntactic_rules = { }
)

premises_connector: _formal_language.Connector = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='premises',
                                      uuid='b78ed901-37d2-4a97-a7a8-588b69dab20a')
    # TODO: Pass syntactic_rules = { }
)

conclusion_connector: _formal_language.Connector = _formal_language.Connector(
    uid=_identifiers.UniqueIdentifier(slug='conclusion',
                                      uuid='d66e41ae-9989-48b5-986e-31db0995661d')
    # TODO: Pass syntactic_rules = { fixed_arity: 1 }
)


class Statements(tuple):
    """A tuple of statement formula instances."""

    def __getitem__(self, key) -> _formal_language.Formula:
        if isinstance(key, int):
            # Default behavior for integer keys
            return super().__getitem__(key)
        if isinstance(key, _identifiers.FlexibleUUID):
            # Custom behavior for uuid keys
            item: _formal_language.Formula | None = self.get_from_uuid(uuid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        if isinstance(key, _identifiers.FlexibleUniqueIdentifier):
            # Custom behavior for UniqueIdentifier keys
            item: _formal_language.Formula | None = self.get_from_uid(uid=key, raise_error_if_not_found=False)
            if item is not None:
                return item
        else:
            raise TypeError(f'Unsupported key type: {type(key).__name__}')

    def __init__(self, *args):
        self._index = tuple(i.uid for i in self)
        super().__init__()

    def __new__(cls, *args):
        typed_formulas = tuple(_formal_language.ensure_formula(r) for r in args)
        return super().__new__(cls, typed_formulas)

    def __repr__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def __str__(self):
        return '(' + ', '.join(e.uid.slug for e in self) + ')'

    def get_from_uid(self, uid: _identifiers.FlexibleUniqueIdentifier,
                     raise_error_if_not_found: bool = False) -> _formal_language.Formula | None:
        """Return a Formula by its UniqueIdentifier.

        :param uid: a UniqueIdentifier.
        :param raise_error_if_not_found:
        :return:
        """
        uid: _identifiers.UniqueIdentifier = _identifiers.ensure_unique_identifier(uid)
        item: _formal_language.Formula | None = next((item for item in self if item.uid == uid), None)
        if item is None and raise_error_if_not_found:
            raise IndexError(f'Formula not found. UID: "{uid}".')
        else:
            return item

    def get_from_uuid(self, uuid: _identifiers.FlexibleUUID,
                      raise_error_if_not_found: bool = False) -> _formal_language.Formula | None:
        """Return a Formula by its UUID.

        :param uuid: a UUID.
        :param raise_error_if_not_found:
        :return:
        """
        uuid: _identifiers.uuid_pkg.UUID = _identifiers.ensure_uuid(uuid)
        if uuid in self._index:
            identifier_index = self._index.index(uuid)
            return self[identifier_index]
        elif raise_error_if_not_found:
            raise IndexError(f'Formula not found. UUID: "{uuid}".')
        else:
            return None

    def to_yaml(self, default_flow_style):
        return yaml.dump(self, default_flow_style=default_flow_style)
