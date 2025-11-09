# detectors.py placeholder
import argparse
import numpy as np
from sklearn.ensemble import IsolationForest


def mahalanobis_scores(X, X_ref=None):
    import numpy as np
    if X_ref is None:
        X_ref = X
    mu = X_ref.mean(axis=0)
    cov = np.cov(X_ref.T)
    cov += np.eye(cov.shape[0]) * 1e-6
    cov_inv = np.linalg.pinv(cov)
    dif = X - mu
    md = np.einsum('ij,jk,ik->i', dif, cov_inv, dif)
    return md


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    data = np.load(args.in)
    X = data['X']
    y = data['y'] if 'y' in data.files and data['y'].size else None

    # Rule-based score (raw failed_attempts column index 2)
    scores_rule = X[:, 2].astype(float)

    # Mahalanobis: use only rows where y==0 if y provided, else use entire dataset as reference
    if y is not None and y.size:
        X_ref = X[y==0]
    else:
        X_ref = X
    md = mahalanobis_scores(X, X_ref=X_ref)
    md_norm = (md - md.min()) / (md.max() - md.min() + 1e-12)

    # Isolation Forest
    iso = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
    iso.fit(X)
    iso_raw = -iso.decision_function(X)
    iso_norm = (iso_raw - iso_raw.min()) / (iso_raw.max() - iso_raw.min() + 1e-12)

    np.savez_compressed(args.out, scores_rule=scores_rule, scores_md=md_norm, scores_iso=iso_norm, y=y)
    print(f"Scores saved to {args.out}")

if __name__ == '__main__':
    main()