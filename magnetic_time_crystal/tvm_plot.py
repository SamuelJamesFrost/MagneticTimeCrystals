import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as manim
import numpy as np
import sys
from .colours import pastel
from . import log
from . import tvm

def record_simulation(video_file, dpi=400, cmap=pastel, fps=5):
    if isinstance(cmap, str):
        cmap = mpl.cm.get_cmap(cmap)

    fig = plt.figure()

    # grab ffmpeg writer
    Writer = manim.writers['ffmpeg']
    writer = Writer(fps=fps)

    magnet = []
    x_axis = [] 

    saver = writer.saving(fig, video_file, dpi=dpi)
    saver.__enter__()

    def generate_frame(*args, **kwargs):
        plt.clf() # clears the figure every cycle so graphs don't accumulate

        img = tvm.graph(*args, **kwargs)

        writer.grab_frame()
        img.remove()

    return generate_frame, lambda: saver.__exit__(*sys.exc_info())

