import argparse
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def ip_to_numeric(octets):
    return octets[0]*256**3 + octets[1]*256**2 + octets[2]*256 + octets[3]


def generate_synthetic(n_normal=8000, n_anom=800):
    np.random.seed(42)
    N_NORMAL = n_normal
    N_ANOM = n_anom
    hours_normal = np.random.choice(range(8,19), size=N_NORMAL)
    ip_normals = np.random.randint(1000, 50000, size=N_NORMAL)
    failed_normal = np.random.poisson(0.4, size=N_NORMAL)
    geo_dist_normal = np.abs(np.random.normal(loc=50, scale=30, size=N_NORMAL))
    status_normal = np.random.binomial(1, 0.98, size=N_NORMAL)

    hours_anom = np.random.choice([0,1,2,3,4,5,22,23], size=N_ANOM)
    ip_anom = np.random.randint(70000, 140000, size=N_ANOM)
    failed_anom = np.random.poisson(6, size=N_ANOM) + 1
    geo_dist_anom = np.abs(np.random.normal(loc=1200, scale=400, size=N_ANOM))
    status_anom = np.random.binomial(1, 0.2, size=N_ANOM)

    hours = np.concatenate([hours_normal, hours_anom])
    ip_numeric = np.concatenate([ip_normals, ip_anom])
    failed_attempts = np.concatenate([failed_normal, failed_anom])
    geo_distance = np.concatenate([geo_dist_normal, geo_dist_anom])
    status = np.concatenate([status_normal, status_anom])

    start = datetime(2025,1,1,0,0,0)
    timestamps = [start + timedelta(minutes=int(i)) for i in range(N_NORMAL+N_ANOM)]
    timestamps = [t.isoformat() for t in timestamps]

    labels = np.array([0]*N_NORMAL + [1]*N_ANOM)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'hour': hours,
        'ip_numeric': ip_numeric,
        'failed_attempts': failed_attempts,
        'geo_distance': geo_distance,
        'status': status,
        'is_anomaly': labels
    })
    return df


def parse_logs(input_path):
    # Placeholder: implement parser to convert your raw log lines into the DataFrame schema
    # For now, raise informative error
    raise NotImplementedError("Please implement parse_logs() for your specific log format.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['synthetic','parse'], default='synthetic')
    parser.add_argument('--out', required=True)
    parser.add_argument('--input', default=None)
    args = parser.parse_args()

    if args.mode == 'synthetic':
        df = generate_synthetic()
        df.to_csv(args.out, index=False)
        print(f"Synthetic data written to {args.out}")
    else:
        if not args.input:
            raise ValueError('Please supply --input when mode=parse')
        df = parse_logs(args.input)
        df.to_csv(args.out, index=False)
        print(f"Parsed data written to {args.out}")

if __name__ == '__main__':
    main()