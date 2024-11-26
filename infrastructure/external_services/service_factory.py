import os
from service_integrator import ServiceIntegrator
from config_loader import load_config

def create_service_integrator(service_name: str) -> ServiceIntegrator:
    """
    Factory method to create service-specific integrators.
    
    :param service_name: Name of the service to integrate
    :return: Configured ServiceIntegrator
    """
    # Load configuration from external file
    service_configs = load_config()
    
    config = service_configs.get(service_name.lower())
    if not config:
        raise ValueError(f"Unsupported service: {service_name}")
    
    # Get API key from environment variable
    api_key = os.getenv(f"{service_name.upper()}_API_KEY")
    if not api_key:
        raise ValueError(f"No API key found for {service_name}")
    
    return ServiceIntegrator(
        base_url=config['base_url'], 
        api_key=api_key,
        auth_type=config.get('auth_type')
    )
