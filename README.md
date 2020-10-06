# Cube++
Cube++ is a new dataset for the color constancy problem that continues the Cube+ dataset https://ipg.fer.hr/ipg/resources/color_constancy. It includes images of different scenes under various conditions. For calculating the ground truth illuminance object with known colors appears in the scene. The Cube++ dataset is used in ICMV 2020 2nd IEC and will be fully published soon. 

# Characteristics
* 4890 images
*	Manual annotation and metadata for images
*	Various illumination scenes

# Detailed description
Images were obtained with Canon 550D and Canon 600D cameras. As a calibration tool SpyderCube was used due to its ability to identify multiple illumination sources.

## Dataset includes
* *auxiliary/source/CR2/\*.CR2* – Raw CR2 images
* *PNG/\*.png* – 16-bit PNG images, generated using original CR2 files
* *JPG/\*.jpg* – Downscaled JPG images
* *auxiliary/source/JPG.JSON/\*.jpg.json* – JSON markup files. Each file contains manually labeled annotation
* *gt.csv* – Ground truth file. The table contains automatically calculated ground truth values. The columns are: image and for each of the 4 triangles (left, right, left bottom, right bottom) it contains three columns r, g, b with the corresponding RGB illumination estimation. The illumination estimation is normalized so that r + g + b = 1
* *properties.csv* – Annotation and metadata file. The table contains the most relevant meta information of the dataset images. It includes the average triangle brightness, manually labeled properties, selected EXIF fields
* *auxiliary/extra/exif/\*.json* – Extracted EXIF data
* *auxiliary/extra/gt_json/\*.json* – Calculated ground truth values in JSON format

## Manually labeled features description
* daytime – time of the day when the image was taken. Possible answers: day, night, unknown.
* place – is the image taken indoor or outdoor. Possible answers: indoor, outdoor, unknown.
* illumination – is the illumination of the scene natural or artificial. Possible answers: natural, artificial, mixed, unknown.
* is_sharp – is the image sharp. Possible answers: True, False.
* shadows – are there any shadows in the scene. Possible answers: yes, no, unknown.
* richness – does the scene has many objects of various colors. Possible answers: rich, simple, unknown.
* has_known_objects – are there any objects with known colors in the scene (except for SpyderCube). Possible answers: True, False.
* light_objects – what illumination sources (out of the predetermined list) are presented in the scene. May have multiple answers. Possible answers: sun, sky, lamp, flash, none.

## Camera and EXIF data included
* MakerNotes:InternalSerialNumber – Internal Serial number of the camera
* EXIF:ISO – ISO
* EXIF:Model – Model of the camera
* EXIF:ExposureTime – Exposure time of the photo
* EXIF:ApertureValue – Aperture value of the photo
* MakerNotes:LensModel – Model of the camera’s lens
* EXIF:Orientation – Image orientation

# Papers
If you use the dataset in your research, please refer to our paper:
* Ershov, Egor I., A. V. Belokopytov, and A. V. Savchik. "Problems of dataset creation for light source estimation." arXiv preprint [arXiv:2006.02692](https://arxiv.org/abs/2006.02692).
