import cv2
import numpy as np

def compute_stereo_rectification_parameters():
    # 相机内参
    left_camera_matrix = np.array([[147.0830506484228, 0, 106.3834686120761],
                                   [0, 260.7685416156737, 118.5751518872908],
                                   [0, 0, 1]])
    right_camera_matrix = np.array([[147.3441774926454, 0, 90.58915159623945],
                                    [0, 261.1263542220087, 109.211853174341],
                                    [0, 0, 1]])

    # 畸变系数
    left_distortion = np.array([-0.419193409170514, 0.231173494836553, -0.011972854323690, 0.003444759451851, 0])
    right_distortion = np.array([-0.446462725561946, 0.391077256097635, -0.011193076112989, 0.003278039800043, 0])

    # 立体校正参数
    R = np.array([[0.999909159352864, -0.012787814019209, 0.004259677788077],
                  [0.012764651599512, 0.999903832967274, 0.005421114912710],
                  [-0.004328592356784, -0.005366249152233, 0.999976233046689]])
    T = np.array([[-50.22027679081481], [-0.923912290414619], [2.28431109056798]])

    size = (224, 224)
    R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(left_camera_matrix, left_distortion,
                                                right_camera_matrix, right_distortion,
                                                size, R, T)

    left_map1, left_map2 = cv2.initUndistortRectifyMap(left_camera_matrix, left_distortion, R1, P1, size, cv2.CV_16SC2)
    right_map1, right_map2 = cv2.initUndistortRectifyMap(right_camera_matrix, right_distortion, R2, P2, size, cv2.CV_16SC2)
    
    return left_map1, left_map2, right_map1, right_map2, Q
