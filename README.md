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
converted.classic_view()  # play the converted frames
```

## Documentation
