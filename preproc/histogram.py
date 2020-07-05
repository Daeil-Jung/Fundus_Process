import cv2
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
        img = cv2.imread(image_file)
        img_y_cr_cb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(img_y_cr_cb)
        y_eq = cv2.equalizeHist(y)
        img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
        img_rgb_eq = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCR_CB2BGR)
        cv2.imwrite(image_file, img_rgb_eq)

    print("모든 이미지에 대하여 histogram equalization을 적용하였습니다.")
