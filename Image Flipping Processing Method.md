# jetcam-双目摄像头图像倒置问题

## 图像倒置

- 进入jetcam.py文件找到def _gst_str(self)函数。将nvvidconv 替换为nvvidconv flip-method=2
即将以下代码替"def _gst_str(self):
        return 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.capture_device, self.capture_width, self.capture_height, self.capture_fps, self.width, self.height)"
替换为"def _gst_str(self):
        return 'nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 ! nvvidconv flip-method=2 ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (
                self.capture_device, self.capture_width, self.capture_height, self.capture_fps, self.width, self.height)"
- 将修改好的文件保存，然后将其卸载重装，让修改有效，具体代码如下

- `sudo pip3 uninstall jetcam`,

- `cd jetcam`,

- `sudo python3 setup.py install`
