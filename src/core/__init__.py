"""
Core module.

This module contains configuration and dependency injection components.
"""

from src.core.config import Config
from src.core.container import container

__all__ = [
    'Config',
    'container',
]
