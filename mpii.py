import numpy as np
from util import Rodrigues, normalize

class MPII:
    r_ankle = 0
    r_knee = 1
    r_hip = 2
    l_hip = 3
    l_knee = 4
    l_ankle = 5
    pelvis = 6
    spine = 7
    neck = 8
    head = 9
    r_wrist = 10
    r_elbow = 11
    r_shoulder = 12
    l_shoulder = 13
    l_elbow = 14
    l_wrist = 15

    r_shoulder_v = 0
    r_upperarm_v = 1
    r_forearm_v = 2
    l_shoulder_v = 3
    l_upperarm_v = 4
    l_forearm_v = 5
    upperspine_v = 6
    lumbarspine_v = 7
    r_hipbone_v = 8
    r_thigh_v = 9
    r_calfbone_v = 10
    l_hipbone_v = 11
    l_thigh_v = 12
    l_calfbone_v = 13

    point_labels = ['r_ankle', 'r_knee', 'r_hip', 'l_hip', 
                    'l_knee', 'l_ankle', 'pelvis', 'spine', 
                    'neck', 'head', 'r_wrist', 'r_elbow', 
                    'r_shoulder', 'l_shoulder', 'l_elbow', 'l_wrist']

    vector_labels = ['r_shoulder_v', 'r_upperarm_v', 'r_forearm_v', 'l_shoulder_v', 
                    'l_upperarm_v', 'l_forearm_v', 'upperspine_v', 'lumbarspine_v', 
                    'r_hipbone_v', 'r_thigh_v', 'r_calfbone_v', 'l_hipbone_v', 
                    'l_thigh_v', 'l_calfbone_v']

    angle_labels = ['r_arm_0', 'r_arm_1', 'r_arm_2', 'r_arm_3', 
                    'l_arm_0', 'l_arm_1', 'l_arm_2', 'l_arm_3', 
                    'r_leg_0', 'r_leg_1', 'r_leg_2', 'r_leg_3', 
                    'l_leg_0', 'l_leg_1', 'l_leg_2', 'l_lge_3']

    def __init__(self, callback):
        self.vec_start = np.array([self.neck, self.r_shoulder, self.r_elbow, self.neck, 
                                    self.l_shoulder, self.l_elbow, self.neck, self.pelvis, 
                                    self.pelvis, self.r_hip, self.r_knee, self.pelvis, 
                                    self.l_hip, self.l_knee], dtype=np.uint8)
        self.vec_end = np.array([self.r_shoulder, self.r_elbow, self.r_wrist, self.l_shoulder, 
                                self.l_elbow, self.l_wrist, self.spine, self.spine, 
                                self.l_hip, self.r_knee, self.r_ankle, self.l_hip, 
                                self.l_knee, self.l_ankle], dtype=np.uint8)
        self.callback = callback

    def gen_vecs(self, points:np.ndarray):
        return normalize(points[self.vec_end] - points[self.vec_start])

    def gen_init_axis(self, vecs:np.ndarray):
        shoulder_x = vecs[self.upperspine_v]
        r_shoulder_y, l_shoulder_y = np.cross(vecs[[self.r_shoulder_v, self.l_shoulder_v]], shoulder_x)
        r_shoulder_z, l_shoulder_z = np.cross(shoulder_x, [r_shoulder_y, l_shoulder_y])
        l_shoulder_y = - l_shoulder_y # Inverse the direction of y axis for the left side
        
        hip_x = - vecs[self.lumbarspine_v]
        r_hip_y, l_hip_y = np.cross(vecs[[self.r_hipbone_v, self.l_hipbone_v]], hip_x)
        r_hip_z, l_hip_z = np.cross(hip_x, [r_hip_y, l_hip_y])
        l_hip_y = - l_hip_y # Inverse the direction of y axis for the left side
        return normalize(np.array([shoulder_x, r_shoulder_y, r_shoulder_z, shoulder_x, l_shoulder_y, l_shoulder_z, hip_x, r_hip_y, r_hip_z, hip_x, l_hip_y, l_hip_z])).reshape(4,3,3)

    def cal_limb_angle(self, upper_limb:np.ndarray, lower_limb:np.ndarray, init_axis:np.ndarray):
        project_vec = upper_limb - (upper_limb.dot(init_axis[1]) * init_axis[1])
        project_vec /= np.linalg.norm(project_vec)
        theta_0 = np.arccos(project_vec.dot(init_axis[0]))
        theta_1 = np.arccos(upper_limb.dot(init_axis[1]))
        axis = init_axis
        R1 = Rodrigues(theta_0, axis[1])
        axis = np.matmul(R1, axis.T).T
        R2 = Rodrigues(theta_1, axis[2])
        axis = np.matmul(R2, axis.T).T

        project_vec = lower_limb - (lower_limb.dot(axis[0]) * axis[0])
        project_vec /= np.linalg.norm(project_vec)
        theta_2 = np.arccos(project_vec.dot(init_axis[2]))
        theta_3 = np.arccos(lower_limb.dot(axis[0]))
        theta_3 = 130 if theta_3 > 130 else theta_3

        return (np.array([theta_0, theta_1, theta_2, theta_3]) * 180 / np.pi).astype(int)

    def handle_pose_data(self, points:np.ndarray):
        vecs = self.gen_vecs(points)
        r_shoulder_axis, l_shoulder_axis, r_hip_axis, l_hip_axis = self.gen_init_axis(vecs)
        r_arm_angle = self.cal_limb_angle(vecs[self.r_upperarm_v], vecs[self.r_forearm_v], r_shoulder_axis)
        l_arm_angle = self.cal_limb_angle(vecs[self.l_upperarm_v], vecs[self.l_forearm_v], l_shoulder_axis)
        r_hip_angle = self.cal_limb_angle(vecs[self.r_thigh_v], vecs[self.r_calfbone_v], r_hip_axis)
        l_hip_angle = self.cal_limb_angle(vecs[self.l_thigh_v], vecs[self.l_calfbone_v], l_hip_axis)
        angle = np.hstack([r_arm_angle, l_arm_angle, r_hip_angle, l_hip_angle])
        angle[angle >= 180] = 180
        angle[angle < 1] = 1
        self.callback(angle.astype(np.uint8))