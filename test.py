from toascii.converters import ColorConverter, GrayscaleConverter
from toascii.extensions.color_converter_nim import ColorConverterNim
from toascii.gradients import HIGH, BLOCK, LOW
from toascii.image import Image
from toascii.converters.options import ConverterOptions
from toascii.video import Video

# p = "C:\\Users\\miloi\\Pictures\\walle2adj.png"
# i = Image(p, ConverterOptions(scale=0.15, width_stretch=2.1, gradient=LOW), ColorConverter())

# i.view()

# ## 16 pt ft

p = "C:\\Users\miloi\\Downloads\\sam_low.gif"
v = Video(p, ConverterOptions(gradient=LOW, height=64, x_stretch=3.5), ColorConverterNim())
v.view()
