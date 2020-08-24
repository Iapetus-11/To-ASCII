# video2ascii
*Goes through a video frame by frame, and converts each frame into ascii art*

## Installation
Via pip:
```
python3 -m pip install video2ascii
```

## Example Usage
```
from video2ascii import Video

v = Video('my_file.mp4', resize_amount=.3, w_stretch=2, verbose=True)
converted = v.convert()  # convert the frames into ascii
converted.view()  # play the converted frames in the console
```

## Documentation
video2ascii.**Video**(**filename**=*'video.mp4'*, \*, **resize_amount**=*1*, **w_stretch**=*1*, **gradient**=*Union[int, str]*, **verbose**=*False*)
Note: only filename can be a positional argument, the rest are kwargs.
* `filename` *the name of the file/video which is to be opened and processed*
* `resize_amount` *the amount/1 which the video dimensions are multiplied by*
* `w_stretch` *the amount that the width dimension is multiplied by*
* `gradient` *either an integer from the preset gradients, or a custom gradient Example: '#$a=+-., '*
* `verbose` *whether or not to show extra information*
