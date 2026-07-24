import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

METRIC_PATH = os.path.join(BASE_DIR, "models", "metrics.json")


def load_metrics():

    if not os.path.exists(METRIC_PATH):

        return {}

    with open(METRIC_PATH, "r") as f:

        return json.load(f)