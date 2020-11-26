import os
import os.path as osp
import glob
import shutil

DS_FILES = {
    'CR2':          '{ds_dir}/auxiliary/source/CR2/{img_id}.CR2',
    'json_markup':  '{ds_dir}/auxiliary/source/JPG.JSON/{img_id}.jpg.json',
    'json_exif':    '{ds_dir}/auxiliary/extra/exif/{img_id}.json',
    'json_gt':      '{ds_dir}/auxiliary/extra/gt_json/{img_id}.json',
    'png':          '{ds_dir}/PNG/{img_id}.png',
    'jpg':          '{ds_dir}/JPG/{img_id}.jpg',
}

DS_COMMON_FILES = {
    'gt':               '{ds_dir}/gt.csv',
    'properties':       '{ds_dir}/properties.csv',
    'cam_estimation':   '{ds_dir}/auxiliary/extra/cam_estimation.csv',
    'exif_stat':        '{ds_dir}/auxiliary/extra/exif_stat.csv',
}


def get_path(ds_dir, img_id, data_type):
    if data_type not in DS_FILES: 
        raise KeyError('{} (Available keys: {}'.format(data_type, str(DS_FILES.keys())))

    return DS_FILES[data_type].format(
        ds_dir=ds_dir,
        img_id=img_id,
    )


def get_common_path(ds_dir, data_type): 
    if data_type not in DS_COMMON_FILES: 
        raise KeyError('{} (Available keys: {}'.format(data_type, str(DS_COMMON_FILES.keys())))

    return DS_COMMON_FILES[data_type].format(
        ds_dir=ds_dir
    )


def prepare_generated_dirs(ds_dir, overwrite=False): 
    for path in [
        '{ds_dir}/auxiliary/extra/exif',
        '{ds_dir}/auxiliary/extra/gt_json',
        '{ds_dir}/PNG',
        '{ds_dir}/JPG',
    ]: 
        path = path.format(ds_dir=ds_dir)
        if overwrite and osp.exists(path): 
            shutil.rmtree(path)
        assert not osp.exists(path), 'Error! DS dirs (for example, {}) already exist. \nUse --overwrite to explicitly force its removing'.format(path)
        os.makedirs(path)
    
    for path in [
        '{ds_dir}/gt.csv',
        '{ds_dir}/properties.csv',
        '{ds_dir}/auxiliary/extra/cam_estimation.csv',
        '{ds_dir}/auxiliary/extra/exif_stat.csv',
    ]:
        path = path.format(ds_dir=ds_dir)
        if overwrite and osp.exists(path): 
            os.remove(path)
        assert not osp.exists(path), 'Error! File {} already exists. \nUse --overwrite to explicitly force its removing'.format(path)


def get_img_ids(ds_dir): 
    json_jpg_files = glob.glob(DS_FILES['json_markup'].format(
        ds_dir=ds_dir, 
        img_id='*')
    )

    def _img_id(path): 
        return osp.basename(path).split('.')[0]
    img_ids = [_img_id(f) for f in json_jpg_files]
    return img_ids
