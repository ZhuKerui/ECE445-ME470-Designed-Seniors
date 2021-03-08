# ECE445-ME470-Designed-Seniors

> This is the senior design project for the group of **Xinyi Lai**, **Hao Hu**, **Zhi Cen** and **Kerui Zhu**.

## Requirements

> Python 3.x

## Environment Setup

### PyTorch
To run the 3D Pose Estimater, we need to install the PyTorch.

```bash
pip install torch
pip install torchvision
```

### Download Pre-trained Model
Download the [model](https://drive.google.com/file/d/1_2CCb_qsA1egT5c2s0ABuW3rQCDOLvPq) and put it in the "pose_model_3d/models"

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

## Demo
To demo the project, type

```bash
python main.py
```
