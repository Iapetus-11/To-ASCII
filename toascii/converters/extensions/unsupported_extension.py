
def UnsupportedExtension(name: str, exception: Exception):
    class _UnsupportedExtension:
        def __init__(self, *args, **kwargs):
            raise RuntimeError(f"{name} can not be initialized.") from exception

    return _UnsupportedExtension
