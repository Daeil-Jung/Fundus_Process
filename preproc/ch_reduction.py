import glob
import cv2
import numpy as np


def red_ch_zeros(foldername):
    '''
    Drop red channel.
    :param foldername: string
    :return: None
    '''
    dir_name = foldername + "/*"
    image_files_list = list(glob.glob(dir_name))

    for image_file in image_files_list:
        src = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
        src[:, :, 2] = np.zeros([src.shape[0], src.shape[1]])
        # save image
        cv2.imwrite(image_file, src)

    print("모든 이미지에 대하여 Red channel Zeros 를 적용하였습니다.")
