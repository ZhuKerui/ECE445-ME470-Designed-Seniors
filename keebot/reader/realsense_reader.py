
    # RealSense Depth Camera D435 Reader
    # Created by Zhi Cen on Jan 14, 2021

import numpy as np
import pyrealsense2 as rs

class RealSenseReader:
    def __init__(self, row=480, col=640):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, col, row, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, col, row, rs.format.bgr8, 30)

    def start(self):
        # Start streaming
        self.pipeline.start(self.config)
    
    def get_depth_color_array(self):        
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        while not depth_frame or not color_frame:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
        # Convert images to numpy arrays
        depth_array = np.asanyarray(depth_frame.get_data())
        color_array = np.asanyarray(color_frame.get_data())
        return depth_array, color_array
    
    def stop(self):
        # Stop streaming
        self.pipeline.stop()