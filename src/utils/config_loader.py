import yaml


def load_config(config_path:str = "myconfigs\config.yaml")->dict:
    """loads the config file"""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config