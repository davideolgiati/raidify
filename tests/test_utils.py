import platform
import tempfile

def temp_dirs(func):
    """Decorator to generate temporary directories."""

    def wrap(*args, **kwargs):
        tempdir = "/tmp" if platform.system() == "Darwin" else None
        with tempfile.TemporaryDirectory(dir=tempdir) as source:
            with tempfile.TemporaryDirectory(dir=tempdir) as destination:
                func(*args, **kwargs, source=str(source), destination=str(destination))

    return wrap
