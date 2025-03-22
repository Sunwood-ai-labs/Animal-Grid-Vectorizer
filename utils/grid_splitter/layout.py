"""
Grid layout generation functionality.
"""

import xml.etree.ElementTree as ET
from loguru import logger

def create_grid_layout(svg_files, output_path, rows, cols):
    """
    Create a single SVG file with grid layout of all SVG files.
    
    Args:
        svg_files (list): List of SVG file paths
        output_path (str): Path where the grid layout SVG will be saved
        rows (int): Number of rows in grid
        cols (int): Number of columns in grid
    
    Returns:
        str: Path to the created grid SVG file
    """
    if not svg_files:
        logger.warning("No SVG files provided")
        return None

    try:
        # Create root SVG element
        svg = ET.Element('svg')
        svg.set('xmlns', 'http://www.w3.org/2000/svg')
        
        # Calculate grid dimensions
        cell_width = 200  # Default cell width
        cell_height = 200  # Default cell height
        padding = 50  # Padding between cells
        
        grid_width = cols * (cell_width + padding) - padding
        grid_height = rows * (cell_height + padding) - padding
        
        # Set SVG dimensions
        svg.set('width', str(grid_width))
        svg.set('height', str(grid_height))
        svg.set('viewBox', f'0 0 {grid_width} {grid_height}')
        
        # Add each SVG file to the grid
        for idx, svg_file in enumerate(svg_files):
            if idx >= rows * cols:  # Skip if exceeds grid size
                break
            
            try:
                # Calculate position in grid
                row = idx // cols
                col = idx % cols
                x = col * (cell_width + padding)
                y = row * (cell_height + padding)
                
                # Create group for this SVG
                g = add_svg_to_grid(svg, svg_file, x, y, cell_width, cell_height)
                if g is None:
                    continue
                    
            except Exception as e:
                logger.error(f"Error processing {svg_file}: {str(e)}")
                continue
        
        # Save the grid layout SVG
        tree = ET.ElementTree(svg)
        tree.write(output_path)
        logger.info(f"Grid layout SVG saved to {output_path}")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error creating grid layout: {str(e)}")
        return None

def add_svg_to_grid(root_svg, svg_file, x, y, cell_width, cell_height):
    """
    Add an SVG file to the grid layout.
    
    Args:
        root_svg (Element): Root SVG element
        svg_file (str): Path to SVG file to add
        x (float): X position in grid
        y (float): Y position in grid
        cell_width (float): Width of grid cell
        cell_height (float): Height of grid cell
        
    Returns:
        Element: Created group element or None on failure
    """
    try:
        # Read SVG file
        tree = ET.parse(svg_file)
        source_root = tree.getroot()
        
        # Create group for this SVG
        g = ET.SubElement(root_svg, 'g')
        g.set('transform', f'translate({x},{y})')
        
        # Get viewBox from original SVG
        viewBox = source_root.get('viewBox')
        if viewBox:
            # Extract dimensions from viewBox
            vb_parts = viewBox.split()
            if len(vb_parts) == 4:
                orig_width = float(vb_parts[2])
                orig_height = float(vb_parts[3])
                
                # Calculate scale to fit in cell
                scale_x = cell_width / orig_width
                scale_y = cell_height / orig_height
                scale = min(scale_x, scale_y)
                
                # Update transform with scaling
                g.set('transform', f'translate({x},{y}) scale({scale})')
        
        # Copy all elements from original SVG
        for child in source_root:
            g.append(child)
            
        return g
            
    except Exception as e:
        logger.error(f"Error adding SVG to grid: {str(e)}")
        return None
