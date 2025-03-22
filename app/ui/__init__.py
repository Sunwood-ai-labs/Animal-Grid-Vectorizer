"""
UI module for Animal Grid Vectorizer.
"""

from .styles import custom_css, custom_head
from .components_common import EMOJI, toggle_gemini_opts, toggle_area_threshold
from .input_components import (
    create_input_components,
    create_grid_components,
    create_background_components,
    create_caption_components
)
from .processing_components import (
    create_svg_components,
    create_process_button,
    create_grid_display_option
)
from .output_components import (
    create_output_components,
    create_progress_display,
    update_progress
)

__all__ = [
    # Styles
    'custom_css',
    'custom_head',
    
    # Common components
    'EMOJI',
    'toggle_gemini_opts',
    'toggle_area_threshold',
    
    # Input components
    'create_input_components',
    'create_grid_components',
    'create_background_components',
    'create_caption_components',
    
    # Processing components
    'create_svg_components',
    'create_process_button',
    'create_grid_display_option',
    
    # Output components
    'create_output_components',
    'create_progress_display',
    'update_progress'
]
