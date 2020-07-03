from PIL import Image
import glob


def os_flip(foldername):
    '''
    Flip left right for OS image
    :param foldername: string
    :return: None
    '''
    dir_name = foldername + "/*"

    image_files_list = list(glob.glob('Fundus/*'))

    # OS image flip algorithm
    for image_file in image_files_list:
        if image_file.split("/")[-1].split("_")[1] == "OS":
            im = Image.open(image_file)
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
            im.save(image_file)

    print("모든 OS 이미지에 대하여 flip left right를 적용하였습니다.")
