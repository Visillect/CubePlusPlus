#!/usr/bin/env python3

"""Build Cube++Small from Cube++. The simpleer dataset:
    * can be easily downloaded and used
    * but it lacks some images/information available in the full one"""

import argparse
from collections import Counter
from utils.paths import prepare_generated_dirs, get_img_ids, get_path, get_common_path
from utils.cr2_convert import numpy_average_downscale
from utils.cube_io import png16_load, png16_save, jpg_load, jpg_save
from utils.calc_gt import save_gt
from tqdm import tqdm as tqdm
from multiprocessing import Pool
import exiftool
import pandas as pd
import re
import os
import os.path as osp
import numpy as np
import shutil
import random

CROP_SX = -700  # 1892+
CROP_SY = -1000  # 728+
SCALE = 4

###############################################################################
# paths

DS_SIMPLE_FILES = {
    "png": "{simple_ds_dir}/{role}/PNG/{simple_img_id}.png",
    "jpg": "{simple_ds_dir}/auxiliary/JPG/{role}_{simple_img_id}.jpg",
}

DS_SIMPLE_COMMON_FILES = {
    "gt": "{simple_ds_dir}/{role}/gt.csv",
    "properties": "{simple_ds_dir}/auxiliary/{role}_properties.csv",
}


def get_simple_path(simple_ds_dir, role, simple_img_id, data_type):
    return DS_SIMPLE_FILES[data_type].format(
        simple_ds_dir=simple_ds_dir, role=role, simple_img_id=simple_img_id
    )


def get_simple_common_path(simple_ds_dir, role, data_type):
    return DS_SIMPLE_COMMON_FILES[data_type].format(
        simple_ds_dir=simple_ds_dir, role=role)


def prepare_dirs(simple_ds_dir):
    for role in "train", "test":
        for k in DS_SIMPLE_FILES:
            f = get_simple_path(simple_ds_dir, role, "00_0000", k)
            os.makedirs(osp.dirname(f), exist_ok=True)

        for k in DS_SIMPLE_COMMON_FILES:
            f = get_simple_common_path(simple_ds_dir, role, k)
            os.makedirs(osp.dirname(f), exist_ok=True)


def remove_and_prepare_dirs(out_dir, overwrite, read_only, verbose):
    if not overwrite and not read_only:
        assert not osp.exists(
            out_dir
        ), "Output dir {} already exists. \
            Use --overwrite to explicitly force its removing".format(
            out_dir
        )
    else:
        if overwrite and osp.exists(out_dir) and not read_only:
            if verbose:
                print("removing {}".format(out_dir))
            shutil.rmtree(out_dir)

    prepare_dirs(out_dir)


###############################################################################
# make roles

TRAIN_PROB = 0.8
RE_ID = re.compile("[0-9]{2}_[0-9]{4}")


def _get_rand_score(img_id):
    # number between 0 and 1
    assert RE_ID.match(img_id), "{} - is not correct id".format(img_id)

    rand = random.Random(img_id)
    return rand.random()


def calc_img_id_role(img_id):
    if _get_rand_score(img_id) < TRAIN_PROB:
        return "train"
    else:
        return "test"


###############################################################################


def csv_path(ds_dir):
    return osp.join(ds_dir, "list.csv")


def convert(input_path, output_path, ext, scale):
    if ext == "png":
        img_load, img_save = png16_load, png16_save
    elif ext == "jpg":
        img_load, img_save = jpg_load, jpg_save
    else:
        raise NotImplementedError()

    img = img_load(input_path)
    img[CROP_SY:, CROP_SX:, :] = 0  # mask
    img = numpy_average_downscale(img, scale)
    img_save(output_path, img)


def build_simple_ds(inp_dir, out_dir, overwrite=False, verbose=False, read_only=False):
    if out_dir is None:
        out_dir = osp.join(inp_dir, "..", "SimpleCube++")
        print("Setting out_dir as {}".format(out_dir))

    inp_gt = pd.read_csv(get_common_path(inp_dir, "gt")).set_index("image")
    inp_props = pd.read_csv(get_common_path(inp_dir, "properties")).set_index("image")

    img_ids_by_role = {
        "train": [],
        "test": [],
        "ignored (no mean gt)": [],
    }

    img_ids = get_img_ids(inp_dir)
    for ii in img_ids:
        if not inp_props.loc[ii, 'has_mean_gt']:
            role = "ignored (no mean gt)"
        else:
            role = calc_img_id_role(ii)
        img_ids_by_role[role].append(ii)

    if verbose:
        print("Images by role:")
        for k, v in img_ids_by_role.items():
            print("    {} images in {}".format(len(v), k))

    remove_and_prepare_dirs(out_dir, overwrite, read_only, verbose)

    for role in "train", "test":
        ids = img_ids_by_role[role]
        for ii in tqdm(ids, desc="processing {role} images".format(role=role)):
            for ext in "jpg", "png":
                inp_img = get_path(inp_dir, ii, ext)
                out_img = get_simple_path(out_dir, role, ii, ext)

                if not read_only:
                    convert(inp_img, out_img, ext, scale=SCALE)

        table = inp_gt.loc[ids, ["mean_r", "mean_g", "mean_b"]].rename({'mean_r': 'r', 'mean_g': 'g', 'mean_b': 'b'})
        path = get_simple_common_path(out_dir, role, "gt")
        if not read_only:
            table.sort_values("image").to_csv(path)

        table = inp_props.loc[
            ids,
            ["ds_version", "daytime", "place", "illumination", "is_sharp", "shadows"],
        ]
        path = get_simple_common_path(out_dir, role, "properties")
        if not read_only:
            table.sort_values("image").to_csv(path)


def parse_args():
    parser = argparse.ArgumentParser("Build Cube++Small from Cube++")
    parser.add_argument("inp_dir", help="cube++ dataset directory")
    parser.add_argument("--out-dir", help="dir for the generated dataset, same level as inp_dir by default")
    parser.add_argument("--overwrite", action="store_true", help="remove previous if exists")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--read-only", action="store_true", help="estimate new dataset without saving anything")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_simple_ds(
        args.inp_dir, args.out_dir, args.overwrite, args.verbose, args.read_only
    )
