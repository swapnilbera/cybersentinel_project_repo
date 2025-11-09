#!/usr/bin/env bash
set -e
mkdir -p results
python -u src/ingest.py --mode synthetic --out results/data.csv
python -u src/features.py --in results/data.csv --out results/features.npz
python -u src/detectors.py --in results/features.npz --out results/scores.npz
python -u src/evaluate.py --in results/scores.npz --out results
echo "Demo finished. Results in results/"
