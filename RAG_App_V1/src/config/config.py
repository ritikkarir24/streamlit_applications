import yaml
from dataclasses import dataclass

@dataclass
class ModelConfig:
    model_name: str
    chunk_size: int
    chunk_overlap: int
    pdfs_directory: str

def load_config(config_path: str = "config.yaml") -> ModelConfig:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return ModelConfig(**config['model_settings'])
