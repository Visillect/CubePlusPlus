# Technical desciption of the dataset files

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
16-bit png image. They are generated from CR2 with a simplest debayering. 

The black level is approximately 2048, not substracted, as it may be useful for some algorithms. 
The saturation level depend on image and is less then 16384.

## JPG/{img_id}.jpg

JPG images generated with the *dcraw* program. The processing depend on camera. For visualization purposes only.

## gt.csv
The table contains automatically calculated ground truth values. The columns are: *image*, *left_r*, *left_g*, *left_b*, *right_r*, *right_g*, *right_b*, *left_white_r*, *left_white_g*, *left_white_b*, *right_white_r*, *right_white_g*, *right_white_b*. 

Image stands for id in the format dd_dddd, where d is 0-9 digit. 
The other columns contain three columns r, g, b each for the 4 triangles (left (gray), right (gray), left white, right white). They are the corresponding RGB illumination estimation. The illumination estimation is normalized so that r + g + b = 1. 

## properties.csv
The table contains selected properties for each image. The columns are: 
* *image* - image identificators 
* *full_estimation* - if the image have a full estimation of the scene or a partial one only. Controverasl good images may be labelled as a partially estimated ones. 
* illuminance features - values within a range 0-1 of mean trianlge illuminance: 
    * *left_tr_illuminance*, 
    * *right_tr_illuminance*, 
    * *left_white_tr_illuminance*, 
    * *right_white_tr_illuminance*,
* overexposed features - estimation, if the triangle is overexposed. The images with any overexposed gray edges were excluded from the dataset.
    * *left_white_overexposed*
    * *right_white_overexposed*

The table also contains manually labeled features and selected camera EXIF fields.

### Manually labeled features description
* *daytime* – time of the day when the image was taken. Possible answers: day, night, unknown.
* *place* – is the image taken indoor or outdoor. Possible answers: indoor, outdoor, unknown.
* *illumination* – is the illumination of the scene natural or artificial. Possible answers: natural, artificial, mixed, unknown.
* *is_sharp* – is the image sharp. Possible answers: True, False.
* *shadows* – are there any shadows in the scene. Possible answers: yes, no, unknown.
* *richness* – does the scene has many objects of various colors. Possible answers: rich, simple, unknown.
* *has_known_objects* – are there any objects with known colors in the scene (except for SpyderCube). Possible answers: True, False.
* *light_objects* – what illumination sources (out of the predetermined list) are presented in the scene. May have multiple answers. Possible answers: sun, sky, lamp, flash, none.

### Camera and EXIF data included
* *MakerNotes:InternalSerialNumber* – Internal Serial number of the camera. There were 3 cameras, so the field enables.
* *EXIF:ISO*
* *EXIF:ApertureValue*
* *EXIF:ExposureTime*
* *MakerNotes:PerChannelBlackLevel* - may be useful for a black level substraction.
* *MakerNotes:NormalWhiteLevel* - may be useful for a correct saturation estimation.
* *EXIF:Model* – Model of the camera, Canon EOS 550D or a Canon EOS 600D.
* *MakerNotes:LensModel* – Model of the camera’s lens.

## auxiliary/extra 
Some files that can be used for dataset usage. 
* *exif/{img_id}.json* – All the extracted EXIF data
* *gt_json/{img_id}.json* – Calculated gts, all the data is duplicated in gt.csv or properties csv
* *exif_stat.csv* – Exif fields statistics, how many unique values in the dataset, the three most common ones. 

### auxiliary/extra/cam_estimation.csv
Selected EXIF estimations made by camera. The table contains columns *image*, *Composite:BlueBalance*, *Composite:RedBalance*, *Composite:LightValue*, MakerNotes:ColorTempMeasured*, *MakerNotes:ColorTempAsShot*

## auxiliary/source 

The source of the dataset, all the other files are automatically build from this directory. 

### auxiliary/sourceCR2/{img_id}.CR2 

Original raw CR2 images taken from the camera.

### full_estimation.csv

The table with a manually full_estimation labeled annotation.

### JPG.JSON/{img_id}.jpg.json

The image-wise JSON markup files. Each file contains manually labeled annotation and an automatically calculated overexpose esimation

The annotation contains the cube faces coordinates (they can be slightly outside of the image).


