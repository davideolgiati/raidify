import sys
import tempfile


def temp_dirs(func):
    """Decorator to generate temporary directories."""

    def wrap(*args, **kwargs):
        sys.argv = sys.argv[:1]
        with tempfile.TemporaryDirectory() as source:
            with tempfile.TemporaryDirectory() as destination:
                func(
                    *args,
                    **kwargs,
                    source=str(source),
                    destination=str(destination)
                )

    return wrap
