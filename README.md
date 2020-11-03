# Cube++

![Image examples](./description/examples.jpg)

Cube++ is a new dataset for the color constancy problem that continues on the [Cube+ dataset](https://ipg.fer.hr/ipg/resources/color_constancy). It includes 4890 images of different scenes under various conditions. For calculating the ground truth illumination, a calibration object with known surface colors was placed in every scene. The Cube++ dataset was used in [ICMV 2020 2nd Illumination Estimation Challenge](http://chromaticity.iitp.ru/). 

**The dataset will be published soon**. 

# Description
* 4890 raw images
* Manual annotations and metadata
* Various scene illuminations

Images were obtained with sensors of same type on Canon 550D and Canon 600D cameras. As a calibration tool, SpyderCube was used due to its ability to identify multiple illumination sources from different angles. The dataset includes:
* **PNG/{img_id}.png** – 16-bit PNG images
* **gt.csv** – Ground truth chromaticities answers. Ground truth file. The table contains automatically calculated ground truth values. The columns are: image and for each of the 4 triangles (left, right, left bottom, right bottom) it contains three columns r, g, b with the corresponding RGB illumination estimation. The illumination estimation is normalized so that r + g + b = 1
* **properties.csv** – Annotation and metadata file. The table contains the most relevant meta information of the dataset images. It includes the average triangle brightness, manually labeled properties, selected EXIF fields
* **JPG/{img_id}.jpg** – JPEG images, for visualization purposes only
* **auxiliary/** 
    * **extra/**
        * **exif/{img_id}.json** – All the extracted EXIF data
        * **gt_json/{img_id}.json** – Calculated gts, all the data is duplicated in gt.csv or properties csv
        * **cam_estimation.csv** – Selected EXIF estimations made by camera
        * **exif_stat.csv** – EXIF fields statistics
    * **source/** – the dataset is automatically build from this directory
        * **CR2/{img_id}.CR2** – Original raw CR2 images
        * **JPG.JSON/{img_id}.jpg.json** – JSON markup files. Each file contains manually labeled features and cube coordinates
        * **full_estimation.csv** – extra markup file for full estimation or partial estimation

See also a more [detailed description](./description/description.md).

# Papers
If you use the dataset in your research, please refer to the following paper:
* Ershov, Egor I., A. V. Belokopytov, and A. V. Savchik. "Problems of dataset creation for light source estimation." arXiv preprint [arXiv:2006.02692](https://arxiv.org/abs/2006.02692).
