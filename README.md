# byeframe
Trim video clips using audio threshold

## Requirements

- `moviepy == 1.0`: `pip install moviepy==1.0`

## Basic Usage

`python byeframe.py PATH_TO_VIDEO min_thres max_thresh thresh_duration`

And you should obtain an output at the same folder of the input video
called `out.mp4`. 

Here are the available options:

```
usage: byeframe.py [-h] [--tmax TMAX] [--tdur TDUR]
                   [--thread THREAD]
                   path

positional arguments:
  path             Path to video file [home/usr/foo.mp4]

optional arguments:
  -h, --help       show this help message and exit
  --tmax TMAX      maximum threshold for sound [0.1 by default]
  --tdur TDUR      duration in seconds for threshold for sound [0.05 by
                   default]
  --thread THREAD  use multiple thread [3 by default]

```

## Dev Usage

Everything you need for trimming videos is in `trim.py`, if you'd like 
to use it in an api. I use to have a minimum threshold as well to capture
volume ranges, but it did not serve a bunch, plus it was a little difficult
come up with a sensible default value, so I removed that from the
implementation.
However if you have such a need just add a min threshold value to the `if`
statement of `cut_silence` method of the `SilenceTrimmer`.
