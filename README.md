# CubePlusPlus
Cube++ - is the new dataset for the color constancy problem that continues the Cube+ dataset https://ipg.fer.hr/ipg/resources/color_constancy. The CubePlusPlus dataset is used in ICMV 2020 2nd IEC and will be fully published after the challenge. See http://chromaticity.iitp.ru for a more detailed description.

The challenge files for general/indoor/two_illuminant tracks are available via links: 

Train | Test (password-protected)
------------ | -------------
[general 1/4](https://drive.google.com/file/d/1-jWLZeG4h0OkjDhCgD7D8Q6cphhnkJCp/view?usp=sharing), [2/4](https://drive.google.com/file/d/1HxkQ4JJb2Nbp0s0ikI99lwBUHyV-VRw8/view?usp=sharing), [3/4](https://drive.google.com/file/d/1cjQ5HEt7KE268iv3uOn1mVGeIryzbUHg/view?usp=sharing), [4/4 (same as indoor)](https://yadi.sk/d/84w9OHpUZIoPZA) | [general_test](https://yadi.sk/d/M8Jdq_tuiR-I4A) 
[indoor](https://yadi.sk/d/84w9OHpUZIoPZA) | [indoor_test](https://yadi.sk/d/KruOvfdD10ptag) 
[two_illuminant](https://drive.google.com/file/d/12Qq32voyQzF8Vf6c-o_6j2h3EuAwQatE/view?usp=sharing) | [two_illuminant_test](https://yadi.sk/d/8u9y4uAU1bBFrQ)


# Challenge scripts 
* calc_metrics.py - script that calculates the final metrics. It has three variants for the challenge tracks. For example, the constant baseline results for all the tracks can be calculated with:
```bash
python3 calc_metrics.py --gt train_csvs/general.csv --pred train_csvs/const_baseline/general.csv --problem general
python3 calc_metrics.py --gt train_csvs/indoor.csv --pred train_csvs/const_baseline/indoor.csv --problem indoor
python3 calc_metrics.py --gt train_csvs/two_illuminant.csv --pred train_csvs/const_baseline/two_illuminant.csv --problem two_illuminant
```
* make_preview.py - script for train images visualization

Scripts requirements can be installed with a command
```pip3 install -r requirements.txt```

# Papers
If you use the dataset in your research, please refer to our papers from the list:
* Ershov, Egor I., A. V. Belokopytov, and A. V. Savchik. "Problems of dataset creation for light source estimation." arXiv preprint arXiv:2006.02692 (2020).