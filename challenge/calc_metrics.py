import argparse
import json
import os
import os.path as osp
import pandas as pd
import numpy as np


def parse_csv(csv_path):
    df = pd.read_csv(csv_path)
    return df


def save_json(json_path, data): 
    with open(json_path, 'w') as f:
        f.write(json.dumps(data))
        f.write('\n')


def assert_same_images(gt_imgs, pred_imgs):
    gt_without_pred = list(set(gt_imgs) - set(pred_imgs))
    assert len(gt_without_pred) == 0, 'Error! There are images without prediction, e.g. {}'.format(str(gt_without_pred[:10]))
    not_gt_predicted = list(set(pred_imgs) - set(gt_imgs))
    assert len(not_gt_predicted) == 0, 'Error! There are predictions for other images, e.g. {}'.format(str(not_gt_predicted[:10]))
    

def normalize(v):
    return np.array(v) / np.linalg.norm(v, ord=2)


def angle(v1, v2): 
    v1 = normalize(v1)
    v2 = normalize(v2)
    return np.arccos((v1*v2).sum().clip(-1, 1)) / np.pi * 180
        

def repr_ang_error(gt, pred): 
    """Calc reproduction angular errors. See "Finlayson, Graham D., and Roshanak Zakizadeh. Reproduction angular
        error: An improved performance metric for illuminant estimation." """
    errs = [] 
    for v1, v2 in zip(gt, pred):
        err = angle([1, 1, 1], v2 / v1)
        errs.append(err)
    return np.array(errs)


def mean_repr_ang_error(gt, pred):
    reprs = repr_ang_error(gt=gt, pred=pred)
    return np.mean(reprs)


def mean_squared_repr_ang_error(gt, pred):
    reprs = repr_ang_error(gt=gt, pred=pred)
    return np.mean(reprs ** 2)


def two_illuminant_error(gt, pred, skip_share=0.75):
    gt1, gt2 = gt
    pred1, pred2 = pred

    reprs_sq_straight = (
        repr_ang_error(gt1, pred1) ** 2 + 
        repr_ang_error(gt2, pred2) ** 2
    )
    reprs_sq_reverted = (
        repr_ang_error(gt1, pred2) ** 2 + 
        repr_ang_error(gt2, pred1) ** 2 
    )
    reprs_sq = np.minimum(reprs_sq_straight, reprs_sq_reverted)
    
    reprs_sq = sorted(reprs_sq)
    worst = reprs_sq[int(skip_share * len(reprs_sq)):]
    return np.mean(worst)


def calc_metrics(gt, pred, problem_type): 
    assert problem_type in ['indoor', 'general', 'two_illuminant']
    assert_same_images(gt['image'], pred['image'])

    pred = pred.add_prefix('p_')
    joined = gt.set_index('image').join(pred.set_index('p_image'))
    
    if problem_type == 'indoor': 
        error = mean_repr_ang_error(
            joined[['r', 'g', 'b']].to_numpy(), 
            joined[['p_r', 'p_g', 'p_b']].to_numpy()
        )                
        return {'mean_repr_ang_error': error}
    elif problem_type == 'general': 
        error = mean_squared_repr_ang_error(
            joined[['r', 'g', 'b']].to_numpy(), 
            joined[['p_r', 'p_g', 'p_b']].to_numpy()
        )                
        return {'mean_squared_repr_ang_error': error}
    elif problem_type == 'two_illuminant':
        gt_vals = (
            joined[['r1', 'g1', 'b1']].to_numpy(),
            joined[['r2', 'g2', 'b2']].to_numpy(),
        )
        pred_vals = (
            joined[['p_r1', 'p_g1', 'p_b1']].to_numpy(),
            joined[['p_r2', 'p_g2', 'p_b2']].to_numpy(),
        )
        return {'two_illuminant_error': two_illuminant_error(gt_vals, pred_vals)}

    else:  
        raise NotImplementedError


###############################################################################
# main

def parse_args():
    parser = argparse.ArgumentParser("Calculate final metrics for the ICMV 2020 2nd IEC challenge")
    parser.add_argument('--gt', required=True, help="csv with ground_truth answers")
    parser.add_argument('--pred', required=True, help="csv with predicted answers")
    parser.add_argument('-o', '--output', help="file to save metrics info")
    parser.add_argument('-p', '--problem', required=True, help="problem type")
    return parser.parse_args()


def main(gt, pred, problem, output=None, verbose=True): 
    gt_ans = parse_csv(gt)
    pred_ans = parse_csv(pred)
    results = calc_metrics(gt_ans, pred_ans, problem)
    if verbose:
        print(results)
    if output:
        save_json(output, results)

    return results


if __name__ == "__main__":
    args = parse_args()
    main(args.gt, args.pred, args.problem, args.output)
