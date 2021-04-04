import numpy as np
import cv2


def normalize(vecs:np.ndarray):
    norm = np.linalg.norm(vecs, axis=1, keepdims=True)
    norm[norm==0]=1
    return vecs / norm

def Rodrigues(theta:float, k:np.ndarray):
    k_ = normalize(k.reshape((-1, 3))) * theta
    return cv2.Rodrigues(k_)[0]