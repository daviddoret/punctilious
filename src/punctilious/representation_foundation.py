import abc
import typing


class Presenter(abc.ABC):
    """A `Presenter` is an abstract object that is able to generate representations of the object it is linked to."""

    def __call__(self, **kwargs):
        pass

    def get_representation(self, **kwargs) -> str:
        return ''.join(self.yield_representation(**kwargs))

    @abc.abstractmethod
    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        pass


class TechnicalPresenter(Presenter):
    """A `TechnicalPresenter` is a `Presenter` that renders any object as a string of the following format:
        Id (ClassName)

    """

    def __init__(self):
        super().__init__()

    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        yield f'{id(self)} ({self.__class__.__name__})'


technical_representer: Presenter = TechnicalPresenter()


class StringPresenter(Presenter):
    """A `StringPresenter` is a `Presenter` that renders a object as fixed string.

    """

    def __init__(self, string: str):
        self.string = string
        super().__init__()

    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        yield self.string


class Representable(abc.ABC):
    """A `Representable` is an abstract object that has a `Presenter` linked to it.

    """

    def __init__(self, representation_function: Presenter | None = None):
        global technical_representer
        if representation_function is None:
            representation_function = technical_representer
        self._presenter = representation_function

    def __repr__(self) -> str:
        return self.get_representation()

    def __str__(self) -> str:
        return self.get_representation()

    def yield_representation(self, **kwargs) -> typing.Iterator[str]:
        yield from self.presenter.yield_representation(**kwargs)

    def get_representation(self, **kwargs) -> str:
        return self.presenter.get_representation(**kwargs)

    @property
    def presenter(self) -> Presenter:
        """The `Presenter` linked to this object."""
        return self._presenter

    @presenter.setter
    def presenter(self, presenter: Presenter):
        self._presenter = presenter
