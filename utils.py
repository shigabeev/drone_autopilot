import cv2
from cv2 import aruco

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


######
# Everything below is a template code
#####


def translate(drone_tvec, drone_rvec, marker_tvec, marker_rvec):
    """
    Translates coordinates of a found marker into global ones with respect to postition of a drone
    input: (x, y, z) - tvec of a drone
           (pitch, yaw, roll) - rvec of a drone

    """
    return x, y, z

def store(i, x, y, z, db_connection):
    success = db_connection.store({"id":i, "x":x, "y":y, "z":z})
    return success

def process_markers(drone_tvec, drone_rvec, corners, ids, revcs, tvecs):
    valid_ids = set()
    for i, c, rvec, tvec in zip(ids, corners, revc, tvec):
        if i in valid_ids:
            x, y, z = translate(drone_tvec, drone_rvec, tvec, rvec)
            store(i, x, y, z)


