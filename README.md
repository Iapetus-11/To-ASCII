# To-Ascii ![PYPI Downloads](https://img.shields.io/pypi/dw/to-ascii?color=64b594)
*Converts videos, images, and gifs into ascii art!*

[\[Example\]](https://www.youtube.com/watch?v=S5-_BzdrOkQ) [\[Example 2\]](https://www.youtube.com/watch?v=eX4pYQjCyYg)

* Works on most common image types
* Works on most common video types
* Works on gifs

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
    * `filename` *the name of the file/video which is to be opened and processed*
    * `scale` *the amount/1 which the video dimensions are multiplied by*
    * `w_stretch` *the amount that the width dimension is multiplied by*
    * `gradient` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
    * `verbose` *whether or not to show extra information*
  * Functions:
    * `convert` *actually converts the video into ascii*
    * `view` *view the converted video*

<br>

* toascii.**Image**(**filename**=*'image.png'*, \*, **scale**=*1*, **w_stretch**=*2*, **gradient**=*Union[int, str]*, **verbose**=*False*)
  * Note: only filename can be a positional argument, the rest are kwargs.
  * Arguments:
    * `filename` *the name of the file/image which is to be opened and processed*
    * `scale` *the amount/1 which the image dimensions are multiplied by*
    * `w_stretch` *the amount that the width dimension is multiplied by*
    * `gradient` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
    * `verbose` *whether or not to show extra information*
  * Functions:
    * `convert` *actually converts the image into ascii*
    * `view` *view the converted image*
