from toascii.converters import (ColorConverter, ColorConverterNim,
                                GrayscaleConverter, GrayscaleConverterNim)
from toascii.converters.options import ConverterOptions
from toascii.gradients import BLOCK, HIGH, LOW
from toascii.image import Image
from toascii.video import Video

# p = "C:\\Users\\miloi\\Pictures\\walle2adj.png"
# i = Image(p, ColorConverter(ConverterOptions(scale=0.15, width_stretch=2.1, gradient=LOW)))

# i.view()

# ## 16 pt ft

# p = "C:\\Users\miloi\\Videos\\based_omni_man.mp4"
# v = Video(p, ColorConverterNim(ConverterOptions(gradient=LOW, height=48, x_stretch=6, saturation=1, contrast=.25)))
# v.view()

# p = "C:\\Users\miloi\\Downloads\\rick_roll.mp4"
# v = Video(p, ColorConverterNim(ConverterOptions(gradient=LOW, height=48, x_stretch=4, saturation=1, contrast=.25)))
# v.view()

v = Video(
    0,
    ColorConverterNim(
        ConverterOptions(
            gradient=LOW, height=56, x_stretch=4, saturation=0.5, contrast=0.01
        ),
    ),
)
print(v)
v.view()
