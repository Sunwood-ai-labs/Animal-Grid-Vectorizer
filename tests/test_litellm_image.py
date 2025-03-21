import os
import base64
from litellm import completion

import os
from dotenv import load_dotenv
import gradio as gr
import tempfile
import shutil

# .envファイルを読み込む
load_dotenv()

# 画像をBase64エンコード
image_path = "static/image_fx_ - 2025-03-18T000151.879.jpg"
with open(image_path, "rb") as f:
    image_data = f.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

# openai call
response = completion(
    model = "xai/grok-2-vision-1212", 
    messages=[
        {
            "role": "user",
            "content": [
                            {
                                "type": "text",
                                "text": "What’s in this image simple caption?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
        }
    ],
)

