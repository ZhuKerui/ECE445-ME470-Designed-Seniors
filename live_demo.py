from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from time import sleep, time
import gc
import os
import argparse

import cv2
import numpy as np
import torch
import torch.utils.data
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from pose_model_3d.src.lib.model import create_model
from pose_model_3d.src.lib.utils.image import get_affine_transform, transform_preds
from pose_model_3d.src.lib.utils.eval import get_preds, get_preds_3d

mean = np.array([0.485, 0.456, 0.406], np.float32).reshape(1, 1, 3)
std = np.array([0.229, 0.224, 0.225], np.float32).reshape(1, 1, 3)

class Live_Model(QThread):

  model_signal = pyqtSignal(np.ndarray)

  def __init__(self, parent:QObject=None):
    super(Live_Model, self).__init__(parent=parent)
    self.__alive = False
    self.generate_demo_opt()
    self.image = None
    self.model, _, _ = create_model(self.opt)
    self.model = self.model.to(self.opt.device)
    self.model.eval()
    self.transform_matrix = np.array([[1, 0, 0],
                                      [0, 0,-1],
                                      [0, 1, 0]])

  def stop(self):
    self.__alive = False

  def run(self):
    self.__alive = True
    while self.__alive:
      if self.image is None:
        sleep(0.01)
        continue
      # print('image received')
      # start_time = time()
      image = self.image
      self.image = None
      self.demo_image(image)
      image = None
      gc.collect()
      # print('time: %.2f' % (time()-start_time))
  def enqueue_image(self, image):
    self.image = image

  def demo_image(self, image):
    s = max(image.shape[0], image.shape[1]) * 1.0
    c = np.array([image.shape[1] / 2., image.shape[0] / 2.], dtype=np.float32)
    trans_input = get_affine_transform(c, s, 0, [self.opt.input_w, self.opt.input_h])
    inp = cv2.warpAffine(image, trans_input, (self.opt.input_w, self.opt.input_h), flags=cv2.INTER_LINEAR)
    inp = (inp / 255. - mean) / std
    inp = inp.transpose(2, 0, 1)[np.newaxis, ...].astype(np.float32)
    inp = torch.from_numpy(inp).to(self.opt.device)
    out = self.model(inp)[-1]
    pred = get_preds(out['hm'].detach().cpu().numpy())[0]
    pred = transform_preds(pred, c, s, (self.opt.output_w, self.opt.output_h))
    pred_3d = get_preds_3d(out['hm'].detach().cpu().numpy(), out['depth'].detach().cpu().numpy())[0]
    pred_3d = np.matmul(pred_3d.reshape(-1, 3), self.transform_matrix)
    pred_3d[:, :2] = - pred_3d[:, :2]
    self.model_signal.emit(pred_3d)
    
  def generate_demo_opt(self):
    parser = argparse.ArgumentParser()
    opt = parser.parse_args()
    opt.arch = 'msra_50'
    opt.dataset = 'mpii'
    opt.lr = 0.001
    opt.load_model = 'pose_model_3d/models/fusion_3d_var.pth'
    opt.gpus = [-1]
    opt.resume = False
    opt.exp_id = 'default'
    opt.debug = 0
    opt.lr_step = '90,120'
    opt.test = False
    opt.input_h = -1
    opt.input_w = -1
    opt.output_h = -1
    opt.output_w = -1
    opt.scale = -1
    opt.rotate = -1
    opt.task = 'human3d'

    opt.eps = 1e-6
    opt.momentum = 0.0
    opt.alpha = 0.99
    opt.epsilon = 1e-8
    opt.hm_gauss = 2
    opt.root_dir = os.path.join(os.path.dirname(__file__), 'pose_model_3d')
    opt.data_dir = os.path.join(opt.root_dir, 'data')
    opt.exp_dir = os.path.join(opt.root_dir, 'exp')

    opt.save_dir = os.path.join(opt.exp_dir, opt.exp_id)
    if opt.debug > 0:
      opt.num_workers = 1

    opt.lr_step = [int(i) for i in opt.lr_step.split(',')]
    if opt.test:
      opt.exp_id = opt.exp_id + 'TEST'
    opt.save_dir = os.path.join(opt.exp_dir, opt.exp_id)

    if 'hg' in opt.arch or 'posenet' in opt.arch:
      opt.num_stacks = 2
    else:
      opt.num_stacks = 1
    
    if opt.input_h == -1 and opt.input_w == -1 and \
      opt.output_h == -1 and opt.output_w == -1:
      if opt.dataset == 'coco':
        opt.input_h, opt.input_w = 256, 192
        opt.output_h, opt.output_w = 64, 48
      else:
        opt.input_h, opt.input_w = 256, 256
        opt.output_h, opt.output_w = 64, 64
    else:
      assert opt.input_h // opt.output_h == opt.input_w // opt.output_w
    
    if opt.scale == -1:
      opt.scale = 0.3 if opt.dataset == 'coco' else 0.25
    if opt.rotate == -1:
      opt.rotate = 40 if opt.dataset == 'coco' else 30

    opt.num_output = 17 if opt.dataset == 'coco' else 16
    opt.num_output_depth = opt.num_output if opt.task == 'human3d' else 0
    opt.heads = {'hm': opt.num_output}
    if opt.num_output_depth > 0:
      opt.heads['depth'] = opt.num_output_depth
    if opt.gpus[0] >= 0:
          opt.device = torch.device('cuda:{}'.format(opt.gpus[0]))
    else:
      opt.device = torch.device('cpu')
    print('heads', opt.heads)

    if opt.resume:
      opt.load_model = '{}/model_last.pth'.format(opt.save_dir)

    self.opt = opt
    
if __name__ == '__main__':
  live_model = Live_Model()

  def turn_off(para:list):
    print(para)
    live_model.stop()
    print('stop')

  live_model.model_signal.connect(turn_off)
  live_model.start()
  sleep(1)
  live_model.enqueue_image(cv2.imread('pose_model_3d/images/h36m_1818.png'))
  sleep(1)
