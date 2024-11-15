# explorer/utils/loaders.py
import yaml
import os
from .logging import logger

def load_yaml_config(file_path):
    """Load and parse the configuration file from the project root."""
    # Resolve the absolute path based on the project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(project_root, file_path)

    logger.info("📝 Loading configuration from %s", full_path)

    try:
        with open(full_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info("✅ Configuration loaded successfully.")
            return config
    except FileNotFoundError:
        logger.error("🚫 Configuration file not found at %s", full_path)
    except yaml.YAMLError as e:
        logger.error("❌ YAML parsing error in configuration file: %s", str(e))
    except Exception as e:
        logger.error("❌ Unexpected error loading configuration file: %s", str(e))
    return None
