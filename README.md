# To-Ascii ![PYPI Downloads](https://img.shields.io/pypi/dw/to-ascii?color=64b594)
*Converts videos, images, gifs, and even live video into ascii art!*

[\[Example\]](https://www.youtube.com/watch?v=S5-_BzdrOkQ) [\[Example 2\]](https://www.youtube.com/watch?v=eX4pYQjCyYg)

* Works on most common image types
* Works on most common video types
* Works on LIVE VIDEO
* Works on gifs

## How does it work?
### Videos:
When the conversion process is started, the video file is opened up and went through frame by frame. Each frame is composed of a set of arrays like `[[[r, g, b], [r, g, b]], [[r, g, b], [r, g, b]]]`, the software then goes through each frame and calculates the average brightness of each pixel, which is then used to get a value from a gradient of ascii characters. Then, at the end, a set of "pretty" frames are made, that list looks like `['frame',  'frame',..]` with frame obviously being the ascii art for each frame. When `.view()` is called or the video is viewed, the software `print()`s out each frame and then `time.sleep()`s for a bit.
### Images:
The process is virtually identical to the one above, except it doesn't need to do a multitude of frames/images, it only needs to convert one. When `.view()` is called it just displays the image.

## Installation
Via pip:
```
python3 -m pip install to-ascii
```

## Example Usage
### CLI:
```
to-ascii -t filetype -f filename
```
### Video / GIF:
```
from toascii import Video

v = Video('my_file.mp4', scale=.1, verbose=True)
v.convert()  # convert the frames into ascii
v.view()  # play the converted frames in the console
```

### Image:
```
from toascii import Image

img = Image('my_image.png', scale=.1, verbose=True)  # load the image
img.convert()  # convert the image to ascii
img.view()  # view the final asciified image
```

## Documentation
* toascii.**Video**(**filename**=*'video.mp4'*, \*, **scale**=*1*, **w_stretch**=*2*, **gradient**=*Union[int, str]*, **verbose**=*False*)
  * Note: only filename can be a positional argument, the rest are kwargs.
  * Arguments:
    * `filename: str` *the name of the file/video which is to be opened and processed*
    * `scale: float` *the amount/1 which the video dimensions are multiplied by*
    * `w_stretch: float` *the amount that the width dimension is multiplied by*
    * `gradient: Union[int, str]` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
    * `verbose: boolean` *whether or not to show extra information*
  * Functions:
    * `convert()` *actually converts the video into ascii*
    * `view(fps: float)` *view the converted video*
  * Attributes:
    * `filename: str` *the name of the file/video which was opened and processed*
    * `video: cv2.VideoCapture` *the actual `cv2.VideoCapture` object*
    * `frames: list` *the converted frames, will be populated when `.convert()` is called*
    * `fps: float` *the fps of the video*
    * `width: int` *the unaltered width of the video*
    * `height: int` *the unaltered height of the video*
    * `scale: float` *the scale which is applied to both the dimensions of the video*
    * `w_stretch: float` *the scale which is only applied to the width dimension*
    * `scaled_width: int` *the final scaled width*
    * `scaled_height: int` *the final scaled height*
    * `gradient: tuple` *the gradient used*
    * `gradient_len: int` *the number of characters in the gradient*
    * `verbose: boolean` *whether or not to do verbose logging*

<br>

* toascii.**Image**(**filename**=*'image.png'*, \*, **scale**=*1*, **w_stretch**=*2*, **gradient**=*Union[int, str]*, **verbose**=*False*)
  * Note: only filename can be a positional argument, the rest are kwargs.
  * Arguments:
    * `filename: str` *the name of the file/image which is to be opened and processed*
    * `scale: str` *the amount/1 which the image dimensions are multiplied by*
    * `w_stretch: float` *the amount that the width dimension is multiplied by*
    * `gradient: float` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
    * `verbose: boolean` *whether or not to show extra information*
  * Functions:
    * `convert()` *actually converts the image into ascii*
    * `view()` *view the converted image*
  * Attributes:
    * `filename: str` *the name of the file/video which was opened and processed*
    * `image: numpy array` *actual numpy array returned from `cv2.imread()`*
    * `width: int` *the unaltered width of the image*
    * `height: int` *the unaltered height of the image*
    * `scale: float` *the scale which is applied to both the dimensions of the image*
    * `w_stretch: float` *the scale which is only applied to the width dimension*
    * `scaled_width: int` *the final scaled width*
    * `scaled_height: int` *the final scaled height*
    * `gradient: tuple` *the gradient used*
    * `gradient_len: int` *the number of characters in the gradient*
    * `verbose: boolean` *whether or not to do verbose logging*

<br>

* toascii.**Live**(**source**=*0*, \*, **scale**=*1*, **w_stretch**=*2*, **gradient**=*Union[int, str]*, **fps**=*10*, **verbose**=*False*)
  * Note: only source can be a positional argument, the rest are kwargs.
  * Arguments:
    * `source: int` *the number relating to the video camera to be used, default is 0*
    * `scale: str` *the amount/1 which the source video dimensions are multiplied by*
    * `w_stretch: float` *the amount that the width dimension is multiplied by*
    * `gradient: int` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
    * `fps: float` *the fps used when showing the live video source*
    * `verbose: boolean` *whether or not to show extra information*
  * Functions:
    * `view()` *view the live video*
  * Attributes:
    * `source: int` *the name of the file/video which was opened and processed*
    * `video: cv2.VideoCapture` *the actual `cv2.VideoCapture` object*
    * `fps: float` *the fps of the live source video*
    * `width: int` *the unaltered width of the live source video*
    * `height: int` *the unaltered height of the live source video*
    * `scale: float` *the scale which is applied to both the dimensions of the live source video*
    * `w_stretch: float` *the scale which is only applied to the width dimension*
    * `scaled_width: int` *the final scaled width*
    * `scaled_height: int` *the final scaled height*
    * `gradient: tuple` *the gradient used*
    * `gradient_len: int` *the number of characters in the gradient*
    * `verbose: boolean` *whether or not to do verbose logging*
