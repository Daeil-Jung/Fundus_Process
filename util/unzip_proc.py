import zipfile
import os


def unzip(filename):
    '''
    This will help you unzip file in this
    :param filename: string
    :return: None
    '''
    target_zip = zipfile.ZipFile(filename)
    target_zip.extractall(os.getcwd())
    target_zip.close()
    print(filename + "을 압축해제 하였습니다.")
