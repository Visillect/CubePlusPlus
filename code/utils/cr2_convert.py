#!/usr/bin/env python3
import argparse
import os
import os.path as osp
import numpy as np 
import subprocess
from utils.cube_io import tiff16_load, png16_save, jpg_load, jpg_save

SHIFT = [10, 4]
SIZE = [5184, 3456] 


def numpy_average_downscale(image, s): 
    assert image.shape[0] % s == 0
    assert image.shape[1] % s == 0
    imgs = []
    for i in range(s):
        for j in range(s):
            imgs.append(image[i::s, j::s])
    
    res = np.mean(imgs, axis=0).astype(image.dtype)
    return res


def default_crop(img): 
    return img[
        SHIFT[1]: SHIFT[1] + SIZE[1], # height
        SHIFT[0]: SHIFT[0] + SIZE[0], # width
    ]


def process_jpg(inp_path, out_path, std_size):
    """ Process ([crop + downscale]) jpg view image
    Args: 
        inp_path(str): path of 8-bit .tiff image
        out_path(str): path for 8-bit .jpg image
        std_size(bool): crop+downscale to a standart size
    """
    img = jpg_load(inp_path)
    if std_size:
        img = default_crop(img)
        img = numpy_average_downscale(img, 2)
    jpg_save(out_path, img)
    

def process_png(inp_path, out_path, std_size):
    """ Process (debayer + [crop]) raw image
    Args: 
        inp_path(str): path of 16-bit .tiff image
        out_path(str): path for 16-bit .png image
        std_size(bool): crop to a standart size
    """

    img = tiff16_load(inp_path)
    if std_size:
        img = default_crop(img)

    s0 = img.shape[0] - (img.shape[0] % 2)
    s1 = img.shape[1] - (img.shape[1] % 2)
    img = img[:s0, :s1, ...]

    r = img[::2, ::2]
    b = img[1::2, 1::2]
    g = (img[1::2, ::2] + img[::2, 1::2]) // 2  # img < 2**14 < 2**16/2
    
    debayer = np.dstack([r, g, b])
    png16_save(out_path, debayer)


def cr2_convert(input_path, output_path, raw_png_mode, dcraw_size=False, save_tmp_file=False): 
    assert(input_path.lower().endswith('.cr2'))
    assert(osp.exists(input_path))
    if raw_png_mode: 
        # raw(.CR2) -> raw(.tiff)
        assert output_path.lower().endswith('.png')
        command = 'dcraw -D -4 -T {}'.format(input_path)
    else: 
        # raw(.CR2) -> sRGB
        assert output_path.lower().endswith('.jpg'), 'DS contains raw-pngs and view-jpgs, other formats are disabled for simplicity'
        command = 'dcraw -T {}'.format(input_path)
    
    process = subprocess.run(command, shell=True, check=True)
    tiff_path = input_path[:-len('.cr2')] + '.tiff'
        
    if raw_png_mode:
        process_png(tiff_path, output_path, not dcraw_size)
    else: 
        process_jpg(tiff_path, output_path, not dcraw_size)

    if not save_tmp_file:
        os.remove(tiff_path)


def parse_args():
    parser = argparse.ArgumentParser("Generate png (14-bit debayered raw) / jpg (sRGB view)")
    parser.add_argument('input_path', help='cube_plus dir')
    parser.add_argument('output_path', help='cube_plus dir')
    parser.add_argument('--raw_png_mode', action='store_true', help='Raw image mode (14-bit debayered)')
    parser.add_argument('--dcraw_size', action='store_true', help='Change the size to the dataset value (2592x1728) or use dcraw(+debayer) defaults')
    parser.add_argument('--save_tmp_file', action='store_true', help='Not remove temporary .tiff files in cr2 directory')
    return parser.parse_args()


if __name__ == "__main__":
    cr2_convert(**vars(parse_args()))
