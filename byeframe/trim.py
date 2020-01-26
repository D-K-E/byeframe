# author: Kaan Eraslan
# license: see, LICENSE
"""
Deal with fprobe related function
"""

from moviepy.editor import VideoFileClip
import os
import pdb


class SilenceTrimmer:
    def __init__(
        self,
        path: str,
        thresh_min=0.02,
        thresh_max=0.1,
        thresh_duration=0.05,
        thread_nb=3,
    ):
        """
        Enter a threshold value and duration (in seconds 1.3)
        """
        self.path = path
        self.cpv = VideoFileClip(path)
        self.tmin = thresh_min
        self.tmax = thresh_max
        self.tdur = thresh_duration
        self.thread_nb = thread_nb

    def cut_silence(self, start: float, end: float) -> bool:
        "go to next chunk"
        if end >= self.cpv.duration:
            return False
        else:
            sclip = self.cpv.subclip(start, end)
        vol = sclip.audio.max_volume()
        if vol <= self.tmax:
            # pdb.set_trace()
            self.cpv = self.cpv.cutout(start, end)
            return True
        return False

    def trim_clip(self):
        "trim clip using given threshold values"
        counter = 0
        check = True
        while check:
            cend = self.cpv.end
            if counter >= cend:
                break
            send = counter + self.tdur
            if send >= cend:
                check = False
                send = cend
                isCut = self.cut_silence(counter, send)
            else:
                isCut = self.cut_silence(counter, send)
            if not isCut:  # if the cut did not occur I should move to next
                # chunk if it did I should stay in the same place
                # pdb.set_trace()
                counter = send
            # pdb.set_trace()

    def save_clip(self) -> None:
        "save clip to path"
        dname = os.path.dirname(self.path)
        ext = os.path.basename(self.path).split(".").pop()
        # pdb.set_trace()
        spath = os.path.join(dname, "out.mp4")
        self.cpv.write_videofile(spath, threads=self.thread_nb)

    def trim(self):
        "trim and save the clip"
        self.trim_clip()
        self.save_clip()
