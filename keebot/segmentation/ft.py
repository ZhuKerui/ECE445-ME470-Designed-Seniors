 
    # Use fourier transform to find edge
    # Created by Zhi Cen on Jan 16, 2021

import numpy as np
import cv2

class FT:
    def __init__(self, rows = 480, cols = 640):
        self.rows = rows
        self.cols = cols

    def low_pass(self, gray_img):
        # 从频率域转换回空间域（并使用低通滤波）
        # uint8转换为float32
        img_float32 = np.float32(gray_img)
        # 傅里叶转换为复数
        dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
        # 将低频从左上角转换到中心
        dft_shift = np.fft.fftshift(dft)

        # 在这里进行低通滤波
        rows, cols = self.rows, self.cols
        c_row, c_col = int(rows / 2), int(cols / 2)
        mask_low = np.zeros_like(dft_shift, np.uint8)
        mask_low[c_row - 30:c_row + 30, c_col - 50:c_col + 50] = 1
        # 使用低通滤波
        fshift_low = dft_shift * mask_low
        # 转换为可以显示的图片（fshift_low），fshift_low中包含实部和虚部
        magnitude_spectrum_low = 20 * np.log(cv2.magnitude(fshift_low[:, :, 0], fshift_low[:, :, 1]))

        f_ishift_low = np.fft.ifftshift(fshift_low)
        img_back_low = cv2.idft(f_ishift_low)
        img_back_low = cv2.magnitude(img_back_low[:, :, 0], img_back_low[:, :, 1])
        
        return img_back_low
    
    def high_pass(self, gray_img):
        # 从频率域转换回空间域（并使用高通滤波）
        # uint8转换为float32
        img_float32 = np.float32(gray_img)
        # 傅里叶转换为复数
        dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
        # 将低频从左上角转换到中心
        dft_shift = np.fft.fftshift(dft)

        # 在这里进行高通滤波
        rows, cols = self.rows, self.cols
        c_row, c_col = int(rows / 2), int(cols / 2)
        mask_high = np.ones_like(dft_shift, np.uint8)
        mask_high[c_row - 5:c_row + 5, c_col - 10:c_col + 10] = 0
        # 使用高通滤波
        fshift_high = dft_shift * mask_high
        # 转换为可以显示的图片（fshift_high），fshift_high中包含实部和虚部
        magnitude_spectrum_high = 20 * np.log(cv2.magnitude(fshift_high[:, :, 0], fshift_high[:, :, 1]))

        f_ishift_high = np.fft.ifftshift(fshift_high)
        img_back_high = cv2.idft(f_ishift_high)
        img_back_high = cv2.magnitude(img_back_high[:, :, 0], img_back_high[:, :, 1])

        return img_back_high

    def fft(self, gray_img):
        rows, cols = self.rows, self.cols
        #快速傅里叶变换，输出复数
        imgPadded = np.zeros((rows, cols), np.float32)  # 填充
        imgPadded[:rows, :cols] = gray_img
        fft_img = cv2.dft(imgPadded, flags=cv2.DFT_COMPLEX_OUTPUT)
        return fft_img

    def fft_reverse(self, fft_img):
        rows, cols = self.rows, self.cols
        #快速傅里叶逆变换，只输出实数部分
        ifft_img = cv2.dft(fft_img, flags=cv2.DFT_REAL_OUTPUT+cv2.DFT_INVERSE+cv2.DFT_SCALE)
        ori_img = np.copy(ifft_img[:rows, :cols])  # 裁剪
        new_gray_img = ori_img.astype(np.uint8)
        return new_gray_img