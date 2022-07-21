from toascii import Video, gradients, ColorConverter, ConverterOptions

options = ConverterOptions(gradient=gradients.HIGH, width=32, y_stretch=0.5, saturation=0.25)
converter = ColorConverter(options)
image_path = "some_video.mp4"
image = Video(image_path, converter, loop=True)
image.view()
