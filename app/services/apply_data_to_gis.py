from arcgis.features import FeatureLayer
from arcgis.gis import GIS
import pandas as pd


def load_csv_features(csv_path: str) -> list:
    """
    Load CSV and convert each row to a
    Feature dict with geometry and attributes.
    """
    df = pd.read_csv(csv_path)
    features = []
    for row in df.itertuples(index=False):
        attributes = {
            column: getattr(row, column)
            for column in df.columns
        }
        feature = {
            "geometry": {
                "x": float(getattr(row, "long")),
                "y": float(getattr(row, "lat")),
                "spatialReference": {"wkid": 4326}
            },
            "attributes": attributes
        }
        features.append(feature)
    return features


def connect_gis(
        username: str,
        password: str,
        url: str = "https://www.arcgis.com"
) -> GIS:
    return GIS(url, username=username, password=password)


def get_feature_layer(
        gis: GIS,
        item_id: str,
        layer_index: int = 0
) -> FeatureLayer:
    item = gis.content.get(item_id)
    return item.layers[layer_index]


def clear_layer(layer: FeatureLayer):
    existing = layer.query(where="1=1", out_fields="*")
    if existing.features:
        layer.delete_features(where="1=1")


def add_features(layer: FeatureLayer, features: list):
    if features:
        layer.edit_features(adds=features)
