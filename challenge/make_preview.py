import argparse
import cv2
import numpy as np
import json
from pathlib import Path
from tqdm import tqdm


cam2rgb = np.array([
        1.8795, -1.0326, 0.1531,
        -0.2198, 1.7153, -0.4955,
        0.0069, -0.5150, 1.5081,]).reshape((3, 3))


def parse_args():
    parser = argparse.ArgumentParser("Generate JPG previews of PNG images using illuminance chromaticity data (\"gt\" field) from JSON markup")
    parser.add_argument("-d", "--dir", required=False, default=None, help="Path to dir with PNG images")
    parser.add_argument("-i", "--imgs", nargs='+', required=False, default=[], help="Paths to PNG images")
    args = parser.parse_args()
    assert bool(args.imgs) ^ bool(args.dir), "Directory (explicit) or images should be specified"
    return args


def linearize(img, black_lvl=2048, saturation_lvl=2**14-1):
    """
    :param saturation_lvl: 2**14-1 is a common value. Not all images
                           have the same value.
    """
    return np.clip((img - black_lvl)/(saturation_lvl - black_lvl), 0, 1)


def get_preview(img_png_path, field_name="gt"):
    assert img_png_path.endswith("PNG"), "Image filename extension is not PNG!"
    with open(img_png_path[:-4] + ".JPG.json") as meta:
        illum = np.array(json.load(meta)[field_name])
        illum /= illum.sum()

    cam = cv2.imread(img_png_path, cv2.IMREAD_UNCHANGED)
    cam = linearize(cv2.cvtColor(cam, cv2.COLOR_BGR2RGB).astype(np.float64))

    cam_wb = np.clip(cam/illum, 0, 1)

    rgb = np.dot(cam_wb, cam2rgb.T)
    rgb = np.clip(rgb, 0, 1)**(1/2.2)
    return (rgb*255).astype(np.uint8)


def save_preview(img_path, img):
    cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    args = parse_args()
    images_list = args.imgs if args.dir is None else [str(img_path) for img_path in Path(args.dir).glob("*.PNG")]
    for img_path in tqdm(images_list):
        image = get_preview(img_path)
        save_preview(img_path[:-4] + "_corrected.JPG", image)

