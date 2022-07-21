from toascii import ColorConverter, ConverterOptions, Video, gradients

options = ConverterOptions(
    gradient=gradients.LOW, height=56, x_stretch=4, saturation=0.5, contrast=0.01
)
converter = ColorConverter(options)
camera_id = 0
video = Video(camera_id, converter)
video.view()
