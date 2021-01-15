
    # Visualization of array
    # Created by Zhi Cen on Jan 14, 2021

import numpy as np
import cv2

class Viewer:
    def __init__(self):
        self.alpha = 1

    def array_to_color(self, array):
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        array = array.astype(np.uint8)
        colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_array, alpha=self.alpha), cv2.COLORMAP_JET)
        return colormap
        
    def show_realsense_window(self, depth_array, color_array):
        depth_colormap = self.array_to_color(depth_array)
        # Stack both images horizontally
        images = np.hstack((color_array, depth_colormap))
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)


    def show_vibe_window(self, gray_array, vibe_array):
        gray_array = gray_array.astype(np.uint8)
        vibe_array = vibe_array.astype(np.uint8)
        images = np.hstack((gray_array, vibe_array))
        cv2.namedWindow('Vibe', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Vibe', images)

    def stop(self):
        cv2.destroyAllWindows()