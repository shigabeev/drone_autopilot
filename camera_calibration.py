import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt



WAIT_TIME = 10
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('calibration_data/macbook/*.png')

for fname in images:
    img = cv2.imread(fname)
    #img_big = cv2.resize(img, (1280, 720))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # plt.figure()
    # plt.imshow(gray)
    # plt.show()

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7, 6), None, cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        print("I'm on line 32")
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(WAIT_TIME)

cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# ---------- Saving the calibration -----------------
cv_file = cv2.FileStorage("calibration_data/test.yaml", cv2.FILE_STORAGE_WRITE)
cv_file.write("camera_matrix", mtx)
cv_file.write("dist_coeff", dist)
# note you *release* you don't close() a FileStorage object
cv_file.release()