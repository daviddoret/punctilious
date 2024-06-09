import punctilious as pu

l = pu.pl1.MinimalistPropositionalLogic()
pu.preferences.typesetting.protocol.protocol = pu.ts.protocols.unicode_extended
print(l.axiomatization.pl1)
print(l.axiomatization.pl2)
print(l.axiomatization.pl3)
print(l.axiomatization.pl4)
print(l.axiomatization.pl5)
pass
