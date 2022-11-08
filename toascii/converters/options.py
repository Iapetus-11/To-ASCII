from typing import Optional

from pydantic import BaseModel, Field


class ConverterOptions(BaseModel):
    gradient: str = Field(min_length=1)
    width: Optional[int] = Field(default=None, gt=0)
    height: Optional[int] = Field(default=None, gt=0)
    x_stretch: float = Field(default=1.0, gt=0)
    y_stretch: float = Field(default=1.0, gt=0)
    saturation: float = Field(default=0.5, ge=-1, le=1)
    contrast: Optional[float] = Field(default=None, ge=0, le=1)
    blur: Optional[int] = Field(default=None, ge=1)
