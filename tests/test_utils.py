import tempfile

def temp_dirs(func):
    """Decorator to generate temporary directories."""

    def wrap(*args, **kwargs):
        with tempfile.TemporaryDirectory() as source:
            with tempfile.TemporaryDirectory() as destination:
                func(*args, **kwargs, source=str(source), destination=str(destination))

    return wrap
