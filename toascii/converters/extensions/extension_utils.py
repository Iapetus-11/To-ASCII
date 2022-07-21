import pathlib

import nimporter

_did_build_extensions = False


def build_extensions() -> None:
    global _did_build_extensions
    if not _did_build_extensions:
        nimporter.build_nim_extensions(pathlib.Path(__file__).parent.resolve())
        _did_build_extensions = True
