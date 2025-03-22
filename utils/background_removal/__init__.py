"""
Background removal module for Animal Grid Vectorizer.
"""

from .simple import remove_background_simple
from .advanced import remove_background_advanced
from .svg_cleanup import find_and_remove_large_paths
from .batch import batch_remove_background

__all__ = [
    'remove_background_simple',
    'remove_background_advanced',
    'find_and_remove_large_paths',
    'batch_remove_background'
]
