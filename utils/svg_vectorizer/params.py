"""
Parameter management for SVG vectorization.
"""

# Default parameters for SVG conversion
DEFAULT_PARAMS = {
    # Color mode settings
    'COLORMODE': 'color',  # 'color' or 'binary'

    # Hierarchy mode settings
    'HIERARCHICAL': 'stacked',  # 'stacked' or 'cutout'

    # Trace mode settings
    'MODE': 'spline',  # 'spline', 'polygon', or 'none'

    # Filter settings
    'FILTER_SPECKLE': 10,  # Noise filter (0-128)
    'COLOR_PRECISION': 6,  # Color precision (1-8)
    'LAYER_DIFFERENCE': 16,  # Gradient steps (0-128)

    # Curve fitting settings
    'CORNER_THRESHOLD': 60,  # Angle threshold (0-180)
    'LENGTH_THRESHOLD': 4.0,  # Segment length (3.5-10)
    'MAX_ITERATIONS': 10,  # Maximum iterations (1-20)
    'SPLICE_THRESHOLD': 45,  # Splice threshold (0-180)
    'PATH_PRECISION': 9,  # Path precision (1-10)
}

def update_params(base_params, new_params):
    """
    Update parameters with new values.

    Args:
        base_params (dict): Base parameter dictionary
        new_params (dict): New parameter values to update
        
    Returns:
        dict: Updated parameter dictionary
    """
    updated_params = base_params.copy()
    for key, value in new_params.items():
        if key in updated_params:
            updated_params[key] = value
            print(f"Parameter updated: {key} = {value}")
        else:
            print(f"Warning: Unknown parameter '{key}' was ignored.")
    return updated_params

def print_params(params):
    """
    Display current parameter settings.
    
    Args:
        params (dict): Parameter dictionary to display
    """
    print("Current parameter settings:")
    for key, value in params.items():
        print(f"  {key}: {value}")

def validate_params(params):
    """
    Validate parameter values.
    
    Args:
        params (dict): Parameters to validate
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    validations = {
        'COLORMODE': lambda x: x in ['color', 'binary'],
        'HIERARCHICAL': lambda x: x in ['stacked', 'cutout'],
        'MODE': lambda x: x in ['spline', 'polygon', 'none'],
        'FILTER_SPECKLE': lambda x: 0 <= x <= 128,
        'COLOR_PRECISION': lambda x: 1 <= x <= 8,
        'LAYER_DIFFERENCE': lambda x: 0 <= x <= 128,
        'CORNER_THRESHOLD': lambda x: 0 <= x <= 180,
        'LENGTH_THRESHOLD': lambda x: 3.5 <= x <= 10,
        'MAX_ITERATIONS': lambda x: 1 <= x <= 20,
        'SPLICE_THRESHOLD': lambda x: 0 <= x <= 180,
        'PATH_PRECISION': lambda x: 1 <= x <= 10
    }
    
    for key, validator in validations.items():
        if key not in params:
            return False, f"Missing parameter: {key}"
        if not validator(params[key]):
            return False, f"Invalid value for {key}: {params[key]}"
    
    return True, "Parameters are valid"
