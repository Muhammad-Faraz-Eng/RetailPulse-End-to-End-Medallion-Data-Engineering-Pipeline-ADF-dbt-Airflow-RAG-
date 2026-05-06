import yaml
import os


def load_config():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    config_path = os.path.join(BASE_DIR, "configs", "pipeline.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
