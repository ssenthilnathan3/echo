from dotenv import load_dotenv
from pydantic import ValidationError
from app.common.models.spec import Spec
import sys
import os
import yaml

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

_ = load_dotenv()

PUBLIC_YAML_PATH = os.getenv("PUBLIC_YAML_PATH")


def load_validate():
    if not PUBLIC_YAML_PATH:
        raise ValueError("PUBLIC_YAML_PATH not found in environment variable")

    if not PUBLIC_YAML_PATH.endswith((".yaml", ".yml")):
        raise ValueError("PUBLIC_YAML_PATH must end with .yaml or .yml")

    if not os.path.exists(PUBLIC_YAML_PATH):
        raise FileNotFoundError(f"File not found at path: {PUBLIC_YAML_PATH}")

    try:
        with open(PUBLIC_YAML_PATH) as stream:
            loaded_file = yaml.safe_load(stream)

            try:
                spec_schema = Spec(**loaded_file)
                print(spec_schema.model_dump())
            except ValidationError as e:
                for err in e.errors():
                    print(f" - {err['loc']}: {err['msg']}")
                return None
        return loaded_file
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax: {e}") from e


def load():
    try:
        return load_validate()
    except Exception as e:
        print(f"Error loading YAML: {e}")
        return None
