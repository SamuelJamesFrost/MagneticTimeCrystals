import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as manim
import numpy as np
import sys
from .colours import pastel
from . import log

def record_simulation(video_file, cycles, duration, fps=5, dpi=192, cmap=pastel):
    if isinstance(cmap, str):
        cmap = mpl.cm.get_cmap(cmap)

    fig = plt.figure()
    frames = fps * duration
    cycles_per_frame = int(cycles / frames)

    # grab ffmpeg writer
    Writer = manim.writers['ffmpeg']
    writer = Writer(fps=fps)

    magnet = []
    x_axis = [] 

    saver = writer.saving(fig, video_file, dpi=dpi)
    saver.__enter__()

    def video_frame_callback(model, cycle):
        if cycle % cycles_per_frame == 0:
            log(f"\rfinished: {round(cycle/cycles * 100)}%", end="")
            plt.clf() # clears the figure every cycle so graphs don't accumulate
            magnet.append(model.magnetisation())
            x_axis.append(cycle)

            plt.subplot(211)
            img = plt.imshow(model.lattice, cmap=cmap, clim=(-1, 1))
            plt.subplot(212)
            plt.plot(x_axis, magnet)

            plt.ylabel("Pseudo-Magnetisation")
            plt.xlabel("Cycles")
            writer.grab_frame()
            img.remove()

    return video_frame_callback, lambda: saver.__exit__(*sys.exc_info())

