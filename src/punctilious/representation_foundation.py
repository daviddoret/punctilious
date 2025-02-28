import abc
import typing


class RepresentationFunction(abc.ABC):

    def __call__(self, **kwargs):
        pass

    def get_representation(self, **kwargs) -> str:
        return ''.join(self.yield_representation(**kwargs))

    @abc.abstractmethod
    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        pass


class TechnicalRepresentation(RepresentationFunction):

    def __init__(self):
        super().__init__()

    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        yield f'{id(self)} ({self.__class__.__name__})'


technical_representation: RepresentationFunction = TechnicalRepresentation()


class Representable(abc.ABC):

    def __init__(self, representation_function: RepresentationFunction | None = None):
        global technical_representation
        if representation_function is None:
            representation_function = technical_representation
        self._representation_function = representation_function

    def __repr__(self) -> str:
        return self.get_representation()

    def __str__(self) -> str:
        return self.get_representation()

    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        yield from self.representation_function.yield_representation(**kwargs)

    def get_representation(self, **kwargs) -> str:
        return self.representation_function.get_representation(**kwargs)

    @property
    def representation_function(self) -> RepresentationFunction:
        return self._representation_function
