#!/usr/bin/env python3

"""Building Cube++ dataset from source (CR2 and JSON files)"""

import argparse
from collections import Counter
from utils.paths import prepare_generated_dirs, get_img_ids, get_path, get_common_path
from utils.cr2_convert import cr2_convert
from utils.cube_io import json_load, json_save
from utils.calc_gt import save_gt
from tqdm import tqdm as tqdm
from multiprocessing import Pool, cpu_count
import exiftool
import pandas as pd


class ProcessImg(): 
    def __init__(self, ds_dir): 
        self.ds_dir = ds_dir

    def process(self, img_id): 
        def path(data_type): 
            return get_path(self.ds_dir, img_id, data_type)

        cr2_convert(path('CR2'), path('jpg'), raw_png_mode=False)
        cr2_convert(path('CR2'), path('png'), raw_png_mode=True)
        save_gt(path('png'), path('json_markup'), path('json_gt'))


def extract_exifs(ds_dir, img_ids):
    files = [get_path(ds_dir, img_id, 'CR2') for img_id in img_ids]
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(files)
    for m, f, img_id in zip(metadata, files, img_ids): 
        assert m['SourceFile'] == f
        json_save(get_path(ds_dir, img_id, 'json_exif'), m)


def join_gt_info(ds_dir, img_ids):
    rows = []
    keys = ['mean', 'left', 'right', 'left_white', 'right_white']

    for img_id in img_ids:
        json_gt = json_load(get_path(ds_dir, img_id, 'json_gt'))
        row = {'image': img_id}
        for key in keys:
            for i, c in enumerate('rgb'):
                row['{}_{}'.format(key, c)] = json_gt[key][i]
    
        rows.append(row)
        
    res = pd.DataFrame(rows, columns=['image', 'mean_r', 'mean_g', 'mean_b', 'left_r', 'left_g', 'left_b', 'right_r', 'right_g', 'right_b', 'left_white_r', 'left_white_g', 'left_white_b', 'right_white_r', 'right_white_g', 'right_white_b'])
    path = get_common_path(ds_dir, 'gt')
    res.sort_values('image').to_csv(path, index=False)


def join_meta_info(ds_dir, img_ids): 
    rows = []
    gt_keys = ['has_mean_gt', 'left_tr_illuminance', 'right_tr_illuminance', 'left_white_tr_illuminance', 'right_white_tr_illuminance',]
    markup_keys = ['ds_version', 'left_white_overexposed', 'right_white_overexposed']
    markup_properties_keys = ['daytime', 'place', 'illumination', 'is_sharp', 'shadows', 'richness', 'has_known_objects', 'light_objects']  # and 'estimation', moved for sorting purposes
    exif_keys = ['MakerNotes:InternalSerialNumber', 'EXIF:ISO', 'EXIF:ApertureValue', 'EXIF:ExposureTime', 'MakerNotes:PerChannelBlackLevel', 'MakerNotes:NormalWhiteLevel', 'EXIF:Model', 'MakerNotes:LensModel']
    
    for img_id in img_ids:
        row = {
            'image': img_id,
        }

        json_gt = json_load(get_path(ds_dir, img_id, 'json_gt'))
        for k in gt_keys:
            row[k] = json_gt[k]

        json_markup = json_load(get_path(ds_dir, img_id, 'json_markup'))
        for k in markup_keys: 
            value = json_markup[k]
            row[k] = str(value)  
        for k in ['estimation'] + markup_properties_keys:
            value = json_markup['properties'][k]
            row[k] = str(value)  # str for 'light_objects', which value is not str but list

        json_exif = json_load(get_path(ds_dir, img_id, 'json_exif'))
        for k in exif_keys: 
            row[k] = json_exif[k]

        
        rows.append(row)
    
    res = pd.DataFrame(
        rows, 
        columns = ['image', 'estimation'] + markup_keys + gt_keys + markup_properties_keys + exif_keys
        )
    
    path = get_common_path(ds_dir, 'properties')
    res.sort_values('image').to_csv(path, index=False)


def join_camera_estimation_info(ds_dir, img_ids): 
    rows = []
    exif_keys = ['Composite:BlueBalance', 'Composite:RedBalance', 'Composite:LightValue', 'MakerNotes:ColorTempMeasured', 'MakerNotes:ColorTempAsShot']
    
    for img_id in img_ids:
        row = {
            'image': img_id,
        }

        json_exif = json_load(get_path(ds_dir, img_id, 'json_exif'))
        for k in exif_keys: 
            row[k] = json_exif[k]
        
        rows.append(row)
    
    res = pd.DataFrame(
        rows, 
        columns = ['image'] + exif_keys
        )
    
    path = get_common_path(ds_dir, 'cam_estimation')
    res.sort_values('image').to_csv(path, index=False)


def calc_exif_statistics(ds_dir, img_ids): 
    """Calculates some extra statistics about exifs, not used in the main ds part"""
    feature_vals = {}
    for img_id in img_ids: 
        exif = json_load(get_path(ds_dir, img_id, 'json_exif'))
        for f, v in exif.items(): 
            if f not in feature_vals:
                feature_vals[f] = []
            feature_vals[f].append(v)
    
    rows = []
    for f in sorted(feature_vals.keys()):     
        vals = feature_vals[f]
        row = {
            'feature': f,
            'vals_count': len(vals),
            'uniq_vals_count': len(set(vals)),
        }
        counter = Counter(vals)
        MAX_LENGTH = 3
        for i, (v, _) in enumerate(counter.most_common(MAX_LENGTH)):
            row['top_{}_common_value'.format(i+1)] = v
        rows.append(row)

    res = pd.DataFrame(rows, columns=['feature', 'vals_count', 'uniq_vals_count', 'top_1_common_value', 'top_2_common_value', 'top_3_common_value'])
    path = get_common_path(ds_dir, 'exif_stat')
    res.sort_values('feature').to_csv(path, index=False)


def build_ds(ds_dir, overwrite, jobs): 
    img_ids = get_img_ids(ds_dir)
    assert len(img_ids) > 0, 'No images, is ds_dir correct?'

    # process all imgs
    prepare_generated_dirs(ds_dir, overwrite)
    img_processor = ProcessImg(ds_dir)
    with Pool(jobs) as p:
        list(tqdm(p.imap(img_processor.process, img_ids), total=len(img_ids), desc='processing ds files'))
    extract_exifs(ds_dir, img_ids)

    # aggregate imgs info to csvs
    join_gt_info(ds_dir, img_ids)
    join_meta_info(ds_dir, img_ids)
    calc_exif_statistics(ds_dir, img_ids)
    join_camera_estimation_info(ds_dir, img_ids)


def parse_args():
    parser = argparse.ArgumentParser("Building Cube++ dataset from source (CR2 and JSON files)")
    parser.add_argument('ds_dir', help='cube_plus_plus home dir')
    parser.add_argument('--overwrite', action='store_true', help='remove previous if exists')
    parser.add_argument('-j', '--jobs', default=max(1, cpu_count()-1), type=int, help='parallel threads count')
    return parser.parse_args()

[]
if __name__ == "__main__":
    build_ds(**vars(parse_args()))
