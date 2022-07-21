from toascii import ConverterOptions, GrayscaleConverter, Image, gradients

options = ConverterOptions(
    gradient=gradients.BLOCK, width=32, y_stretch=0.5, saturation=0.25
)
converter = GrayscaleConverter(options)
image_path = "some_image.png"
image = Image(image_path, converter)
image.view()
