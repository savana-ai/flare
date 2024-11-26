import os
import json
import requests
from typing import Dict, Any, Optional
import logging
from enum import Enum, auto


class RequestMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()


class ServiceIntegrator:
    def __init__(
        self, 
        base_url: str, 
        api_key: Optional[str] = None,
        timeout: int = 30,  # Increased timeout for LLM services
        default_headers: Optional[Dict[str, str]] = None,
        auth_type: Optional[str] = None  # 'bearer', 'basic', etc.
    ):
        """
        Initialize the Service Integrator with flexible authentication.
        
        :param base_url: Base URL of the service
        :param api_key: API key for authentication
        :param timeout: Request timeout in seconds
        :param default_headers: Default headers to be sent with each request
        :param auth_type: Authentication type (bearer, basic, etc.)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.default_headers = default_headers or {}
        self.auth_type = auth_type
        self.logger = logging.getLogger(__name__)

        # Set up authentication headers
        if self.api_key:
            if self.auth_type == 'bearer':
                self.default_headers['Authorization'] = f'Bearer {self.api_key}'
            elif self.auth_type == 'basic':
                # For basic auth, you'd typically pass username:password base64 encoded
                import base64
                credentials = base64.b64encode(f"{self.api_key}:".encode()).decode()
                self.default_headers['Authorization'] = f'Basic {credentials}'
            else:
                # Default API key header for many services
                self.default_headers['api-key'] = self.api_key

    def make_request(
        self, 
        endpoint: str, 
        method: RequestMethod = RequestMethod.POST,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a standardized request to the service.
        
        :param endpoint: Service endpoint
        :param method: HTTP method
        :param params: Query parameters
        :param data: Form data
        :param json: JSON payload
        :param headers: Additional headers
        :param kwargs: Additional arguments for requests library
        :return: Standardized response dictionary
        """
        # Merge headers
        request_headers = {**self.default_headers, **(headers or {})}
        
        # Prepare full URL
        full_url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self.logger.info(f"Request to {full_url}")
        
        try:
            request_methods = {
                RequestMethod.GET: requests.get,
                RequestMethod.POST: requests.post,
                RequestMethod.PUT: requests.put,
                RequestMethod.DELETE: requests.delete,
                RequestMethod.PATCH: requests.patch
            }
            
            response = request_methods[method](
                full_url, 
                params=params, 
                data=data, 
                json=json, 
                headers=request_headers,
                timeout=self.timeout,
                **kwargs
            )
            
            response.raise_for_status()
            return {
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'data': response.json() if response.content else None
            }
        
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise




