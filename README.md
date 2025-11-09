# CyberSentinel — MTech Project Template
This repository contains a full reproducible pipeline for an unsupervised enterprise threat detector (ETD).
## What is included
- Data ingestion (`src/ingest.py`) — parse logs or generate synthetic data for experiments
- Feature engineering (`src/features.py`) — build features such as failed attempts, geo distance, hour-of-day
- Detectors (`src/detectors.py`) — rule-based, Mahalanobis, IsolationForest
- Evaluation & visualization (`src/evaluate.py`) — ROC, Precision@K, histograms, top alerts
- Utilities (`src/utils.py`) — I/O helpers
- Dockerfile and requirements for reproducibility


## Quickstart (run synthetic demo)
1. Create a Python environment and install dependencies:


```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt