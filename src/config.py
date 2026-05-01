from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

NOTEBOOKS_DIR = ROOT_DIR / "notebooks"
REPORTS_DIR = ROOT_DIR / "reports"
REFERENCES_DIR = ROOT_DIR / "references"
FIGURES_DIR = ROOT_DIR / "figures"
MODELS_DIR = ROOT_DIR / "models"

RAW_MICRODATA_PATH = (
    RAW_DIR
    / "global_findex_2025_microdata"
    / "findex_microdata_2025_labelled_update112425.csv"
)

MODEL_NUMERIC_FEATURES = [
    "age",
]

MODEL_BINARY_FEATURES = [
    "is_female",
    "is_employed",
    "is_urban",
    "uses_internet",
]

MODEL_CATEGORICAL_FEATURES = [
    "education_level",
    "income_quintile",
    "region",
]

MODEL_FEATURES = (
    MODEL_NUMERIC_FEATURES
    + MODEL_BINARY_FEATURES
    + MODEL_CATEGORICAL_FEATURES
)

RANDOM_STATE = 42
