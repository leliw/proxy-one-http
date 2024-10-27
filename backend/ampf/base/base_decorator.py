class BaseDecorator[T]:
    def __init__(self, decorated: T) -> None:
        self.decorated = decorated

    def __getattr__(self, name):
        if hasattr(self.decorated, name):
            return getattr(self.decorated, name)
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{name}'"
            )
