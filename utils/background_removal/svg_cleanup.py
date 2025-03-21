"""
SVG cleanup functionality for background removal.
"""

import xml.etree.ElementTree as ET
import re
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

def get_transform_values(transform_attr):
    """
    Extract translation values from transform attribute.
    
    Args:
        transform_attr (str): SVG transform attribute
        
    Returns:
        tuple: (x, y) translation values
    """
    if not transform_attr:
        return 0, 0

    match = re.search(r'translate\((-?\d+\.?\d*),(-?\d+\.?\d*)\)', transform_attr)
    if match:
        return float(match.group(1)), float(match.group(2))
    return 0, 0

def calculate_new_dimensions(paths):
    """
    Calculate dimensions needed to contain remaining paths.
    
    Args:
        paths (list): List of path elements
        
    Returns:
        tuple: (min_x, min_y, max_x, max_y)
    """
    if not paths:
        return 0, 0, 0, 0

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    for path in paths:
        path_data = path.get('d', '')
        transform = path.get('transform', '')
        tx, ty = get_transform_values(transform)

        # Extract coordinates
        coords = re.findall(r'[A-Z]\s*(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)
        if not coords:
            coords = re.findall(r'(-?\d+\.?\d*)\s+(-?\d+\.?\d*)', path_data)

        if coords:
            # Apply transform and update bounds
            for x_str, y_str in coords:
                x, y = float(x_str) + tx, float(y_str) + ty
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    # Add padding
    padding = 10
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    max_x += padding
    max_y += padding

    return min_x, min_y, max_x, max_y

def find_and_remove_large_paths(svg_file, output_file, area_threshold=0.9, auto_resize=True):
    """
    Find and remove all paths that exceed the area threshold from SVG file.
    
    Args:
        svg_file (str): Path to input SVG file
        output_file (str): Path for output SVG file
        area_threshold (float): Threshold ratio of total area to consider as background (0.0-1.0)
        auto_resize (bool): Whether to automatically resize SVG after removal
        
    Returns:
        str: Path to processed SVG file
    """
    logger.info(f"Processing SVG file: {svg_file}")
    try:
        # Parse SVG file
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Find all path elements
        paths = root.findall('.//{http://www.w3.org/2000/svg}path')
        if not paths:
            paths = root.findall('.//path')  # Try without namespace

        if not paths:
            print("No paths found in SVG file.")
            return None

        # Calculate total SVG area
        total_area = 0
        path_areas = {}

        logger.info("Calculating path areas...")
        for path in paths:
            path_data = path.get('d', '')
            if 'Z' in path_data:  # Only consider closed paths
                area = calculate_path_area(path_data)
                transform = path.get('transform', '')
                tx, ty = get_transform_values(transform)
                transform_factor = 1 + (abs(tx) + abs(ty)) / 1000
                area *= transform_factor
                path_areas[path] = area
                total_area += area

        # Find all paths that exceed the area threshold
        large_paths = []
        for path, area in path_areas.items():
            area_ratio = area / total_area if total_area > 0 else 0
            logger.debug(f"Path area ratio: {area_ratio:.2%}")
            
            if area_ratio > area_threshold:
                large_paths.append(path)
                logger.info(f"Found large path with area ratio: {area_ratio:.2%}")

        # Remove all large paths
        if large_paths:
            paths_removed = 0
            for path in large_paths:
                parent = None
                for p in root.findall('.//*'):
                    for child in p:
                        if child == path:
                            parent = p
                            break

                if parent is not None:
                    parent.remove(path)
                else:
                    root.remove(path)
                paths_removed += 1

            logger.info(f"Removed {paths_removed} paths that exceeded area threshold of {area_threshold:.2%}")
        else:
            logger.info(f"No paths exceeded area threshold of {area_threshold:.2%}")

        # Update paths list
        paths = root.findall('.//{http://www.w3.org/2000/svg}path')
        if not paths:
            paths = root.findall('.//path')

        # Auto-resize SVG if requested
        if auto_resize and paths:
            min_x, min_y, max_x, max_y = calculate_new_dimensions(paths)
            width = max_x - min_x
            height = max_y - min_y

            if width > 0 and height > 0:
                root.set('width', str(int(width)))
                root.set('height', str(int(height)))
                root.set('viewBox', f"{min_x} {min_y} {width} {height}")
                print(f"Resized SVG: width={width}, height={height}")

        # Write output file
        ET.register_namespace('', "http://www.w3.org/2000/svg")
        tree.write(output_file, encoding='utf-8', xml_declaration=True)

        return output_file

    except Exception as e:
        print(f"Error processing SVG: {str(e)}")
        return None
