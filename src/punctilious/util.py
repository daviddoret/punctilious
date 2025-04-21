class PunctiliousException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message: str = message
        self.variables: dict = kwargs
        super().__init__(message)

    def __str__(self):
        variables: str = ' | '.join(f'`{k}`=`{v!r}`' for k, v in self.variables.items())
        return f'{self.message} | {variables}'
