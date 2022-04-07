import mtc
import matplotlib.pyplot as plt
import numpy as np
# mtc.graph(0)
# plt.show()

# video_frame_at_temp, stop_recording = mtc.tvm_plot.record_simulation('tvm.mp4', fps=1)

# for T in np.arange(0, 3, 0.2):
#     video_frame_at_temp(T, 20, (0, 1), (0.1, 4))
# stop_recording()

mtc.tvm.graph(mtc.nano.Model, res=10, mu=(0.75, 1), tau=(0.25, 3))
plt.show()