# To-Ascii ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/to-ascii/badge/master) ![PYPI Version](https://img.shields.io/pypi/v/to-ascii.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/to-ascii?color=0FAE6E)
*Converts videos, images, gifs, and even live video into ascii art!*

* Works on most image and video types including GIFs
* Works on LIVE VIDEO

<img src="https://user-images.githubusercontent.com/38477514/180253533-e0725ba5-6c6d-408d-a643-ff02f021cff8.png" width="360" /> <img src="https://user-images.githubusercontent.com/38477514/180254306-9e8eca93-ea38-47bf-b1c2-72ad75244604.png" width="360" /> <img src="https://user-images.githubusercontent.com/38477514/180251469-8826a23d-a292-42b2-83c6-c9a637214b5e.png" width="360" /> <img src="https://user-images.githubusercontent.com/38477514/180251666-49b07f5f-da3c-4790-85b9-ba72dbca606b.png" width="360" />

[[DEMO SITE]](https://ascii.iapetus11.me/) [\[Video Example\]](https://www.youtube.com/watch?v=S5-_BzdrOkQ) [\[Video Example 2\]](https://www.youtube.com/watch?v=eX4pYQjCyYg) 

## Installation
Via pip:
```
pip install to-ascii
```

## CLI Usage
*Note: Required arguments are surrounded in `<>`, optional arguments are surrounded in `[]`.*
```
toascii <media_type> <source> <converter> [--gradient <string>] [--width <int>] [--height <int>] [--xstretch <float>] [--ystretch <float>] [--saturation <float>] [--contrast <float>] [--loop]
```

### CLI Arguments
- `media_type` - the type of media, either `image` or `video`
- `source` - the source for the media, this is the primary argument in constructing an instance of an [OpenCV `VideoCapture`](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html)
- `converter` - the converter used to convert the media, check [this file](toascii/converters/__init__.py) for the available options
- `gradient` - the characters used when converting an image to ascii
- `width` - an integer value for the width in characters of the final converted image
- `height` - an integer value for the height in characters of the final converted image
- `xstretch` - the amount to stretch the width by
- `ystretch` - the amount to stretch the height by
- `saturation` - how much to saturate the image, a value from -1.0 to 1.0.
- `contrast` - how much to modify the contrast, a value from 0.0 to 1.0
- `loop` - whether or not to loop the video when it is done playing

### CLI Examples
```bash
# live video
toascii video 0 grayscaleconverternim --xstretch 3 --height 56 --saturation .25 --contrast .01
```
```bash
toascii image "C:\Users\miloi\Pictures\my_image.png" colorconverter
```
```bash
toascii video "C:\Users\miloi\Videos\omni_man.mp4" colorconverternim --height 32 --width 48 --saturation 0.5 --contrast 0.01 --loop
```

## API Reference
### [Usage Examples Folder](examples)
#### *class* [`ConverterOptions`](toascii/converters/options.py)(\*, `gradient`: *`str`*, `width`: *`Optional[int]`*, `height`: *`Optional[int]`*, `x_stretch`: *`float`*, `y_stretch`: *`float`*, `saturation`: *`float`*, `contrast`: *`Optional[float]`*)
- *pydantic model for converter options*
- Parameters / Attributes:
    - `gradient`: *`str`* - *string containing the characters the converter will use when converting the image to ascii*
        - must be at least one character
    - `width`: *`Optional[int]`* - *width in characters of the final converted image*
        - default value is `None`
        - must be greater than `0`
    - `height`: *`Optional[int]`* - *height in characters of the final converted image*
        - default value is `None`
        - must be greater than `0`
    - `x_stretch`: *`float`* - *how much to stretch the width by*
        - default value is `1.0` (which doesn't change the width by anything)
        - must be greater than `0.0`
    - `y_stretch`: *`float`* - *how much to stretch the height by*
        - default value is `1.0` (which doesn't change the height by anything)
        - must be greater than `0.0`
    - `saturation`: *`float`* - *how much to adjust the saturation*
        - default value is `0.5` (which increases the saturation)
        - must be between `-1.0` and `1.0`, `0.0` is no change to saturation
    - `contrast`: *`Optional[float]`* - *how much to increase the contrast by*
        - default value is `None` (which doesn't apply any contrast filter)
        - must be between `0.0` and `1.0`
#### *class* [`ConverterBase`](toascii/converters/base_converter.py)(`options`: *`ConverterOptions`*)
- *base class for implementing converters*
- Parameters:
    - `options`: *`ConverterOptions`* - *Options used when converting media*
- Methods:
    - *abstract* `asciify_image`(`image`: *`numpy.ndarray`*) -> *`str`*
    - `calculate_dimensions`(`initial_height`: *`int`*, `initial_width`: *`int`*) -> *`Tuple[int, int]`*
    - `resize_image`(`image`: *`numpy.ndarray`*) -> *`numpy.ndarray`*
- Implementations:
    - [`GrayscaleConverter`](toascii/converters/grayscale_converter.py) - *converts media to grayscale ascii*
    - [`GrayscaleConverterNim`](toascii/converters/extensions/grayscale_converter_nim.py) - *converters media to grayscale ascii, see the [Extensions](#extensions) section*
    - [`ColorConverter`](toascii/converters/color_converter.py) - *converts media to colored ascii using [Colorama](https://pypi.org/project/colorama/)*
    - [`ColorConverterNim`](toascii/converters/extensions/color_converter_nim.py) - *converts media to colored ascii using [Colorama](https://pypi.org/project/colorama/), see the [Extensions](#extensions) section*
    - [`HtmlColorConverter`](toascii/converters/html_color_converter.py) - *converts media to ascii in colored html spans*
    - [`HtmlColorConverterNim`](toascii/converters/extensions/html_color_converter_nim.py) - *converts media to ascii in colored html spans, see the [Extensions](#extensions) section*
#### *class* [`Image`](toascii/image.py)(`source`: *`Union[str, bytes, IOBase]`*, `converter`: *`BaseConverter`*)
- *class for converting an image to ascii*
- Parameters:
    - `source`: *`Union[str, bytes, IOBase]`* - *the source of the image that is to be loaded and converted*
        - if `source` is a `str`, it's assumed that it's a path to an image file
        - if `source` is `bytes` or `IOBase` it's assumed to be the data of an image and is decoded in-memory
    - `converter`: *`ConverterBase`* - *the converter used to convert the image*
        - takes anything that implements `ConverterBase`
- Methods:
    - `to_ascii`() -> *`str`*
        - *returns the image converted by the converter*
    - `view`() -> *`None`*
        - *prints out the converted image to the console*
#### *class* [`Video`](toascii/video.py)(`source`: *`Union[str, int, bytes, IOBase]`*, `converter`: *`BaseConverter`*, \*, `fps`: *`Optional[float]`*, `loop`: *`bool`*)
- *class for converting a video to ascii*
- Parameters:
    - `source`: *`Union[str, int bytes, IOBase]`* - *the source of the video that is to be loaded and converted*
        - if `source` is a `str`, it's assumed that it's a path to an image file
        - if `source` is `bytes` or `IOBase` it's assumed to be the data of an image and is written to a temporary file before being loaded and decoded by OpenCV
        - if `source` is an `int`, it's assumed to be the index of a camera device
        - see [OpenCV's `VideoCapture`](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html) for more information
    - `converter`: *`ConverterBase`* - *the converter used to convert the image*
        - takes anything that implements `ConverterBase`
    - `fps`: *`Optional[float]`* - *the fps to play the video at*
        - default value is `None`
        - if `None` then the fps used is fetched from OpenCV's `VideoCapture` API
    - `loop`: *`bool`* - *whether or not to loop the video when it's done playing*
        - default value is `False`
        - if the video source is live, this parameter is ignored
- Methods:
    - `get_ascii_frames`() -> *`Generator[str, None, None]`* - *returns a generator which yields each ascii frame as it is converted*
    - `view`() -> *`None`* - *prints out each frame of the converted video*
        - if the video source is not live, this method will first generate all frames and cache them in memory for a smoother playback
        - if the `loop` parameter was set to `True` earlier, then this will play the video and restart it when it finishes unless the source is live

## Extensions
- For each converter available, there is a separate implementation written in [Nim](https://nim-lang.org/)
- These implementations are generally orders of magnitude faster than their Python counterparts
- To use these extensions you must [install Nim](https://nim-lang.org/install.html) and install the `to-ascii[speedups]` package via pip or your package manager of choice
