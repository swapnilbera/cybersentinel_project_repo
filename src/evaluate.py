# evaluate.py placeholder
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_fscore_support


def evaluate_scores(scores, y, top_k_fraction=0.05):
    try:
        roc = roc_auc_score(y, scores)
    except Exception:
        roc = float('nan')
    K = max(1, int(len(scores) * top_k_fraction))
    idx_sorted = np.argsort(-scores)
    topk_idx = idx_sorted[:K]
    prec_at_k = y[topk_idx].sum() / K
    thr = np.median(scores)
    pred_bin = (scores >= thr).astype(int)
    prec, recall, f1, _ = precision_recall_fscore_support(y, pred_bin, average='binary', zero_division=0)
    return dict(roc_auc=roc, prec_at_k=prec_at_k, precision=prec, recall=recall, f1=f1, K=K)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    data = np.load(args.in)
    s_rule = data['scores_rule']
    s_md = data['scores_md']
    s_iso = data['scores_iso']
    y = data['y'] if 'y' in data.files and data['y'].