# author: Kaan Eraslan
# license: see, LICENSE

from moviepy.editor import VideoFileClip, concatenate_videoclips
from typing import Dict
import shutil
import os
from datetime import datetime as dt


class Splitter:
    "Split video clip into given number of parts"

    def __init__(self, nb_parts: int, clip_path: str):
        self.nb_parts = nb_parts
        self.path = clip_path
        self.clip = VideoFileClip(clip_path)
        self.name = os.path.basename(clip_path)
        noext = self.name.split(".")
        noext.pop()
        self.name = "".join([n for n in noext])
        self.dir = os.path.dirname(clip_path)
        date = dt.today()
        fmt = date.strftime("%Y-%m-%d-%H-%M-%S-%f")
        self.sname = "out-" + self.name + "-" + fmt + ".mp4"
        self.subsize = round(self.clip.duration / self.nb_parts, 4)
        #
        self.tempdir = os.path.join(self.dir, "temp" + "-" + self.name)
        #
        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)
        #
        os.mkdir(self.tempdir)
        self.vid_index: Dict[int, str] = {}

    def get_sub_clip(self, start: float, end: float):
        "get sub clip video"
        if self.clip.duration == end:
            return self.clip.subclip(start, None)
        return self.clip.subclip(start, end)

    def get_subclip_name(self, index: int):
        "obtain subclip name"
        name = str(index) + "-" + self.sname
        save_path = os.path.join(self.tempdir, name)
        self.vid_index[index] = save_path
        return save_path

    def save_subclip(self, subclip, index: int):
        "save subclip to temporary folder and hide"
        save_path = self.get_subclip_name(index)
        subclip.write_videofile(save_path)

    def split_clip(self):
        "split clips into subclip"
        counter = 0
        index_counter = 0
        check = True
        while check:
            if counter >= self.clip.duration:
                break
            send = round(counter + self.subsize, 4)
            if send >= self.clip.duration:
                send = self.clip.duration
                check = False
            #
            subclip = self.get_sub_clip(counter, send)
            self.save_subclip(subclip, index_counter)
            print("------------------")
            print(
                "counter:",
                counter,
                "send: ",
                send,
                "index:",
                index_counter,
                "subsize:",
                self.subsize,
                "duration: ",
                self.clip.duration,
            )
            print("------------------")
            index_counter += 1
            counter = send

    def merge_subclips(self):
        "merge subclips using index"
        clips = []
        indices = list(self.vid_index.items())
        indices.sort(key=lambda x: x[0])
        for index in indices:
            path = index[1]
            clip = VideoFileClip(path)
            clips.append(clip)
        #
        merged = concatenate_videoclips(clips)
        return merged

    def save_clip(self, clip: VideoFileClip, thread_nb=1):
        "save clip"
        dname = os.path.dirname(self.path)
        ext = os.path.basename(self.path).split(".").pop()
        # pdb.set_trace()
        date = dt.today()
        fmt = date.strftime("%Y-%m-%d-%H-%M-%S-%f")
        sname = "out-" + fmt + ".mp4"
        spath = os.path.join(dname, sname)
        clip.write_videofile(spath, threads=thread_nb, preset="fast")
