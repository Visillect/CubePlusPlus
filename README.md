# CubePlusPlus
CubePlusPlus - is the new dataset for the color constancy problem that continues the CubePlus dataset https://ipg.fer.hr/ipg/resources/color_constancy. The CubePlusPlus dataset is used in ICMV 2020 2nd IEC (http://chromaticity.iitp.ru) and will be fully published after the challenge.

# Scripts: 
* calc_metrics.py - script that calculates final metric. Usage examples:
```bash
python3 calc_metrics.py --gt train_csvs/general.csv --pred train_csvs/const_baseline/general.csv --problem general
python3 calc_metrics.py --gt train_csvs/indoor.csv --pred train_csvs/const_baseline/indoor.csv --problem indoor
python3 calc_metrics.py --gt train_csvs/two_illuminant.csv --pred train_csvs/const_baseline/two_illuminant.csv --problem two_illuminant
```
* make_preview.py - script for the image reading and visualization.


# Requirements:
* opencv-python - for image reading
* numpy, pandas - for metrics calculation

# Papers
If you use the dataset in your research, please refer to our papers from the list:
* Ershov, Egor I., A. V. Belokopytov, and A. V. Savchik. "Problems of dataset creation for light source estimation." arXiv preprint arXiv:2006.02692 (2020).