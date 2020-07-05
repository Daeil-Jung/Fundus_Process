import cv2
import numpy as np
import glob, os

def hist_equalize(foldername):
    '''
    Do histogram equalization in target foldername
    :param foldername: string
    :return: None
    '''
    dir_name = foldername + os.sep + "*"
    image_files_list = list(glob.glob(dir_name))

    for image_file in image_files_list:
        if image_file.split(os.sep)[-1].split("_")[1] == "OS":
            img = cv2.imread(image_file)
            img2 = cv2.equalizeHist(img)
            cv2.imwrite(image_file, img2)

    print("모든 이미지에 대하여 histogram equalization을 적용하였습니다.")
