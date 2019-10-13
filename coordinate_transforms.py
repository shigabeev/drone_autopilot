
import numpy as np
import math

def positionVectorToTranslationMatrix(vec):
    ret = [
        [1, 0, 0, vec[0]],
        [0, 1, 0, vec[1]],
        [0, 0, 1, vec[2]],
        [0, 0, 0, 1]  
    ]
    return ret

# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta):
    """

    """
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))
 
    return R

def localToGlobal(local_pos, local_rot):
    """
    Globals are always 0
    """
    worldCoordToLocal = positionVectorToTranslationMatrix(local_pos)
    worldCoordToLocal = np.linalg.inv(worldCoordToLocal) 
    localCoordToWorld = np.linalg.inv(worldCoordToLocal)

    worldRotToLocal = eulerAnglesToRotationMatrix(local_rot)
    rot = np.linalg.inv(worldRotToLocal)

    localRotToWorld = np.array([
      [
        [rot[0][0], rot[0][1], rot[0][2], 0],
        [rot[1][0], rot[1][1], rot[1][2], 0],
        [rot[2][0], rot[2][1], rot[2][2], 0],
        [0, 0, 0, 1]
      ],
    ])

    return localCoordToWorld.dot(localRotToWorld)
    #  return localRotToWorld.dot(localCoordToWorld)

def transform(tvec1, rvec1, tvec2, rvec2):
    """
    Transforms location of objects in tvec1 into their global location with respect to tvec2
    local coordinates - tvec2, rvec2
    rotation won't work
    """
    op = localToGlobal(np.squeeze(tvec2), np.squeeze(rvec2))
    tvec3 = []
    for tvec in tvec1:
        #tvec = tvec.squeeze()
        tvec3.append(np.matmul(op, tvec))
    tvec3 = np.array(tvec3)
    return tvec3


if __name__ == "__main__":
    # Demo
    
    # local_pos = np.array([1, 1, 1])
    # local_rot = np.array([0, 0.0, 0.0])


    # vec = np.array([1, 1, 2, 1])
    # op = localToGlobal()
    # res = np.matmul(op, vec)

    rvec = np.array([[[ 4.92864772e-02,  2.62773048e+00, -1.81148253e+00]],

       [[-4.30564033e-02, -2.58801317e+00,  1.74977545e+00]],

       [[-3.80904810e-02, -2.57119067e+00,  1.75401830e+00]],

       [[ 5.77575526e-02, -2.54445780e+00,  1.77728444e+00]],

       [[-6.30371617e-02,  2.61509411e+00, -1.80731513e+00]],

       [[-1.81466338e-02,  2.59730378e+00, -1.81298288e+00]],

       [[-4.56411086e-02,  2.60945600e+00, -1.82681086e+00]],

       [[ 7.99255714e-03, -2.56875853e+00,  1.81007717e+00]],

       [[-4.55645480e-02, -2.61464372e+00,  1.77534114e+00]],

       [[-3.03226304e-03, -2.57964304e+00,  1.77964242e+00]],

       [[-8.10370184e-02,  2.60133450e+00, -1.81843120e+00]],

       [[-6.89706730e-03, -2.57058630e+00,  1.77395959e+00]],

       [[-2.13853104e-01,  7.83218334e+00, -5.31295137e+00]]])

    tvec = np.array([[[-0.94786715,  0.40177878,  2.97766469]],

       [[-1.00027552, -0.33699278,  4.89468613]],

       [[-0.98205601, -0.72841617,  5.69677846]],

       [[ 1.12030107, -1.05462115,  5.99229414]],

       [[ 1.08052332, -0.33800979,  4.33679387]],

       [[ 0.08583185, -0.70225094,  5.34312036]],

       [[ 1.11309504, -0.70130298,  5.20555559]],

       [[ 0.05592615,  0.38421448,  2.87788171]],

       [[-1.01230305,  0.04430789,  4.07937178]],

       [[ 0.06027309,  0.02254106,  3.69040468]],

       [[ 1.05770385,  0.02025311,  3.50334092]],

       [[ 0.06999761, -0.33850242,  4.519224  ]],

       [[ 1.16796685, -1.79370261,  7.71997869]]])

    drone_tvec = np.array([[2., 0., 0.]])
    drone_rvec = np.array([[0., 0., 0.]])

    transform(tvec, rvec, drone_tvec, drone_rvec)