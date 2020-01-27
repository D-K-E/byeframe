# author: Kaan Eraslan
# license: see, LICENSE

from trim import SilenceTrimmer

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
    return parser.parse_args()


if __name__ == "__main__":
    args = parseMainArg()
    path = args.path
    # tmin = args.tmin
    tmax = args.tmax
    tdur = args.tdur
    thread = args.thread
    sys.setrecursionlimit(10000)
    if not thread:
        thread = 3
    if not tmax:
        tmax = 0.1
    if not tdur:
        tdur = 0.05
    trimmer = SilenceTrimmer(
        path,
        # tmin,
        thresh_max=tmax,
        thresh_duration=tdur,
        thread_nb=thread,
    )
    trimmer.trim()
