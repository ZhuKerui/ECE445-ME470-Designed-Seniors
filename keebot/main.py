
    # Main
    # Created by Zhi Cen on Jan 14, 2021

import numpy as np
import cv2
import time
from tqdm import tqdm

from reader.realsense_reader import RealSenseReader
from visualization.viewer import Viewer
from segmentation.vibe import Vibe

if __name__ == "__main__":
    ROW = 480
    COL = 640
    reader = RealSenseReader(ROW, COL)
    reader.start()
    viewer = Viewer()
    segmentation = Vibe(ROW, COL)

    depth_array, color_array = reader.get_depth_color_array()
    gray_array = cv2.cvtColor(color_array, cv2.COLOR_RGB2GRAY)
    segmentation.process_first_frame(gray_array)

    # t0 = time.time()
    # for i in tqdm(range(10)):
    #     for j in range(5):
    #         segmentation.process_first_frame(gray_array)
    # t1 = time.time()
    # print(t1 - t0)

    # t2 = time.time()
    # for i in tqdm(range(20)):
    #     for j in range(10):
    #         depth_array, color_array = reader.get_depth_color_array()
    #         gray_array = cv2.cvtColor(color_array, cv2.COLOR_RGB2GRAY)
    #         vibe_array = segmentation.run(gray_array)
    #         viewer.show_vibe_window(gray_array, vibe_array)
    # t3 = time.time()
    # print(t3 - t2)

    while True:
        depth_array, color_array = reader.get_depth_color_array()
        # viewer.show_realsense_window(depth_array, color_array)
        gray_array = cv2.cvtColor(color_array, cv2.COLOR_RGB2GRAY)
        vibe_array = segmentation.run(gray_array)
        viewer.show_vibe_window(gray_array, vibe_array)
        # Press esc to stop
        if cv2.waitKey(1) == 27:
            break
    
    reader.stop()
    viewer.stop()
            