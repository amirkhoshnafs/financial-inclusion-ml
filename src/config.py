from pathlib import Path

ROOT_DIR=Path(__file__).resolve().parents[1]

DATA_DIR=ROOT_DIR / 'data'
RAW_DIR=DATA_DIR / 'raw'
INTERIM_DIR=DATA_DIR / 'interim'
PROCESSED_DIR=DATA_DIR / 'processed'

NOTEBOOKS_DIR=ROOT_DIR / 'notebooks'
REPORTS_DIR=ROOT_DIR / 'reports'
REFERENCES_DIR=ROOT_DIR / 'references'
FIGURES_DIR=ROOT_DIR / 'figures'
MODELS_DIR=ROOT_DIR / 'models'

RANDOM_STATE=42