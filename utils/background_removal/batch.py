"""
Batch processing functionality for background removal.
"""

import os
from .simple import remove_background_simple
from .advanced import remove_background_advanced

def batch_remove_background(input_dir, output_dir=None, method='simple', threshold=240, iterations=5):
    """
    Remove background from all images in a directory.
    
    Args:
        input_dir (str): Input directory containing images
        output_dir (str, optional): Output directory for processed images
        method (str): Background removal method ('simple' or 'advanced')
        threshold (int): Threshold for simple method
        iterations (int): Iterations for advanced method
        
    Returns:
        list: Paths to processed images
    """
    # Create output directory if not specified
    if output_dir is None:
        output_dir = os.path.join(input_dir, 'nobg')
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")
    
    # List for processed image paths
    processed_paths = []
    
    # Process each image in directory
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue
        
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_nobg.png")
        
        # Apply background removal
        if method.lower() == 'simple':
            result_path = remove_background_simple(input_path, output_path, threshold)
        else:
            result_path = remove_background_advanced(input_path, output_path, iterations)
        
        if result_path:
            processed_paths.append(result_path)
    
    print(f"Processed {len(processed_paths)} images")
    return processed_paths
