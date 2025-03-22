"""
Common UI components and utilities.
"""

import gradio as gr

# Emoji definitions
EMOJI = {
    "grid": "🔲",
    "split": "✂️",
    "vector": "🖋️",
    "settings": "⚙️",
    "upload": "📤",
    "download": "📥",
    "success": "✅",
    "error": "❌",
    "animal": "🐾",
    "art": "🎨",
    "magic": "✨",
    "folder": "📁",
    "image": "🖼️",
    "svg": "📐",
    "processing": "⏳",
    "complete": "🏁",
    "background": "🧹",
    "caption": "💬",
    "ai": "🤖"
}

def toggle_gemini_opts(x):
    """
    Event handler for Gemini options visibility.
    
    Args:
        x (bool): Visibility state
        
    Returns:
        list: List of Gradio updates
    """
    return [
        gr.update(visible=x),  # api_key
        gr.update(visible=x),  # model
        gr.update(visible=x)   # caption_prompt
    ]

def toggle_area_threshold(x):
    """
    Event handler for area threshold visibility.
    
    Args:
        x (bool): Visibility state
        
    Returns:
        Gradio update object
    """
    return gr.update(visible=x)
