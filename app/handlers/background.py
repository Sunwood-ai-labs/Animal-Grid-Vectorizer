"""
Background removal handling functionality.
"""

import os
from utils.background_removal import (
    remove_background_simple,
    remove_background_advanced
)

def handle_background_removal(image_paths, output_dir, method):
    """
    Handle background removal process.
    
    Args:
        image_paths (list): List of paths to input images
        output_dir (str): Directory for output
        method (str): Background removal method ('simple' or 'advanced')
        
    Returns:
        list: Paths to processed images
    """
    bg_removed_dir = os.path.join(output_dir, "bg_removed")
    os.makedirs(bg_removed_dir, exist_ok=True)
    
    bg_removed_paths = []
    for img_path in image_paths:
        filename = os.path.basename(img_path)
        output_path = os.path.join(bg_removed_dir, filename)
        
        if method == "simple":
            processed_path = remove_background_simple(img_path, output_path)
        else:
            processed_path = remove_background_advanced(img_path, output_path)
        
        if processed_path:
            bg_removed_paths.append(processed_path)
    
    return bg_removed_paths if bg_removed_paths else image_paths
