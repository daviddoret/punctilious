import _util
import _formal_language
import _packaging


class TaoAnalysis12006(_packaging.MultiYamlFileBundle):
    """A punctilious package of well-known mathematical operators."""
    _singleton = None
    _singleton_initialized = None

    def __init__(self):
        if self.__class__._singleton_initialized is None:
            connectors = _packaging.YamlFileBundle(path='data.connectors',
                                                   resource='tao_analysis_1_2006.yaml')
            representations = _packaging.YamlFileBundle(path='data.representations',
                                                        resource='tao_analysis_1_2006.yaml')
            mappings = _packaging.YamlFileBundle(path='data.mappings',
                                                 resource='tao_analysis_1_2006.yaml')
            yaml_files = (connectors, representations, mappings,)
            super().__init__(yaml_files=yaml_files)
            self.__class__._singleton_initialized = True
            _util.get_logger().debug(
                f'Tao Analysis 1 (2006) singleton ({id(self)}) initialized.')

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            cls._singleton = super(TaoAnalysis12006, cls).__new__(cls)
        return cls._singleton

    @property
    def successor(self) -> _formal_language.Connector:
        return self.connectors.get_from_slug('successor')

    @property
    def zero(self) -> _formal_language.Connector:
        return self.connectors.get_from_slug('zero')
