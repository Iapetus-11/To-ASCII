# To-Ascii ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/to-ascii/badge/master) ![PYPI Version](https://img.shields.io/pypi/v/to-ascii.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/to-ascii?color=0FAE6E) ![Views](https://api.ghprofile.me/view?username=iapetus-11.to-ascii&color=0FAE6E&label=views&style=flat)
*Converts videos, images, gifs, and even live video into ascii art!*

[\[Example\]](https://www.youtube.com/watch?v=S5-_BzdrOkQ) [\[Example 2\]](https://www.youtube.com/watch?v=eX4pYQjCyYg)

* Works on most common image types
* Works on most common video types
* Works on GIFs
* Works on LIVE VIDEO

## Installation
Via pip:
```
pip install to-ascii
```

## CLI Usage:
*Note: Required arguments are surrounded in `<>`, optional arguments are surrounded in `[]`.*

```
asciify <type> <source> <scale> [width stretch] [gradient] [loop]
```

### CLI Arguments:
- `type` - The type of content, either IMAGE, VIDEO, or LIVE.
- `source` - The source, either a file path or video device.
- `scale` - Used to scale down the image to fit in your console, recommended value is 0.1.
- `width stretch`- Used to account for console characters being taller than they are wide, default value is 2.0.
- `gradient` - The gradient used, one of BLOCK, HIGH, LOW, or a custom gradient as a string.
- `loop` - If "loop" is the 5th argument, the displayed ASCII video will loop until interrupted.

### CLI Examples:
```
asciify image ~/Downloads/image4.gif .6 2.5 block loop
asciify live 0 .055 4.5 low
asciify image ~/Downloads/image4.png .6 2.5 block
asciify image ~/Downloads/image4.png .6 2.5 kkadjfjkdfkaj
asciify video ~/Videos/bruhh.mp4 .05 3.5 high
```

## API Reference
- toascii.**ImageConverter**(filename: *str*, scale: *float*, width_stretch: *float*, gradient: *str*)
  - Parameters:
    - `filename` - *the file path of the image to convert*
    - `scale` - *the value to scale the image by*
    - `width_stretch` - *the value to scale the width extra by*
    - `gradient` - *the gradient to use when asciifying the image*
  - Attributes:
    - `ascii_image` - *the asciified image as a string, only present after `ImageConverter.convert()` has been called*
  - Methods:
    - `convert()` - *converts the source image into ascii and stores it in the `ascii_image` attribute*
    - `view()` - *displays the converted image in the console*


- toascii.**VideoConverter**(filename: *str*, scale: *float*, width_stretch: *float*, gradient: *str*, loop: *bool*)
  - Parameters:
    - `filename` - *the file path of the video to convert*
    - `scale` - *the value to scale the video dimensions by*
    - `width_stretch` - *the value to scale the video width extra by*
    - `gradient` - *the gradient to use when asciifying the video*
    - `loop` - *whether to loop the video at the end when viewing it, defaults to `False`*
  - Attributes:
    - `ascii_frames` - *the asciified video's frames in a list, only present after `VideoConverter.convert()` has been called*
  - Methods:
    - `convert()` - *converts the source video into ascii and stores it in the `ascii_frames` attribute*
    - `view()` - *plays the converted video in the console*


- toascii.**LiveVideoConverter**(source: *Union[str, int]*, scale: *float*, width_stretch: *float*, gradient: *str*)
  - Parameters:
    - `source` - *the source device / camera to grab the frames from*
    - `scale` - *the value to scale the video dimensions by*
    - `width_stretch` - *the value to scale the video width extra by*
    - `gradient` - *the gradient to use when asciifying the video*
  - Methods:
    - `get_ascii_frame()` - *grabs a frame from the camera and converts it*
    - `view()` - *view the live video in the console*
