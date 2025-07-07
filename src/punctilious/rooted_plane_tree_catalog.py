import rooted_plane_tree_library as rptl

# 1-node trees
leaf = rptl.RootedPlaneTree()
t1_a = leaf

# 2-nodes trees
t2_a_aa = rptl.RootedPlaneTree(leaf)

# 3-nodes trees
t3_a_aa_aaa = rptl.RootedPlaneTree(t2_a_aa)
t3_a_aa_ab = rptl.RootedPlaneTree(leaf, leaf)

# 4-nodes trees
t4_a_aa_aaa_aaaa = rptl.RootedPlaneTree(t3_a_aa_aaa)
t4_a_aa_aaa_aab = rptl.RootedPlaneTree(t3_a_aa_ab)
t4_a_aa_aaa_ab = rptl.RootedPlaneTree(t2_a_aa, leaf)
t4_a_aa_ab_aba = rptl.RootedPlaneTree(leaf, t2_a_aa)
t4_a_aa_ab_ac = rptl.RootedPlaneTree(leaf, leaf, leaf)

# 5 nodes trees
t5_a_aa_aaa_aaaa_aaaaa = rptl.RootedPlaneTree(t4_a_aa_aaa_aaaa)
# there must be 14 trees in this section

pass
