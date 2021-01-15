
    # Segmentation Algorithm: Vibe
    # Created by Zhi Cen on Jan 14, 2021

import numpy as np
import cv2

class Vibe:
    def __init__(self, row=480, col=640):
        self.row = row
        self.col = col
        self.num_sam = 20
        self.min_match = 5
        self.radius = 10
        self.rand_prob = 16
        self.fore_pixel = 255
        self.back_pixel = 0
        
        self.FGCount = np.zeros((self.row, self.col))    #每个像素被检测为前景的次数
        self.FGModel = np.zeros((self.row, self.col))    #保存前景像素

        self.samples = np.zeros((self.num_sam, self.row, self.col))
        # self.samples = np.zeros((self.row, self.col, self.num_sam + 1))
        # self.off = [-1, 0, 1]
        
    def process_first_frame(self, frame):
        row, col = self.row, self.col
        randoff_xy = np.random.randint(-1,2,size=(2, self.num_sam, row, col))

        # vibe_my_numpy: xy_split
        x = np.tile(np.arange(row), (col,1)).T
        y = np.tile(np.arange(col), (row,1))
        x = np.tile(x, (self.num_sam, 1, 1)) + randoff_xy[0]
        y = np.tile(y, (self.num_sam, 1, 1)) + randoff_xy[1]

        # x[x < 0] = 0
        # y[y < 0] = 0
        # vibe_my_numpy: split_<0
        tx = x[:, 0, :]
        tx[tx < 0] = 0
        x[:, 0, :] = tx
        ty = y[:, :, 0]
        ty[ty < 0] = 0
        y[:, :, 0] = ty

        tx = x[:, -1, :]
        tx[tx >= row] = row - 1
        x[:, -1, :] = tx
        ty = y[:, :, -1]
        ty[ty >= col] = col - 1
        y[:, :, -1] = ty
        x, y = x.astype(int), y.astype(int)
        self.samples = frame[x, y]

        # vibe_my_numpy: xy_comb
        # x = np.tile(np.arange(row), (col,1)).T
        # y = np.tile(np.arange(col), (row,1))
        # x = np.tile(x, (self.num_sam, 1, 1))
        # y = np.tile(y, (self.num_sam, 1, 1))
        # xy = [x, y]
        # xy = xy + randoff_xy
        # xy[xy < 0] = 0
        # tx = xy[0, :, -1, :]
        # tx[tx >= row] = row - 1
        # xy[0, :, -1, :] = tx
        # ty = xy[1, :, :, -1]
        # ty[ty >= col] = col - 1
        # xy[1, :, :, -1] = ty
        # xy = xy.astype(int)
        # self.samples = frame[xy[0], xy[1]]

        # Baseline: code from https://blog.csdn.net/lyxleft/article/details/102499463
        # xr_=np.tile(np.arange(col),(row,1))
        # yr_=np.tile(np.arange(row),(col,1)).T
        # xyr_=np.zeros((2,self.num_sam,row,col))
        # for i in range(self.num_sam):
        #     xyr_[1,i]=xr_
        #     xyr_[0,i]=yr_
        # xyr_=xyr_+randoff_xy
        # xyr_[xyr_<0]=0
        # tpb_=xyr_[0,:,-1,:]
        # tpb_[tpb_>=row]=row-1
        # xyr_[0,:,-1,:]=tpb_
        # tpr_=xyr_[1,:,:,-1]
        # tpr_[tpr_>=col]=col-1
        # xyr_[1,:,:,-1]=tpr_
        # xyr=xyr_.astype(int)
        # self.samples=frame[xyr[0,:,:,:],xyr[1,:,:,:]]

        # Initial: written w/o numpy
        # for i in range(self.row):
        #     for j in range(self.col):
        #         for k in range(self.num_sam):
        #             rand = random.randint(0, 2) 
        #             row = i + self.off[rand]
        #             row = max(0, row)
        #             row = min(self.row-1, row)
        #             rand = random.randint(0, 2) 
        #             col = j + self.off[rand]
        #             col = max(0, col)
        #             col = min(self.col-1, col)

        #             self.samples[i][j][k] = frame[row][col]

    def run(self, frame):
        row, col = self.row, self.col
        # Baseline: code from https://blog.csdn.net/lyxleft/article/details/102499463
        dist = np.abs((self.samples.astype(float) - frame.astype(float)).astype(int))
        dist[dist < self.radius] = 1
        dist[dist >= self.radius] = 0
        matches = np.sum(dist, axis=0)
        matches = matches < self.min_match
        self.FGModel[matches] = self.back_pixel
        self.FGModel[~matches] = self.fore_pixel
        self.FGCount[matches] += 1
        self.FGCount[~matches] = 0
        fake_fore = self.FGCount > 1000000
        matches[fake_fore] = False
   
    # 1/rand_prob to update background pixel
        update_prob = np.random.randint(self.rand_prob, size=(row, col))
        update_prob[matches] = 1
        update_xy = np.where(update_prob == 0)
        update_num = update_xy[0].shape[0]
        rand_sam_pos = np.random.randint(self.num_sam, size=update_num)
        update_sxy = (rand_sam_pos, update_xy[0], update_xy[1])
        self.samples[update_sxy] = frame[update_xy]
 
    # 1/rand_prob to update bg neighbor pixel
        update_prob = np.random.randint(self.rand_prob, size=(row, col))
        update_prob[matches] = 1
        update_xy = np.where(update_prob == 0)
        update_num = update_xy[0].shape[0]
        rand_sam_pos = np.random.randint(self.num_sam, size=update_num)
        rand_off = np.random.randint(-1, 2, size=(2,update_num))
        update_nb_xy = np.stack(update_xy) + rand_off
        update_nb_xy[update_nb_xy < 0] = 0
        update_nb_xy[0][update_nb_xy[0] >= row] = row - 1
        update_nb_xy[1][update_nb_xy[1] >= col] = col - 1
        update_nb_sxy = (rand_sam_pos, update_nb_xy[0], update_nb_xy[1])
        self.samples[update_nb_sxy] = frame[update_xy]

        # Initial: written w/o numpy
        # for i in range(self.row):
        #     for j in range(self.col):
        #         match_ct = 0
        #         for k in range(self.num_sam):
        #             dist = abs(self.samples[i][j][k] - frame[i][j])
        #             if dist < self.radius:
        #                 match_ct += 1
        #                 if match_ct >= self.min_match:
        #                     break
                
        #         if match_ct >= self.min_match:
        #             self.samples[i][j][self.num_sam] = 0
        #             self.FGModel[i][j] = 0
        #         else:
        #             self.samples[i][j][self.num_sam] += 1
        #             self.FGModel[i][j] = 255

        #             if (self.samples[i][j][self.num_sam] > 50):
        #                 rand = random.randint(0, self.num_sam)
        #                 self.samples[i][j][rand] = frame[i][j]
                
        #         if match_ct >= self.min_match:
        #             rand = random.randint(0, self.rand_prob)
        #             if rand == 0:
        #                 rand = random.randint(0, self.num_sam)
        #                 self.samples[i][j][rand] = frame[i][j]
                    
        #             rand = random.randint(0, self.rand_prob)
        #             if rand == 0:
        #                 rand = random.randint(0, 2) 
        #                 row = i + self.off[rand]
        #                 row = max(0, row)
        #                 row = min(self.row-1, row)
        #                 rand = random.randint(0, 2) 
        #                 col = j + self.off[rand]
        #                 col = max(0, col)
        #                 col = min(self.col-1, col)

        #                 rand = random.randint(0, self.num_sam)
        #                 self.samples[row][col][rand] = frame[i][j]

        return self.FGModel
