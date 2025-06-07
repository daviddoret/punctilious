import immutable_computable_rooted_plane_tree as icrpt


class AbstractFormula(tuple):
    def __init__(self, canonical_connectors_index, rooted_plane_tree: icrpt.FlexibleRootedPlaneTree):
        super(AbstractFormula, self).__init__()

    def __new__(cls, canonical_connectors_index, rpt: icrpt.FlexibleRootedPlaneTree):
        rpt: icrpt.RootedPlaneTree = icrpt.data_validate_rooted_plane_tree(rpt)
        af = super(AbstractFormula, cls).__new__(cls, (canonical_connectors_index, rpt))
        return af
