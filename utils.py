import cv2
from cv2 import aruco

import coordinate_transforms as ct

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
parameters =  aruco.DetectorParameters_create()

def read_camera_profile(path):
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("camera_matrix").mat()
    dist_coef = cv_file.getNode("dist_coeff").mat()
    return camera_matrix, dist_coef

def find_markers(gray, camera_matrix, dist_coef, marker_size = 0.33):
    # input is a GRAY FRAME
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    rvecs, tvecs = [], []
    if len(corners) > 0:
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, dist_coef)
        
    return corners, ids, rvecs, tvecs

def store(i, x, y, z):
    #success = db_connection.store({"id":i, "x":x, "y":y, "z":z})
    with open("db.csv", "a") as fs:
        fs.write(f"\n{i},{x},{y},{z}")
    return {'success':True}

def process_markers(drone_tvec, drone_rvec, corners, ids, rvecs, tvecs):
    valid_ids = set()
    for i, c, rvec, tvec in zip(ids, corners, rvecs, tvecs):
        if i in valid_ids:
            x, y, z = ct.transform(tvec, rvec, drone_tvec, drone_rvec)[0].squeeze()
            store(i, x, y, z)


