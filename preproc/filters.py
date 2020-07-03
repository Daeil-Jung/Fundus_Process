import cv2
import numpy as np
import glob


def sharpening(foldername):
    '''
    Do sharpening filter
    :param foldername: string
    :return: None
    '''
    dir_name = foldername + "/*"
    image_files_list = list(glob.glob(dir_name))

    sharpening = np.array([[-1, -1, -1, -1, -1],
                           [-1, 2, 2, 2, -1],
                           [-1, 2, 9, 2, -1],
                           [-1, 2, 2, 2, -1],
                           [-1, -1, -1, -1, -1]]) / 9.0

    for image_file in image_files_list:
        src = cv2.imread(image_file)
        src = cv2.filter2D(src, -1, sharpening)
        # save image
        cv2.imwrite(image_file, src)

    print("모든 이미지에 대하여 Sharpening filter를 적용하였습니다.")
