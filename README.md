# to-ascii
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
### Video / GIF:
```
from toascii import Video

v = Video('my_file.mp4', resize=.1, verbose=True)
converted = v.convert()  # convert the frames into ascii
converted.view()  # play the converted frames in the console
```

## Documentation
toascii.**Video**(**filename**=*'video.mp4'*, \*, **scale**=*1*, **w_stretch**=*1*, **gradient**=*Union[int, str]*, **max_workers=*60*, **verbose**=*False*)
Note: only filename can be a positional argument, the rest are kwargs.
* `filename` *the name of the file/video which is to be opened and processed*
* `scale` *the amount/1 which the video dimensions are multiplied by*
* `w_stretch` *the amount that the width dimension is multiplied by*
* `gradient` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
<!--* `max_workers` *the maximum number of workers for the multiprocessing done in conversion of the video* **Note**: *on windows the maximum regardless is 60, going above this will break everything so don't.*-->
* `verbose` *whether or not to show extra information*
