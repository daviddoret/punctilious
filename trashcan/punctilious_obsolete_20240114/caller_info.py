"""
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""
import inspect


def caller_info(skip=2):
    """Get the name of a caller in the format module.class.method.

    Copied from: https://gist.github.com/techtonik/2151727

    :arguments:
        - skip (integer): Specifies how many levels of stack
                          to skip while getting caller name.
                          skip=1 means "who calls me",
                          skip=2 "who calls my caller" etc.

    :returns:
        - package (string): caller package.
        - module (string): caller module.
        - klass (string): caller classname if one otherwise None.
        - caller (string): caller function or method (if a class exist).
        - line (int): the line of the call.
        - An empty string is returned if skipped levels exceed stack height.
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]

    # module and packagename.
    module_info = inspect.getmodule(parentframe)
    package = None
    module = None
    if module_info:
        mod = module_info.__name__.split('.')
        package = mod[0]
        module = mod[1]

    # class name.
    klass = None
    if 'self' in parentframe.f_locals:
        klass = parentframe.f_locals['self'].__class__.__name__

    # method or function name.
    caller = None
    if parentframe.f_code.co_name != '<module>':  # top level usually
        caller = parentframe.f_code.co_name

    # call line.
    line = parentframe.f_lineno

    # Remove reference to frame
    # See: https://docs.python.org/3/library/inspect.html#the-interpreter-stack
    del parentframe

    return package, module, klass, caller, line


def friendly_caller_info(skip: int):
    components = caller_info(skip=skip)
    return '.'.join(filter(None, [str(elem) for elem in components]))
