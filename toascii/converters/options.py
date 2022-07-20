from dataclasses import dataclass
from typing import Optional


@dataclass
class ConverterOptions:
    gradient: str
    width: Optional[int] = None
    height: Optional[int] = None
    x_stretch: float = 1.0
    y_stretch: float = 1.0
