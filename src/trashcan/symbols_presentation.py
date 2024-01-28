import typesetting as ts
import symbols


def typeset_symbol(o: Symbol, protocol: typing.Optional[ts.Protocol] = None, **kwargs) -> typing.Generator[
    str, None, None]:
    if protocol is None:
        protocol = ts.protocols.default
    match protocol:
        case ts.protocols.latex:
            yield o.latex_math
        case ts.protocols.unicode_extended:
            yield o.unicode_extended
        case ts.protocols.unicode_limited:
            yield o.unicode_limited
        case _:
            raise Exception('Unsupported protocol.')


def typeset_indexed_symbol(o: IndexedSymbol, protocol: typing.Optional[ts.Protocol] = None, **kwargs) -> \
    typing.Generator[str, None, None]:
    if protocol is None:
        protocol = ts.protocols.default
    match protocol:
        case ts.protocols.latex:
            yield from o.symbol.typeset(protocol=protocol, **kwargs)
            yield "_{"
            yield str(o.index)
            yield "}"
        case ts.protocols.unicode_extended:
            yield from o.symbol.typeset(protocol=protocol, **kwargs)
            yield ts.unicode_subscriptify(s=str(o.index))
        case ts.protocols.unicode_limited:
            yield from o.symbol.typeset(protocol=protocol, **kwargs)
            yield str(o.index)
        case _:
            raise Exception('Unsupported protocol.')


ts.register_typesetting_method(python_function=ts.typeset_styled_text, clazz=ts.clazzes.symbol,
    treatment=ts.treatments.default, flavor=ts.flavors.default, language=ts.languages.default)
ts.register_typesetting_method(python_function=typeset_symbol, clazz=ts.clazzes.symbol, treatment=ts.treatments.default,
    flavor=ts.flavors.default, language=ts.languages.default)
ts.register_typesetting_method(python_function=typeset_indexed_symbol, clazz=ts.clazzes.indexed_symbol,
    treatment=ts.treatments.default, flavor=ts.flavors.default, language=ts.languages.default)
