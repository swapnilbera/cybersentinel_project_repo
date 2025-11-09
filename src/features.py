# features.py placeholder
import argparse
import numpy as np
import pandas as pd

FEATURE_COLUMNS = ['hour', 'ip_numeric', 'failed_attempts', 'geo_distance', 'status']


def build_features(df):
    # Basic selection + simple percentile-based min-max scaling
    X = df[FEATURE_COLUMNS].values.astype(float)
    X_scaled = X.copy()
    for i in range(X.shape[1]):
        col = X[:, i]
        lo = np.percentile(col, 1)
        hi = np.percentile(col, 99)
        if hi - lo <= 0:
            hi = lo + 1.0
        X_scaled[:, i] = (col - lo) / (hi - lo)
    return X_scaled


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='infile', required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.infile)
    X = build_features(df)
    ids = df.index.values
    y = df['is_anomaly'].values if 'is_anomaly' in df.columns else None
    np.savez_compressed(args.out, X=X, y=y, ids=ids, raw=df.to_dict(orient='list'))
    print(f"Features saved to {args.out}")

if __name__ == '__main__':
    main()