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

### Additional Modules
```bash
pip install pandas
pip install matplotlib
```

---

## Embedding Environment Setup

Although Arduino IDE is capable for this project, its lack of auto-completion and syntax highlighting makes coding experience less enjoyable. 
To have a more pleasant coding experience, and more importantly, to write codes that are clearly structuralized and extensible to many devices 
(Arduino UNO, ESP32 board, ...), I decided to write the control code in c++ in vscode, with the help of extension **PlatformIO**.

### Install PlatformIO extension in VSCode

Search "PlatformIO" in VSCode shop and click "install" to install it. The icon of the extension looks like this:

![image](./img/platformIO.png)

### Initialize PlatformIO Workspace

PlatformIO can support the framework for many different devices, like ESP32 board and Arduino UNO. It downloads libraries for different devices and 
manages the libraries seperately. The workspace of a PlatformIO project can be setup very easily with a *platformio.ini* file. The PlatformIO will 
automatically download the libraries needed according to the *platformio.ini* file.

Click the PlatformIO icon in the toolbar on the left and then click the "**Open**" under the "**PIO Home**" section. This will open the PlatformIO 
home page. Click "**Open Project**" and select the "**arduino**" directory in this project, which contains a *platformio.ini* file. The workspace 
should be setup in a minute if it is the first time you use it.

### Compile and Upload Code

At the bottom of the VSCode, you can now see two buttons ![buttons](./img/platformio_button.png).

Click the left one to compile the code and click the right one to upload the code to the board.

## Demo
To demo the project, type

```bash
python main.py
```
