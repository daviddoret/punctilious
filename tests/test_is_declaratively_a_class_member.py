from unittest import TestCase
import punctilious as pu


class IsDeclarativelyMemberOfClass(TestCase):
    def test_is_declaratively_member_of_class(self):
        pu.configuration.encoding = pu.encodings.unicode
        u = pu.UniverseOfDiscourse()
        with u.with_variable(symbol='x') as x1:
            self.assertTrue(pu.is_declaratively_member_of_class(u=u, phi=x1, c=u.c2.formula))
            self.assertTrue(pu.is_declaratively_member_of_class(u=u, phi=x1, c=u.c2.free_variable))
        r = u.r.declare()
        self.assertTrue(pu.is_declaratively_member_of_class(u=u, phi=r, c=u.c2.formula))
        self.assertTrue(pu.is_declaratively_member_of_class(u=u, phi=r, c=u.c2.connective))
        o = u.o.declare()
        self.assertTrue(pu.is_declaratively_member_of_class(u=u, phi=o, c=u.c2.formula))
        self.assertTrue(pu.is_declaratively_member_of_class(u=u, phi=o, c=u.c2.simple_object))

        # TODO: NEXT STEP:
