from __future__ import print_function

import cv2
import utils
from cv2 import aruco


camera_matrix, dist_coef = utils.read_camera_profile("calibration_data/logitech_webcam.yaml")

def aruco_routine(img, drone_tvec, drone_rvec):
    valid_ids = set(range(250))
    corners, ids, rvecs, tvecs = utils.find_markers(img, camera_matrix, dist_coef) #3d
    print(len(corners))
    aruc3d = frame.copy()
    if len(corners) > 0:
        utils.process_markers(drone_tvec, drone_rvec, corners, ids, rvecs, tvecs, valid_ids) #store
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, 0.33, camera_matrix, dist_coef)

        # Draw it
        for rvecs, tvecs in zip(rvec, tvec):
            aruco.drawAxis(aruc3d, camera_matrix, dist_coef, rvecs, tvecs, 0.33)
    
    cv2.imwrite("detection.jpg", aruc3d)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    aruco_routine(gray, [0., 0., 0.], [0., 0., 0.])
    
cv2.destroyAllWindows()
cap.release()