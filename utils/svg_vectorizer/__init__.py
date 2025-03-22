"""
SVG vectorization module.
"""

from .core import convert_image_to_svg
from .optimizer import optimize_svg, calculate_path_area
from .batch import batch_convert_folder, process_images_to_svg
from .params import (
    DEFAULT_PARAMS,
    update_params,
    print_params
)

__all__ = [
    'convert_image_to_svg',
    'optimize_svg',
    'calculate_path_area',
    'batch_convert_folder',
    'process_images_to_svg',
    'DEFAULT_PARAMS',
    'update_params',
    'print_params'
]
