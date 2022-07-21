class UnsupportedExtensionException(RuntimeError):
    def __init__(self, ext_name: str, from_exc: Exception):
        super().__init__(f"{ext_name} can not be initialized.")

        self.ext_name = ext_name
        self.from_exc = from_exc


def unsupported_extension(ext_name: str, exception: Exception):
    class _UnsupportedExtension:
        def __init__(self, *args, **kwargs):
            raise UnsupportedExtensionException(ext_name, exception) from exception

    return _UnsupportedExtension
