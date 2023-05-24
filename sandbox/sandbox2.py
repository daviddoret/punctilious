import core

t = core.Theory()

o1 = t.o()
o2 = t.o()
o3 = t.o()


def morph(phi):
    global r2
    assert isinstance(phi, core.Formula)
    return phi.theory.f(r2, phi.parameters[1], phi.parameters[0])


r1 = t.r(2, symbol='r1', signal_proposition=True, signal_theoretical_morphism=True, implementation=morph)
r2 = t.r(2, symbol='r2', signal_proposition=True)

f1 = t.f(r1, o1, o2)

nla1 = t.nla('blablabla')
fa1 = t.fa(valid_proposition=f1, nla=nla1)

t.prnt()
