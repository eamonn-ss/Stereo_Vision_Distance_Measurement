import cv2
import numpy as np
import math
from camera_params import compute_stereo_rectification_parameters

# 获取立体校正参数
left_map1, left_map2, right_map1, right_map2, Q = compute_stereo_rectification_parameters()

def apocd_process_images(frame1, frame2):
    if frame1 is None or frame2 is None:
        return "无法读取输入图像", None, None, None, None
    else:
        imgL = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        imgR = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        img1_rectified = cv2.remap(imgL, left_map1, left_map2, cv2.INTER_LINEAR)
        img2_rectified = cv2.remap(imgR, right_map1, right_map2, cv2.INTER_LINEAR)

        imageL = cv2.cvtColor(img1_rectified, cv2.COLOR_GRAY2BGR)
        imageR = cv2.cvtColor(img2_rectified, cv2.COLOR_GRAY2BGR)

        blockSize = 4
        img_channels = 3
        stereo = cv2.StereoSGBM_create(minDisparity=1,
                                       numDisparities=64,
                                       blockSize=blockSize,
                                       P1=8 * img_channels * blockSize * blockSize,
                                       P2=32 * img_channels * blockSize * blockSize,
                                       disp12MaxDiff=-1,
                                       preFilterCap=1,
                                       uniquenessRatio=10,
                                       speckleWindowSize=100,
                                       speckleRange=100,
                                       mode=cv2.STEREO_SGBM_MODE_HH)

        disparity = stereo.compute(img1_rectified, img2_rectified).astype(np.float32) / 16.0

        disp = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        dis_color = cv2.applyColorMap(disp, cv2.COLORMAP_JET)

        threeD = cv2.reprojectImageTo3D(disparity, Q, handleMissingValues=True)
        
        # 过滤掉无效的三维点
        mask = (threeD[:,:,2] < 10000) & (threeD[:,:,2] > 0)
        threeD[~mask] = float('inf')

        # 自动检测突出物体的中心
        _, thresh = cv2.threshold(disp, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # 找到最大轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M['m00'] != 0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])
                
                # 获取该点的三维坐标
                X, Y, Z = threeD[cY, cX]
                if np.isfinite([X, Y, Z]).all():
                    distance = math.sqrt(X**2 + Y**2 + Z**2) / 1000.0  # 转换为米
                    return (f"自动选择点的像素坐标: x = {cX}, y = {cY}", 
                            (X, Y, Z), 
                            distance, 
                            dis_color, 
                            disp)
                else:
                    return "检测到无效的三维坐标", None, None, None, None
            else:
                return "无法找到有效的中心点", None, None, None, None
        else:
            return "无法找到轮廓", None, None, None, None
