from util.unzip_proc import unzip
from util.dir_gen import dir_gen_proc
from preproc.filters import sharpening
from preproc.ch_reduction import red_ch_zeros
from preproc.flip import os_flip

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("foldername", help="Target folder name or .zip file's filename(without '.zip')", type=str)
parser.add_argument("-z", "--unzip", help="Unzip file", action="store_true")
parser.add_argument("-s", "--sharpening", help="Use when you want to do sharpening filter process", action="store_true")
parser.add_argument("-r", "--reduction_red", help="make red channel zeros", action="store_true")
args = parser.parse_args()


def main(args):
    if args.unzip:
        filename = args.foldername + ".zip"
        unzip(filename)
    if args.sharpening:
        sharpening(args.foldername)
    if args.reduction_red:
        red_ch_zeros(args.foldername)
    os_flip(args.foldername)
    dir_gen_proc(args.foldername)


if __name__ == '__main__':
    main(args)
