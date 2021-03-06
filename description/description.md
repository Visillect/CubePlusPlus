# Technical description of the dataset files

<!-- * **PNG/{img_id}.png** – 16-bit PNG images
* **gt.csv** – Ground truth chromaticities answers. Ground truth file. The table contains automatically calculated ground truth values. The columns are: image and for each of the 4 triangles (left, right, left bottom, right bottom) it contains three columns r, g, b with the corresponding RGB illumination estimation. The illumination estimation is normalized so that r + g + b = 1
* **properties.csv** – Annotation and metadata file. The table contains the most relevant meta information of the dataset images. It includes the average triangle brightness, manually labeled properties, selected EXIF fields
* **JPG/{img_id}.jpg** – JPG images, for visualization purposes only
* **auxiliary/**
    * **extra/**
        * **exif/{img_id}.json** – All the extracted EXIF data
        * **gt_json/{img_id}.json** – Calculated gts, all the data is duplicated in gt.csv or properties csv
        * **cam_estimation.csv** – Selected EXIF estimations made by camera
        * **exif_stat.csv** – Exif fields statistics
    * **source/** – the dataset is automatically build from this directory
        * **CR2/{img_id}.CR2** – Original raw CR2 images
        * **JPG.JSON/{img_id}.jpg.json** – JSON markup files. Each file contains manually labeled annotation
        * **full_estimation.csv** – extra markup file for full estimation or partial estimation -->

## PNG/{img_id}.png
16-bit 2592×1728=2<sup>5</sup>3<sup>4</sup>×2<sup>6</sup>3<sup>3</sup> png image. They are generated from CR2 files with the simplest debayering and a few pixel crop, to have the same rectangle as the default camera JPEG.

The black level is approximately 2048, not subtracted, as it may be useful for some algorithms.
The saturation level depend on the image and is less than 16384.

## JPG/{img_id}.jpg

JPG 2592×1728=2<sup>5</sup>3<sup>4</sup>×2<sup>6</sup>3<sup>3</sup> images generated by using the *dcraw* program. The processing slightly depends on the camera. For visualization purposes only.

## gt.csv
The table contains automatically calculated ground truth values. The columns are: *image*, *mean_r*, *mean_g*, *mean_b*, *left_r*, *left_g*, *left_b*, *right_r*, *right_g*, *right_b*, *left_white_r*, *left_white_g*, *left_white_b*, *right_white_r*, *right_white_g*, *right_white_b*.

Image stands for the image id in the format dd_dddd, where d is a 0-9 digit.
Other 12 columns contain r, g, b chromaticities for each of the 4 triangles (left (gray), right (gray), left white, right white). They are the corresponding illumination estimation ground-truth. The ground-truth is normalized so that r + g + b = 1.

The other 3 values correspond to the normed mean (bisector) chromaticity of the left (gray) and the right (gray) ones. The mean chromaticity is calculated for 2234 images, that satisfy the following conditions:
* The image should be manually marked with estimation=full. 
* The angle between left (gray) and right (gray) ground truth chromaticities should be less than 1 degree. 
* Both left and right gray triangles should be bright enough: tr_illuminance value is bigger than 0.1.

## properties.csv
The table contains the most relevant meta-information for each image. The columns are:
* *image* - image identificators.
* *full_estimation* - specifies if the image has a full estimation of the scene illumination or a partial one only. Questionably good images may be labeled as partially estimated ones.
* illuminance features - values within a range 0-1 specifying average triangle illuminance:
    * *left_tr_illuminance*,
    * *right_tr_illuminance*,
    * *left_white_tr_illuminance*,
    * *right_white_tr_illuminance*,
* overexposed features - estimation, which says is a white triangle overexposed. The images with any overexposed gray triangles were excluded from the dataset.
    * *left_white_overexposed*
    * *right_white_overexposed*

The table also contains manual annotation data and selected subset of camera EXIF data fields.

### Manual annotation data description
* *daytime* – time of the day when the image was taken. Possible values: day, night, unknown.
* *place* – the location where the image is taken. Possible values: indoor, outdoor, unknown.
* *illumination* – the type of the scene illumination. Possible values: natural, artificial, mixed, unknown.
* *is_sharp* – specifies if the image is sharp. Possible values: True, False.
* *shadows* – specifies if there are any shadows in the scene. Possible values: yes, no, unknown.
* *richness* – specifies if the scene contains many objects of various colors. Possible values: rich, simple, unknown.
* *has_known_objects* – specifies if there are any objects with known colors in the scene (except for SpyderCube). Possible values: True, False.
* *light_objects* – specifies illumination sources (from a predetermined list) present in the scene. May contain multiple values. Possible values: sun, sky, lamp, flash, none.

### Selected camera and EXIF data description
* *MakerNotes:InternalSerialNumber* – Internal Serial number of the camera. There were 3 cameras. This field specifies which camera was used for the image.
* *EXIF:ISO*
* *EXIF:ApertureValue*
* *EXIF:ExposureTime*
* *MakerNotes:PerChannelBlackLevel* - may be useful for a black level substraction.
* *MakerNotes:NormalWhiteLevel* - may be useful for a correct saturation estimation.
* *EXIF:Model* – Model of the camera, Canon EOS 550D or a Canon EOS 600D.
* *MakerNotes:LensModel* – Model of the camera’s lens.

## auxiliary/extra
Additional useful files.
* *exif/{img_id}.json* – All the extracted EXIF data.
* *gt_json/{img_id}.json* – Calculated ground-truth values. The same as in gt.csv or properties.csv
* *exif_stat.csv* – Statistics on EXIF data of the dataset.

### auxiliary/extra/cam_estimation.csv
Illumination information selected from camera's EXIF data. The table contains columns *image*, *Composite:BlueBalance*, *Composite:RedBalance*, *Composite:LightValue*, MakerNotes:ColorTempMeasured*, *MakerNotes:ColorTempAsShot*

## auxiliary/source

Dataset source directory, from which all the other files are automatically built.

### auxiliary/sourceCR2/{img_id}.CR2

Original raw CR2 image files captured by the camera.

### full_estimation.csv

The table with a manually full_estimation labeled annotation.

### JPG.JSON/{img_id}.jpg.json

The image-wise JSON markup files. Each file contains manually labeled annotation and automatically calculated overexposure estimation

Files include information on manually extracted coordiantes of SpyderCube faces (coordinates may be slightly outside of the image).

# SimpleCube++

SimpleCube++ contains 2234 images from the Cube++ dataset, that have a single mean ground truth estimation.
All the images are 4x downscaled to the 648x432 size. The right bottom recangle 175x250 (700x1000 on original scale) is cropped out to remove SpyderCube color target.
The dataset is divided into train and test parts for simplicity. Each image is independently assigned to the test set with probability 20%.

## {test/train}/PNG/{img_id}.png

16-bit 648x432 png image. They are generated from CR2 files with the simplest debayering, 4x downscaling, 175x250 right bottom rectangle cropping.

The black level is approximately 2048, not subtracted, as it may be useful for some algorithms.
The saturation level depends on the image and is less than 16384.


## {test/train}/gt.csv

The ground truth values. The table contain columns: *image*, *r*, *g*, *b*.
Image stands for the image id in the format dd_dddd, where d is a 0-9 digit.
*r*, *g*, *b* are the source illumination estimation. The ground-truth is normalized so that r + g + b = 1.

## auxiliary/{test/train}_properties.csv

Annotation and metadata file. The table contains the most relevant meta information of the dataset images. The columns are:
* *image* – Image id.
* *ds_version* – 0.0 for Cube images, 1.0 for Cube+ extension and IEC2019 test images, 2.0 for Cube++ extension.
* Manually labeled properties (only *daytime*; *place*; *illumination*; *is_sharp*; *shadows*).

## auxiliary/JPG/{test/train}_{img_id}.jpg

JPEG images with cropped cube area, for visualization purposes only.
