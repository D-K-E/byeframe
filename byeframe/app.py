# author: Kaan Eraslan
# license: see, LICENSE

import tkinter as tk
from tkinter import filedialog as fd
from datetime import datetime as dt
from trim import SilenceTrimmer
import os


class MainWindow:
    def __init__(self, master):
        self.main = tk.Frame(master)
        self.main.pack(expand=1, fill=tk.BOTH)
        self.lst_box_cont = tk.Frame(self.main)
        self.lst_box_cont.pack(side=tk.TOP, fill=tk.Y, expand=1)
        self.lst_box = tk.Listbox(self.lst_box_cont)
        self.lst_box.pack(side=tk.TOP, fill=tk.Y, expand=1)
        self.paths = {}
        self.btn_cont = tk.Frame(self.main)
        self.btn_cont.pack(side=tk.TOP, expand=1, fill=tk.X)
        self.btn_load = tk.Button(self.btn_cont, command=self.get_path, text="Load")
        self.btn_load.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.btn_launch = tk.Button(self.btn_cont, text="Trim Silence",
                command=self.launch_prog)
        self.btn_launch.pack(side=tk.LEFT, expand=1, fill=tk.X)
        self.spin_frame = tk.Frame(self.main)
        self.spin_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.tmax = tk.Spinbox(
            self.spin_frame, format="%.2f", increment=0.01, from_="0.00", to="20.00"
        )
        self.tmax.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.tdur = tk.Spinbox(
            self.spin_frame, format="%.2f", increment=0.01, from_="0.00", to="20.00"
        )
        self.tdur.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.tread_nb = tk.Spinbox(self.spin_frame, increment=1, from_=1, to=6)
        self.tread_nb.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def get_date(self):
        "get current instance"
        date = dt.today()
        fmt = date.strftime("%Y-%m-%d-%H-%M-%S-%f")
        return fmt

    def fill_list(self):
        "fill list with path"
        self.lst_box.delete(0, tk.END)
        for pname in self.paths.keys():
            self.lst_box.insert(tk.END, pname)

    def get_path(self):
        "Obtain paths"
        paths = fd.askopenfilenames(title="Select Videos")
        if paths:
            for path in paths:
                self.paths[os.path.basename(path)] = path
            self.fill_list()

    def remove_lst(self, pname):
        "remove given path from list"
        self.lst_box.delete(pname)

    def launch_prog(self):
        "launch program for paths"
        tmax = float(self.tmax.get())
        tdur = float(self.tdur.get())
        thread = self.thread_nb.get()
        for pname, path in self.paths.items():
            psli = pname.split(".")
            psli.pop()
            oname = "".join([p for p in psli])
            trimmer = SilenceTrimmer(
                path=path,
                thresh_max=tmax,
                thresh_duration=tdur,
                thread_nb=thread,
                out_name=oname,
            )
            trimmer.trim()
            self.remove_lst(pname)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
