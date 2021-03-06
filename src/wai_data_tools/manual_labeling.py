

import logging
import pathlib
from typing import Dict, Union, List

import matplotlib.pyplot as plt
import matplotlib.widgets as pltwid
import numpy as np

from wai_data_tools.io import save_frames


class Callbacks:
    """
    Class for handling callbacks for annotation GUI.
    """
    def __init__(self,
                 frame_dict: Dict[int, Dict[str, Union[str, np.ndarray]]],
                 ax_img,
                 ax_togg,
                 frame_dir: pathlib.Path,
                 new_dir: pathlib.Path,
                 classes: List[str]):

        self.frame_dict = frame_dict
        self.frame_dir = frame_dir
        self.new_dir = new_dir
        self.ax_togg = ax_togg
        self.ax_img = ax_img
        self.plt_img = ax_img.imshow(self.frame_dict[0]["img"])
        self.index = 0
        self.max_index = max(self.frame_dict.keys())
        self.classes = classes
        self.class_ind = 0

    def next(self, event):
        if self.index < self.max_index:
            self.index += 1
        else:
            self.index = 0

        self.draw_img()

    def prev(self, event):
        if self.index > 0:
            self.index -= 1
        else:
            self.index = self.max_index

        self.draw_img()

    def draw_img(self):
        self.plt_img.set_array(self.frame_dict[self.index]["img"])
        self.ax_img.set_title(f"Frame {self.index}")
        self.ax_togg.set_title(f"Class: {self.frame_dict[self.index]['target']}")
        plt.pause(0.001)

    def toggle_label(self, event):

        self.class_ind = (self.class_ind + 1) % len(self.classes)

        new_class = self.classes[self.class_ind]

        logging.debug("Toggling Frame %s from %s to %s",
                      self.index,
                      self.frame_dict[self.index]["target"],
                      new_class)

        self.frame_dict[self.index]["target"] = new_class
        self.ax_togg.set_title(f"Class: {self.frame_dict[self.index]['target']}")
        plt.pause(0.001)

    def hotkey_press(self, event):
        if event.key == "t":
            self.toggle_label(event=None)
        elif event.key == "left":
            self.prev(event=None)
        elif event.key == "right":
            self.next(event=None)

    def save_frames(self, event):
        save_frames(video_name=self.frame_dir.stem,
                    dst_root_dir=self.new_dir,
                    frames_dict=self.frame_dict)


def manual_annotation_plot(frame_dict: Dict[int, Dict[str, Union[bool, np.ndarray]]],
                           frame_dir: pathlib.Path,
                           dst_root_dir: pathlib.Path,
                           classes: List[str]):
    fig, ax = plt.subplots()

    plt.subplots_adjust(bottom=0.2)

    axsave = plt.axes([0.1, 0.05, 0.1, 0.075])
    axtogg = plt.axes([0.5, 0.01, 0.15, 0.075])
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])

    bsave = pltwid.Button(axsave, "Save")
    bnext = pltwid.Button(axnext, "Next")
    bprev = pltwid.Button(axprev, "Previous")
    btogg = pltwid.Button(axtogg, "Toggle Class")

    callbacks = Callbacks(frame_dict=frame_dict,
                          ax_img=ax,
                          ax_togg=axtogg,
                          frame_dir=frame_dir,
                          new_dir=dst_root_dir,
                          classes=classes)
    callbacks.draw_img()

    bnext.on_clicked(callbacks.next)
    bprev.on_clicked(callbacks.prev)
    btogg.on_clicked(callbacks.toggle_label)
    bsave.on_clicked(callbacks.save_frames)

    fig.canvas.mpl_connect('key_press_event', callbacks.hotkey_press)

    plt.show()
