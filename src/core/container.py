"""
Dependency Injection Container for modular service management.

This container allows for easy registration and retrieval of services,
making it simple to add, remove, or replace modules.
"""

from typing import Type, TypeVar, Dict, Any

T = TypeVar('T')


class Container:
    """
    A simple dependency injection container.
    
    Services can be registered and retrieved by their interface type.
    This enables loose coupling and easy module replacement.
    """
    
    _instance = None
    _services: Dict[Type, Any] = {}
    _instances: Dict[Type, Any] = {}
    
    def __new__(cls):
        """Singleton pattern to ensure a single container instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the container (useful for testing)."""
        cls._instance = None
        cls._services = {}
        cls._instances = {}
    
    def register(self, interface_type: Type, implementation_type: Type, singleton: bool = True):
        """
        Register a service implementation for an interface.
        
        Args:
            interface_type: The interface/abstract class type
            implementation_type: The concrete implementation class
            singleton: If True, the same instance will be returned for all requests
        """
        self._services[interface_type] = {
            'type': implementation_type,
            'singleton': singleton
        }
    
    def get(self, interface_type: Type) -> Any:
        """
        Get an instance of a service by its interface type.
        
        Args:
            interface_type: The interface/abstract class type
            
        Returns:
            An instance of the registered implementation
            
        Raises:
            ValueError: If no service is registered for the interface
        """
        if interface_type not in self._services:
            raise ValueError(f"No service registered for {interface_type.__name__}")
        
        service_config = self._services[interface_type]
        
        if service_config['singleton'] and interface_type in self._instances:
            return self._instances[interface_type]
        
        implementation_type = service_config['type']
        instance = implementation_type()
        
        if service_config['singleton']:
            self._instances[interface_type] = instance
        
        return instance
    
    def register_instance(self, interface_type: Type, instance: Any):
        """
        Register a pre-created instance for an interface.
        
        Args:
            interface_type: The interface/abstract class type
            instance: The pre-created instance
        """
        self._instances[interface_type] = instance
        self._services[interface_type] = {
            'type': type(instance),
            'singleton': True
        }


# Global container instance
container = Container()
