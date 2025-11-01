from dotenv import load_dotenv
from pydantic import ValidationError
from app.common.models.echo import Echo
import sys
import os
import yaml


def _load_validate(yaml_path: str):
    if not yaml_path.endswith((".yaml", ".yml")):
        raise ValueError("yaml_path must end with .yaml or .yml")

    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"File not found at path: {yaml_path}")

    try:
        with open(yaml_path) as stream:
            loaded_file = yaml.safe_load(stream)

            try:
                echo_schema = Echo(**loaded_file)
                print(echo_schema.model_dump())
            except ValidationError as e:
                for err in e.errors():
                    print(f" - {err['loc']}: {err['msg']}")
                return None
        return loaded_file
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax: {e}") from e


def load(yaml_path):
    try:
        return _load_validate(yaml_path)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        return None
