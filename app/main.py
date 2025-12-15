from logging import basicConfig, INFO, getLogger
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from app.services.apply_data_to_gis import (
    load_csv_features,
    connect_gis,
    get_feature_layer,
    clear_layer,
    add_features
)
from app.services.prepare_data import prepare_data

load_dotenv()

GIS_USERNAME: str = getenv("GIS_USERNAME", "test_user")
GIS_PASSWORD: str = getenv("GIS_PASSWORD", "test_password")
ITEM_ID: str = getenv("ITEM_ID", "815e5b14c4da48109f941d1560b75395")
CSV_FILE_NAME: str = getenv("CSV_FILE_NAME", "prepared_data.csv")
GIS_URL: str = getenv("GIS_URL", "https://www.arcgis.com")

basicConfig(level=INFO)
logger = getLogger(__name__)


def run_pipeline():
    sheet_id = "12846JbH2PwR0wN8eLVnosg4xujw-04gKyyD6RuElc-4"
    prepare_data(sheet_id)
    base_dir = Path(__file__).resolve().parent
    csv_path = (base_dir.parent / CSV_FILE_NAME).resolve()

    features = load_csv_features(csv_path.name)
    gis = connect_gis(GIS_USERNAME, GIS_PASSWORD, GIS_URL)
    feature_layer = get_feature_layer(gis, ITEM_ID)

    clear_layer(feature_layer)

    add_features(feature_layer, features)
    logger.info("Features updated successfully.")


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        logger.critical(f"Unexpected error occurred: {e}")
