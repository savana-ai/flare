def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    :param config_path: Path to the configuration file
    :return: Configuration dictionary
    """
    with open(config_path, 'r') as f:
        return json.load(f)

