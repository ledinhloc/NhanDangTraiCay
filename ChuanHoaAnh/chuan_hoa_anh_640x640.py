import os
import cv2
import numpy as np

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class_name = 'DuaLeo'
path = os.path.join(base_dir, 'Image', class_name)
path_dest = os.path.join(base_dir, 'TraiCay640x640', class_name)
os.makedirs(path_dest, exist_ok=True)

lst_dir = os.listdir(path)
dem = 0
for filename in lst_dir:
    print(filename)
    fullname = os.path.join(path, filename)
    imgin = cv2.imread(fullname, cv2.IMREAD_COLOR)
    if imgin is None:
        print(f'Skip invalid image: {fullname}')
        continue
    # M: width, N: height, C: channel: 3
    M, N, C = imgin.shape
    if M < N:
        imgout = np.zeros((N, N, C), np.uint8) + 255
        imgout[:M, :N, :] = imgin
    elif M > N:
        imgout = np.zeros((M, M, C), np.uint8) + 255
        imgout[:M, :N, :] = imgin
    else:
        imgout = imgin.copy()
    imgout = cv2.resize(imgout, (640, 640))
    fullname_dest = os.path.join(path_dest, f'{class_name}_{dem:03d}.jpg')
    dem+=1
    cv2.imwrite(fullname_dest, imgout)
