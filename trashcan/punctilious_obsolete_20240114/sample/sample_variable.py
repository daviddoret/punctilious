import punctilious as pu

# Create a universe-of-discourse.
u = pu.create_universe_of_discourse(echo=True)
o1 = u.o.register()
o2 = u.o.register()
o3 = u.o.register()
pu.configuration.auto_index = False
f = u.c1.register(symbol='f')
g = u.c1.register(symbol='g')
plus = u.c1.register(symbol='+', formula_rep=pu.CompoundFormula.infix)

# Variables have a scope. But often, when we write mathematical formulas,
# their scope is implicit. Typically, we use "x" multiple times and imply
# that different occurrences of "x" or not necessarily the same variable "x".

# With punctilious_obsolete_20240114, a simple way to declare variables with a precise
# scope is to use the with_variable() method on an instance of UniverseOfDiscourse.
# Here are two examples:

# SAMPLE 1
# Declare a variable and declare a formula that uses it.
# In this example, the scope of the variable "x" is the formula "f(x)".
with u.with_variable(symbol='x') as x:
    phi = f(x)
    print(phi)

# SAMPLE 2
# Declare two variables and declare a formula that uses them.
# In this example, the scope of the variable "x" is the formula "((g(x) + (f(x) + g(y))) + x)".
with u.with_variable(symbol='x') as x, u.with_variable(symbol='y') as y:
    psi = (g(x) | u.c1.plus | (f(x) | u.c1.plus | g(y))) | u.c1.plus | x
    print(psi)

# Note that we created above two distinct "x" variable objects with two distinct scopes:
# the one in SAMPLE 1 and the one in SAMPLE 2.
# This illustrates that two distinct objects may be assigned exactly the same name,
# which may create confusion sometime. And this is often the case with variables.

# The with_variable() method uses the python @contextlib.contextmanager
# to manage automatically the variable scope.

# Alternatively, you may wish to declare variables and define their scope expressly.

# SAMPLE 3
# Declare a variable and close its scope expressly.
x = u.declare_variable(symbol='x')
omega = f(x) | u.c1.plus | x
omega.lock_variable_scope()
print(omega)

# When you call the lock_variable_scope() on an instance of Formula, the scope
# of all the variables contained in the formula is locked and defined as the most
# parent containing formula.
