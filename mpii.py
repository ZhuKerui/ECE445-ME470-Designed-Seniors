import numpy as np
from util import Rodrigues, normalize
from time import time

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

    RIGHT_ARM = 0
    LEFT_ARM = 1
    RIGHT_LEG = 2
    LEFT_LEG = 3

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

    def __init__(self):
        # Predefine the indices of the starting points for the vectors
        self.vec_start = np.array([self.neck, self.r_shoulder, self.r_elbow, self.neck, 
                                    self.l_shoulder, self.l_elbow, self.neck, self.pelvis, 
                                    self.pelvis, self.r_hip, self.r_knee, self.pelvis, 
                                    self.l_hip, self.l_knee], dtype=np.uint8)
        # Predefine the indices of the ending points for the vectors
        self.vec_end = np.array([self.r_shoulder, self.r_elbow, self.r_wrist, self.l_shoulder, 
                                self.l_elbow, self.l_wrist, self.spine, self.spine, 
                                self.r_hip, self.r_knee, self.r_ankle, self.l_hip, 
                                self.l_knee, self.l_ankle], dtype=np.uint8)
        # Denoise components
        self.is_denoise = False                 # Whether denoise is enabled
        self.hist_len = 5
        self.velocity_raw_history = np.zeros((self.hist_len, 16))
        self.last_angle = np.zeros(16)                  # Last sent angle
        self.last_time = time()
        self.interval = 1000

        self.div_lim = 100
        # self.d_lim = np.array([10, 10, 10, 10, 
        #               10, 10, 10, 10,
        #               10, 10, 10, 10,
        #               10, 10, 10, 10], dtype=np.float64)
        # self.v_lim = np.array([10, 10, 10, 10, 
        #               10, 10, 10, 10,
        #               10, 10, 10, 10,
        #               10, 10, 10, 10], dtype=np.float64)
        self.v_lim = np.ones(16) * 60

        # Components for visualizing the denoised pose
        self.std_pose = np.array([[2., 2., 2.], [2., 1., 2.], [2., 0., 2.],             # The standard (or initial) position for the joints
                                [0., 0., 2.], [0., 1., 2.], [0., 2., 2.], 
                                [1., 0., 2.], [1., 0., 3.], [1., 0., 4.], [1., 0., 5.], 
                                [2., 2., 4.], [2., 1., 4.], [2., 0., 4.], 
                                [0., 0., 4.], [0., 1., 4.], [0., 2., 4.]])
        self.init_limb_vecs = self.gen_vecs(self.std_pose)                              # The standard (or initial) vector for each part
        self.rot_r_arm_axis = np.array([[0., 0., -1.], [0., 1., 0.], [1., 0., 0.]])     # The initial rotation axises for right arm
        self.rot_l_arm_axis = np.array([[0., 0., -1.], [0., 1., 0.], [-1., 0., 0.]])    # The initial rotation axises for left arm
        self.rot_r_leg_axis = np.array([[0., 0., -1.], [0., 1., 0.], [1., 0., 0.]])     # The initial rotation axises for right leg
        self.rot_l_leg_axis = np.array([[0., 0., -1.], [0., 1., 0.], [-1., 0., 0.]])    # The initial rotation axises for left leg

    def gen_vecs(self, points:np.ndarray):
        return normalize(points[self.vec_end] - points[self.vec_start])

    def gen_init_axis(self, vecs:np.ndarray):
        '''
        Generate the initial axis for each limb based on the pose data
        '''
        shoulder_x = - vecs[self.lumbarspine_v]
        r_shoulder_y, l_shoulder_y = np.cross(vecs[[self.r_shoulder_v, self.l_shoulder_v]], shoulder_x)
        r_shoulder_z, l_shoulder_z = np.cross(shoulder_x, [r_shoulder_y, l_shoulder_y])
        l_shoulder_y = - l_shoulder_y # Inverse the direction of y axis for the left side, make it left-hand coordinate
        
        hip_x = - vecs[self.lumbarspine_v]
        r_hip_y, l_hip_y = np.cross(vecs[[self.r_hipbone_v, self.l_hipbone_v]], hip_x) # The leg's y direction is the opposite of arm's
        r_hip_z, l_hip_z = np.cross(hip_x, [r_hip_y, l_hip_y])
        l_hip_y = - l_hip_y # Inverse the direction of y axis for the left side, make it left-hand coordinate
        return normalize(np.array([shoulder_x, r_shoulder_y, r_shoulder_z, shoulder_x, l_shoulder_y, l_shoulder_z, hip_x, r_hip_y, r_hip_z, hip_x, l_hip_y, l_hip_z])).reshape(4,3,3)

    def cal_limb_angle(self, upper_limb:np.ndarray, lower_limb:np.ndarray, init_axis:np.ndarray, limb_id:int):
        axis = init_axis.T
        project_vec = upper_limb - (upper_limb.dot(axis[:, 1]) * axis[:, 1])
        project_vec /= np.linalg.norm(project_vec)
        theta_0 = np.arccos(project_vec.dot(axis[:, 0]))
        theta_0_checkpoint = project_vec.dot(axis[:, 2])
        theta_1 = np.arccos(upper_limb.dot(axis[:, 1]))
        rot_axis = axis[:, 1] if limb_id % 2 == 1 else -axis[:, 1]
        R1 = Rodrigues(theta_0, rot_axis)
        axis = np.matmul(R1, axis)
        rot_axis = axis[:, 2] if limb_id % 2 == 1 else -axis[:, 2]
        R2 = Rodrigues(theta_1, rot_axis)
        axis = np.matmul(R2, axis)

        project_vec = lower_limb - (lower_limb.dot(axis[:, 1]) * axis[:, 1])
        project_vec /= np.linalg.norm(project_vec)
        theta_2 = np.arccos(project_vec.dot(axis[:, 2]))
        theta_3 = np.arccos(lower_limb.dot(axis[:, 1]))

        ret = (np.array([theta_0, theta_1, theta_2, theta_3]) * 180 / np.pi).astype(int)
        # Angle check
        ret[0] = ret[0] if theta_0_checkpoint > 0 else 0
        return ret

    def handle_pose_data(self, points:np.ndarray):
        vecs = self.gen_vecs(points)
        self.r_shoulder_axis, self.l_shoulder_axis, self.r_hip_axis, self.l_hip_axis = self.gen_init_axis(vecs)
        r_arm_angle = self.cal_limb_angle(vecs[self.r_upperarm_v], vecs[self.r_forearm_v], self.r_shoulder_axis, self.RIGHT_ARM)
        l_arm_angle = self.cal_limb_angle(vecs[self.l_upperarm_v], vecs[self.l_forearm_v], self.l_shoulder_axis, self.LEFT_ARM)
        r_hip_angle = self.cal_limb_angle(vecs[self.r_thigh_v], vecs[self.r_calfbone_v], self.r_hip_axis, self.RIGHT_LEG)
        l_hip_angle = self.cal_limb_angle(vecs[self.l_thigh_v], vecs[self.l_calfbone_v], self.l_hip_axis, self.LEFT_LEG)
        angle = np.hstack([r_arm_angle, l_arm_angle, r_hip_angle, l_hip_angle])
        if self.is_denoise:
            angle = self.servo_angle_denoise(angle)
        angle[angle >= 180] = 180
        angle[angle < 1] = 1
        self.last_angle = angle
        return self.last_angle.astype(np.uint8).copy()


    def servo_angle_denoise(self, angle_list:np.ndarray):  
        # divergence
        curr_time = time()
        # div = np.abs(self.angle_raw_history - angle_list)
        # if np.sum(div) > self.div_lim:
        #     new_angle_list = self.angle_hist[-1]
        #     np.delete(self.angle_raw_history, 0, 0)
        #     np.append(self.angle_raw_history, angle_list)
        #     np.delete(self.angle_hist, 0, 0)
        #     np.append(self.angle_hist, new_angle_list)
        #     np.delete(self.time_log, 0, 0)
        #     np.append(self.time_log, curr_time)
        #     return new_angle_list
        self.interval = curr_time - self.last_time
        self.last_time = curr_time

        velocity = (angle_list - self.last_angle) / self.interval
        # self.div = np.sum(np.abs(self.velocity_raw_history - velocity)) / self.hist_len
        self.div = np.mean(np.std(self.velocity_raw_history, axis=0))
        self.velocity_raw_history = np.vstack([self.velocity_raw_history[1:], velocity])
        if self.div <= self.div_lim:
            print(self.div)
            new_angle_list = angle_list.copy()
            v_greater = velocity > self.v_lim
            v_lower = velocity < - self.v_lim
            new_angle_list[v_greater] = self.last_angle[v_greater] + (self.v_lim[v_greater] * self.interval)
            new_angle_list[v_lower] = self.last_angle[v_lower] - (self.v_lim[v_lower] * self.interval)

            # for i in range(16):
            #     if velocity[i] > self.v_lim[i]:
            #         new_angle_list[i] = self.last_angle[i] + (self.v_lim[i] * interval)
            #     elif velocity[i] < -self.v_lim[i]:
            #         new_angle_list[i] = self.last_angle[i] - (self.v_lim[i] * interval)
            # np.delete(self.velocity_raw_history, 0, 0)
            # np.append(self.velocity_raw_history, angle_list)
            # self.last_angle = new_angle_list
            # print('%d, %d' % (new_angle_list[0], angle_list[0]))
            return new_angle_list

        return self.last_angle

    def cal_limb_vec(self, init_limb_vec:np.ndarray, limb_angles:np.ndarray, init_axis:np.ndarray, limb_id:int):
        # Transpose the limb vectors and axis vectors for the convenience of matrix multiplication
        limb_vec = init_limb_vec.T
        axis = init_axis.T
        # Calculate the rotation matrix for each servo and rotate the vectors for limb and axis
        rot_axis = axis[:, 1] if limb_id % 2 == 1 else -axis[:, 1]
        R0 = Rodrigues(limb_angles[0], rot_axis)
        limb_vec = np.matmul(R0, limb_vec) # For upper part and lower part
        axis = np.matmul(R0, axis)
        rot_axis = axis[:, 2] if limb_id % 2 == 1 else -axis[:, 2]
        R1 = Rodrigues(limb_angles[1], rot_axis)
        limb_vec = np.matmul(R1, limb_vec) # For upper part and lower part
        axis = np.matmul(R1, axis)
        rot_axis = axis[:, 1] if limb_id == self.LEFT_ARM or limb_id == self.RIGHT_LEG else -axis[:, 1]
        R2 = Rodrigues(limb_angles[2], rot_axis)
        limb_vec[:, 1] = np.matmul(R2, limb_vec)[:, 1] # For lower part only
        axis = np.matmul(R2, axis)
        rot_axis = axis[:, 0] if limb_id % 2 == 0 else -axis[:, 0]
        R3 = Rodrigues(limb_angles[3], rot_axis)
        limb_vec[:, 1] = np.matmul(R3, limb_vec)[:, 1] # For lower part only
        # Transpose the limb vectors back and return the vectors
        return limb_vec.T

    def reconstruct_pose_data(self, angles:np.ndarray):
        reform_angles = angles * np.pi / 180 # Reform the angle from degree to radian
        # Calculate the vectors for each limb
        r_arm_vec = self.cal_limb_vec(self.init_limb_vecs[[self.r_upperarm_v, self.r_forearm_v]], reform_angles[0:4], self.rot_r_arm_axis, self.RIGHT_ARM)
        l_arm_vec = self.cal_limb_vec(self.init_limb_vecs[[self.l_upperarm_v, self.l_forearm_v]], reform_angles[4:8], self.rot_l_arm_axis, self.LEFT_ARM)
        r_leg_vec = self.cal_limb_vec(self.init_limb_vecs[[self.r_thigh_v, self.r_calfbone_v]], reform_angles[8:12], self.rot_r_leg_axis, self.RIGHT_LEG)
        l_leg_vec = self.cal_limb_vec(self.init_limb_vecs[[self.l_thigh_v, self.l_calfbone_v]], reform_angles[12:16], self.rot_l_leg_axis, self.LEFT_LEG)
        denoised_pose = self.std_pose # Copy from the initial standard pose
        # Modify the points at the limbs based on the above vectors
        denoised_pose[[self.r_elbow, self.l_elbow, self.r_knee, self.l_knee]] = denoised_pose[[self.r_shoulder, self.l_shoulder, self.r_hip, self.l_hip]] + np.array([r_arm_vec[0], l_arm_vec[0], r_leg_vec[0], l_leg_vec[0]])
        denoised_pose[[self.r_wrist, self.l_wrist, self.r_ankle, self.l_ankle]] = denoised_pose[[self.r_elbow, self.l_elbow, self.r_knee, self.l_knee]] + np.array([r_arm_vec[1], l_arm_vec[1], r_leg_vec[1], l_leg_vec[1]])
        return denoised_pose