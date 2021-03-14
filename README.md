# ECE445-ME470-Designed-Seniors

> This is the senior design project for the group of **Xinyi Lai**, **Hao Hu**, **Zhi Cen** and **Kerui Zhu**.

## Requirements

> Python 3.x

## Download Pre-trained Model
Download the [model](https://drive.google.com/file/d/1_2CCb_qsA1egT5c2s0ABuW3rQCDOLvPq) and put it in the "pose_model_3d/models"

## Python Environment Setup

For simple setup, just use the following command:
```bash
pip install -r requirements.txt
```
and then you are ready to go. If you want to have a clear understanding of the use of the installed libraries, please read the following.

**If you meet a problem with opencv-python, please uninstall the opencv-python and try the command in the Opencv-python section.**

### PyTorch
To run the 3D Pose Estimater, we need to install the PyTorch.

```bash
pip install torch
pip install torchvision
```

### pyqt5
For a good user experience and a clear control flow, our project is wrapped up by a GUI application. The GUI method we use is pyqt5, since it supports the powerful QT5 and provides python bindings for higher design efficiency.

```bash
pip install pyqt5
pip install pyqt5-tools
pip install pyqtgraph
pip install pyOpenGL
```

### Opencv-python
To read the camera input, we use the opencv-python library, which is a python bindings for opencv.

```bash
pip install --no-binary opencv-python opencv-python
```

### BLE module
```bash
pip install pexpect
pip install pygatt
```

## Demo
To demo the project, type

```bash
python main.py
```
