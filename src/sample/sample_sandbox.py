"""This sample script export all theory packages."""

import punctilious as pu
import theory as pu_theory

target_folder = '../../data/'

pu.configuration.echo_default = False
t = pu_theory.MGZ2021ClassicalLogicK0().t
print('---------------------------')
print(t.rep_article())

pass
