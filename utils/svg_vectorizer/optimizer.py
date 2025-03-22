"""
SVG optimization functionality.
"""

import re
import xml.etree.ElementTree as ET
from loguru import logger

def calculate_path_area(path_data):
    """
    Estimate the area of a path by calculating its bounding box.
    
    Args:
        path_data (str): SVG path data string
        
    Returns:
        float: Estimated area of the path
    """
    # Extract coordinates from path data
    coords = re.findall(r'[A-Z]\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

    if not coords:
        # Try to extract coordinates from more complex path data
        coords = re.findall(r'(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

    if not coords:
        return 0

    # Convert to float
    coords = [(float(x), float(y)) for x, y in coords]

    # Find bounding box
    min_x = min(x for x, _ in coords)
    max_x = max(x for x, _ in coords)
    min_y = min(y for _, y in coords)
    max_y = max(y for _, y in coords)

    # Calculate area
    width = max_x - min_x
    height = max_y - min_y
    return width * height

def optimize_svg(svg_path, min_area_percentage=0.01):
    """
    Optimize SVG by removing tiny paths that are likely noise.
    
    Args:
        svg_path (str): Path to the SVG file
        min_area_percentage (float): Minimum area as percentage of total SVG area
        
    Returns:
        str: Path to the optimized SVG file
    """
    try:
        # Parse the SVG file
        tree = ET.parse(svg_path)
        root = tree.getroot()
        
        # Find all path elements
        paths = root.findall(".//{http://www.w3.org/2000/svg}path")
        
        if not paths:
            logger.warning(f"No paths found in {svg_path}")
            return svg_path
            
        # Get SVG dimensions
        width = float(root.get('width', '100'))
        height = float(root.get('height', '100'))
        total_area = width * height
        min_area = total_area * min_area_percentage / 100
        
        # Count paths before optimization
        path_count_before = len(paths)
        
        # Remove tiny paths
        paths_to_remove = []
        for path in paths:
            path_data = path.get('d', '')
            area = calculate_path_area(path_data)
            if area < min_area:
                paths_to_remove.append(path)
        
        for path in paths_to_remove:
            parent = path.getparent()
            if parent is not None:
                parent.remove(path)
        
        # Count paths after optimization
        paths_after = root.findall(".//{http://www.w3.org/2000/svg}path")
        path_count_after = len(paths_after)
        
        logger.info(f"Optimized SVG: removed {path_count_before - path_count_after} of {path_count_before} paths")
        
        # Save the optimized SVG
        optimized_path = svg_path.replace('.svg', '_optimized.svg')
        tree.write(optimized_path)
        
        return optimized_path
        
    except Exception as e:
        logger.error(f"Error optimizing SVG: {str(e)}")
        return svg_path

def adjust_viewbox(root, paths):
    """
    Adjust SVG viewBox to fit the content.
    
    Args:
        root (ElementTree.Element): SVG root element
        paths (list): List of path elements
        
    Returns:
        tuple: (min_x, min_y, width, height)
    """
    if not paths:
        return 0, 0, 100, 100

    # Initialize bounds
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    # Calculate bounds from all paths
    for path in paths:
        path_data = path.get('d', '')
        coords = re.findall(r'[A-Z]\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)
        if not coords:
            coords = re.findall(r'(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

        if coords:
            xs = [float(x) for x, _ in coords]
            ys = [float(y) for _, y in coords]
            min_x = min(min_x, min(xs))
            max_x = max(max_x, max(xs))
            min_y = min(min_y, min(ys))
            max_y = max(max_y, max(ys))

    # Add padding
    padding = 10
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    width = max_x - min_x + 2 * padding
    height = max_y - min_y + 2 * padding

    return min_x, min_y, width, height
