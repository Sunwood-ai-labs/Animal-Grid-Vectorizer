"""
Advanced background removal using GrabCut algorithm.
"""

import cv2
import numpy as np
import os

def remove_background_advanced(image_path, output_path=None, iterations=5):
    """
    Remove background using GrabCut algorithm for high-quality results.
    
    Args:
        image_path (str): Path to input image
        output_path (str, optional): Path for output image. If None, generates new path
        iterations (int): Number of GrabCut iterations
        
    Returns:
        str: Path to processed image
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image: {image_path}")
        return None
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Initialize mask
    mask = np.zeros(img.shape[:2], np.uint8)
    
    # Initialize background and foreground models
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    
    # Estimate foreground area
    # Use center portion of image as initial foreground
    margin = min(width, height) // 8
    rect = (margin, margin, width - 2*margin, height - 2*margin)
    
    # Run GrabCut algorithm
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, iterations, cv2.GC_INIT_WITH_RECT)
    
    # Create mask for foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # Apply mask to extract foreground
    img_fg = img * mask2[:, :, np.newaxis]
    
    # Create alpha channel
    alpha = np.zeros_like(mask2, dtype=np.uint8)
    alpha[mask2 > 0] = 255
    
    # Create BGRA image
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    
    # Generate output path if not specified
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_nobg_advanced.png"
    
    # Save image
    cv2.imwrite(output_path, bgra)
    print(f"Saved background-removed image: {output_path}")
    
    return output_path
