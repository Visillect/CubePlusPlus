import numpy as np
from skimage import draw
from utils.cube_io import png16_load, linearize, json_load, json_save

ANGLE_THRESHOLD = 1
DARK_THRESHOLD = 0.01  # 2048 + 0.01*2**16


def calc_triangle_color(img, points, scale=0.5):
    """calc mean color on (downscaled) triangle
    Args:
        img(np.array): img with float64 values
        points(list): list of triangle coords
        scale(float): share of triangle to use
    """
    points = np.array(points)
    barycenter = np.mean(points, axis=0)

    for p in points:
        p[0] = scale * p[0] + (1 - scale) * barycenter[0]
        p[1] = scale * p[1] + (1 - scale) * barycenter[1]

    mask = np.zeros([img.shape[0], img.shape[1]], dtype=np.int)
    y, x = draw.polygon(points[:,1], points[:,0], shape=img.shape)
    mask[y, x] = 1

    pixels = img[mask==1]
    return pixels.mean(axis=0).astype(img.dtype)


def calc_angle(v1, v2):
    """calc angle between vectors in degrees"""
    v1 = np.array(v1) / np.linalg.norm(v1, ord=2)
    v2 = np.array(v2) / np.linalg.norm(v2, ord=2)
    return np.arccos((v1 * v2).sum().clip(-1, 1)) / np.pi * 180


def calc_mean_chromaticity(v1, v2):
    """Calculate mean (angle bisector) chromaticity"""
    v1 = np.array(v1) / np.linalg.norm(v1, ord=2)
    v2 = np.array(v2) / np.linalg.norm(v2, ord=2)
    mean = v1 + v2
    return mean / mean.sum()


def calc_single_illuminance(gt, estimation):
    single_gt = {
        "has_mean_gt": False,
        "mean": [float("Nan"), float("Nan"), float("Nan")],
    }

    # white triangles are ignored: they have a slightly different reflectance
    angle_ok = calc_angle(gt['left'], gt['right']) < ANGLE_THRESHOLD
    
    # grey triangles with too small illuminance are ignored: may be not stable
    left_ok = gt["left_tr_illuminance"] >= DARK_THRESHOLD
    right_ok = gt["right_tr_illuminance"] >= DARK_THRESHOLD
    
    if (estimation == "full") and left_ok and right_ok and angle_ok:
        single_gt["has_mean_gt"] = True
        single_gt["mean"] = calc_mean_chromaticity(gt["left"], gt["right"]).tolist()  # tolist for JSON serializability

    return single_gt


def calc_gt(img, markup):
    """calc answers by triangles
    Args:
        img(np.array): img with float64 values
        markup(dict): loaded json with a markup
    Returns:
        colors dict ("gt", "gt_left", "gt_right")
    """

    # markup is x,y; size is h,w
    assert markup['size'][0] == img.shape[1]
    assert markup['size'][1] == img.shape[0]
    assert img.dtype == np.uint16

    triangles = {}
    for obj in markup['objects']:
        assert len(obj['tags']) == 1
        tag = obj['tags'][0]
        triangles[tag] = obj['data']


    rename = {
        'left': 'left',
        'right': 'right',
        'left_b': 'left_white',
        'right_b': 'right_white',
    }
    gt = {}

    for old_name, new_name in rename.items():
        color_with_black_level = calc_triangle_color(img, triangles[old_name])
        tr_color = linearize(color_with_black_level)
        tr_color_sum = np.sum(tr_color)

        gt[new_name] = (tr_color / tr_color_sum).tolist()  # tolist for JSON serializability
        gt[new_name + '_tr_illuminance'] = (tr_color_sum / 3).tolist()  # "/3" averaging for 0-1 range

    gt.update(calc_single_illuminance(gt, markup['properties']['estimation']))
    return gt


def save_gt(img_path, markup_path, output_path):
    img = png16_load(img_path)
    markup = json_load(markup_path)
    gt_colors = calc_gt(img, markup)
    json_save(output_path, gt_colors)


def parse_args():
    parser = argparse.ArgumentParser("Calculate gt vals")
    parser.add_argument('img_path', help='raw img file (png16)')
    parser.add_argument('markup_path', help='annotation file (jpg.json)')
    parser.add_argument('--res_path', help='output path')
    return parser.parse_args()


if __name__ == "__main__":
    main(**vars(parse_args()))
