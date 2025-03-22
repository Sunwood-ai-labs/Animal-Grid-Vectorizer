"""
Simple threshold-based background removal functionality.
"""

import cv2
import numpy as np
import os

def remove_background_simple(image_path, output_path=None, threshold=240):
    """
    Remove background using simple threshold-based method.
    
    Args:
        image_path (str): Path to input image
        output_path (str, optional): Path for output image. If None, generates new path
        threshold (int): Threshold value for background detection (0-255)
        
    Returns:
        str: Path to processed image
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image: {image_path}")
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Threshold to separate background
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)
    
    # Create alpha channel
    alpha = np.zeros_like(gray)
    alpha[mask > 0] = 255
    
    # Create BGRA image
    bgra = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    bgra[:, :, 3] = alpha
    
    # Generate output path if not specified
    if output_path is None:
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_nobg.png"
    
    # Save image
    cv2.imwrite(output_path, bgra)
    print(f"Saved background-removed image: {output_path}")
    
    return output_path
