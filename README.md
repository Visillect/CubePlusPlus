# Cube++
Cube++ - is the new dataset for the color constancy problem that continues the Cube+ dataset https://ipg.fer.hr/ipg/resources/color_constancy. The Cube++ dataset is used in ICMV 2020 2nd IEC and will be fully published after the challenge. 

# ICMV 2020 2nd IEC
The goal of the challenge is to predict illumination chromaticity. The challenge has three tracks for various scene types: 
* Indoor 
* General (indoor included)
* Two illuminant 

The images are available via links: 

Train | Test (password-protected)
------------ | -------------
[general 1/4](https://drive.google.com/file/d/1-jWLZeG4h0OkjDhCgD7D8Q6cphhnkJCp/view?usp=sharing), [2/4](https://drive.google.com/file/d/1HxkQ4JJb2Nbp0s0ikI99lwBUHyV-VRw8/view?usp=sharing), [3/4](https://drive.google.com/file/d/1cjQ5HEt7KE268iv3uOn1mVGeIryzbUHg/view?usp=sharing), [4/4 (same as indoor)](https://yadi.sk/d/84w9OHpUZIoPZA) | [general_test](https://yadi.sk/d/M8Jdq_tuiR-I4A) 
[indoor](https://yadi.sk/d/84w9OHpUZIoPZA) | [indoor_test](https://yadi.sk/d/KruOvfdD10ptag) 
[two_illuminant](https://drive.google.com/file/d/12Qq32voyQzF8Vf6c-o_6j2h3EuAwQatE/view?usp=sharing) | [two_illuminant_test](https://yadi.sk/d/8u9y4uAU1bBFrQ)

See http://chromaticity.iitp.ru for a more detailed description.

## Challenge scripts 
There are calc_metrics.py and make_preview.py scripts useful for the participants. Requirements for them can be installed with
```bash
pip3 install -r requirements.txt
```

The calc_metrics.py script calculates the final metrics of the competition. It has three variants for the challenge tracks. 
* **--problem** - the challenge track *general*, *indoor* or *two_illuminant*, metrics for which to calulate
* **--gt** - csv with the ground truth answers
* **--pred** - csv with the predictions 
* **[--output]** - file to save results (optional)

For example, the constant baseline results for each track can be calculated with
```bash
cd challenge_scripts
python3 calc_metrics.py --problem general --gt train/general.csv --pred baseline_examples/const/general.csv 
python3 calc_metrics.py --problem indoor --gt train/indoor.csv --pred baseline_examples/const/indoor.csv 
python3 calc_metrics.py --problem two_illuminant --gt train/two_illuminant.csv --pred baseline_examples/const/two_illuminant.csv 
```

The make_preview.py script visualizes the train PNG image normalized in respect to ground truth illumination value in the corresponding JSON annotation. 

# Papers
If you use the dataset in your research, please refer to our papers from the list:
* Ershov, Egor I., A. V. Belokopytov, and A. V. Savchik. "Problems of dataset creation for light source estimation." arXiv preprint arXiv:2006.02692 (2020).