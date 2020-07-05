import glob
import shutil
import os
import pandas as pd

csv_data = pd.read_csv("DBdata.csv")


def dir_gen_proc(foldername):
    '''
    Generate directories and split train, test dataset.
    :param foldername: string
    :return: None
    '''
    dir_name = foldername + os.sep + "*"
    image_files_list = list(glob.glob(dir_name))

    train_dir = "Fundus" + os.sep + "train"
    test_dir = "Fundus" + os.sep + "test"

    if not (os.path.isdir(test_dir)):
        os.makedirs(test_dir)
    if not (os.path.isdir(train_dir)):
        os.makedirs(train_dir)

    # split train_test
    train_files_list = image_files_list[:int(0.7 * len(image_files_list))]
    test_files_list = image_files_list[int(0.7 * len(image_files_list)):]

    for train_file in train_files_list:
        shutil.move(train_file, os.path.join(train_dir, train_file.split(os.sep)[-1]))
    for test_file in test_files_list:
        shutil.move(test_file, os.path.join(test_dir, test_file.split(os.sep)[-1]))

    # test files classified with label
    test_files_list = list(glob.glob(os.path.join(test_dir, "*")))

    if not (os.path.isdir(os.path.join(test_dir, "Glaucoma"))):
        os.makedirs(os.path.join(test_dir, "Glaucoma"))
    if not (os.path.isdir(os.path.join(test_dir, "Normal"))):
        os.makedirs(os.path.join(test_dir, "Normal"))

    for test_file in test_files_list:
        label = get_label(test_file)
        if label == 1:
            shutil.move(test_file, os.path.join(test_dir, "Glaucoma", test_file.split(os.sep)[-1]))
        else:
            shutil.move(test_file, os.path.join(test_dir, "Normal", test_file.split(os.sep)[-1]))

    # train files classified with label
    train_files_list = list(glob.glob(os.path.join(train_dir, "*")))

    if not (os.path.isdir(os.path.join(train_dir, "Glaucoma"))):
        os.makedirs(os.path.join(train_dir, "Glaucoma"))
    if not (os.path.isdir(os.path.join(train_dir, "Normal"))):
        os.makedirs(os.path.join(train_dir, "Normal"))

    for train_file in train_files_list:
        label = get_label(train_file)
        if label == 1:
            shutil.move(train_file, os.path.join(train_dir, "Glaucoma", train_file.split(os.sep)[-1]))
        else:
            shutil.move(train_file, os.path.join(train_dir, "Normal", train_file.split(os.sep)[-1]))

    print("딥러닝에 적합한 디렉토리 생성 및 구분이 완료되었습니다.")


def get_label(file_path):
    '''
    Get label from csv file
    :param file_path: string
    :return: 0 or 1, file's label
    '''

    # split filepath to get filename
    file_name = file_path.split(os.sep)[-1]
    # get id, OSOD
    id = int(file_name.split("_")[0][1:])
    osod = file_name.split("_")[1]
    # check id and OSOD in csv_data
    target_row = csv_data[
        (csv_data["study_id"] == id) & (csv_data["OSOD"] == osod) & (csv_data["organization"] == "DKU")]
    # The second to last is the class-directory
    ret_val = target_row["label"].tolist()
    try:
        ret_val = ret_val.pop()
    except:
        ret_val = 0
    return ret_val
