"""
Core functionality for grid image processing.
"""

import os
from .splitter import split_animal_illustrations, create_output_directory
from .refiner import refine_animal_illustrations
from .overview import create_overview_image

def process_grid_image(image_path, output_base_dir='output', rows=3, cols=6):
    """
    Process a grid image by splitting, refining, and creating an overview.
    
    Args:
        image_path (str): Path to the input grid image
        output_base_dir (str): Base directory for all output
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
    
    Returns:
        dict: Dictionary containing paths to split images, refined images, and overview
    """
    # Create base output directory
    output_base_dir = create_output_directory(output_base_dir)
    
    # Create subdirectories
    split_dir = os.path.join(output_base_dir, 'split_animals')
    refined_dir = os.path.join(output_base_dir, 'refined_animals')
    
    # Process the image
    split_paths = split_animal_illustrations(image_path, split_dir, rows, cols)
    refined_paths = refine_animal_illustrations(split_dir, refined_dir)
    overview_path = create_overview_image(refined_dir)
    
    return {
        'split_paths': split_paths,
        'refined_paths': refined_paths,
        'overview_path': overview_path,
        'split_dir': split_dir,
        'refined_dir': refined_dir
    }
