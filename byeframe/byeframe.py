# author: Kaan Eraslan
# license: see, LICENSE

from trim import SilenceTrimmer
from split import Splitter

import argparse
import sys


def parseMainArg():
    "parse main argument"
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to video file [home/usr/foo.mp4]", type=str)
    parser.add_argument(
        "--tmax", help="maximum threshold for sound [0.1 by default]", type=float
    )
    parser.add_argument(
        "--tdur",
        help="duration in seconds for threshold for sound [0.05 by default]",
        type=float,
    )
    parser.add_argument("--thread", help="use multiple thread [3 by default]", type=int)
    parser.add_argument("--splitNb", help="split video to nb parts", type=int)
    return parser.parse_args()


def split_pipeline(path, tmax, tdur, thread, split_part: int):
    "split pipeline"
    splitter = Splitter(nb_parts=split_part, clip_path=path)
    print("my pipeline")
    splitter.split_clip()
    dcopy = splitter.vid_index.copy()
    for index, npath in splitter.vid_index.items():
        trimmer = SilenceTrimmer(
            npath,
            # tmin,
            thresh_max=tmax,
            thresh_duration=tdur,
            thread_nb=thread,
        )
        trimmer.trim()
        dcopy[index] = trimmer.spath
    splitter.vid_index = dcopy
    merged_video = splitter.merge_subclips()
    splitter.save_clip(merged_video, thread)


if __name__ == "__main__":
    args = parseMainArg()
    path = args.path
    # tmin = args.tmin
    tmax = args.tmax
    tdur = args.tdur
    thread = args.thread
    splitnb = args.splitNb
    sys.setrecursionlimit(10000)
    if not thread:
        thread = 3
    if not tmax:
        tmax = 0.1
    if not tdur:
        tdur = 0.05
    if splitnb:
        split_pipeline(path, tmax, tdur, thread, splitnb)
    else:
        trimmer = SilenceTrimmer(
            path,
            # tmin,
            thresh_max=tmax,
            thresh_duration=tdur,
            thread_nb=thread,
        )
        trimmer.trim()
    print("Done!")
