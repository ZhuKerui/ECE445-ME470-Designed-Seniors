# FROM python:3.9.2-buster
FROM ubuntu
ENV PYTHONUNBUFFERED 1
RUN mkdir /keebot_workspace
WORKDIR /keebot_workspace
RUN apt-get update
# RUN apt-get install build-essential -y
# RUN apt-get install libglib2.0-dev -y
# RUN apt-get install libbluetooth-dev -y
RUN apt-get install python3 python3-pip -y
RUN pip3 install torch torchvision pyqt5-tools pyqt5 pyqtgraph pyOpenGL pygatt -i https://pypi.mirrors.ustc.edu.cn/simple/
RUN pip3 install --no-binary opencv-python opencv-python -i https://pypi.mirrors.ustc.edu.cn/simple/
