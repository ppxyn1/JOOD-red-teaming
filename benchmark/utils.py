import base64
import io
import requests
from PIL import Image

def get_base64(image: Image.Image) -> str:
    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return base64_image


def run_llava(prompt, api_url, model, image=None) -> str:
    info = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    # We concern only VLM (paper tested with text-only as well) 
    if image:
        base64_image = get_base64(image)
        info["images"] = [base64_image]

    response = requests.post(api_url, json=info, timeout=60)
    response.raise_for_status()
    result = response.json()
    return result.get("response", "").strip()
 

def run_judge_model(prompt, api_url, model) -> str:
    info = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    response = requests.post(api_url, json=info, timeout=60)
    response.raise_for_status()  # when the request raise an error 
    result = response.json()

    content = result.get("message",{}).get("content")
    if content:
        return content.strip()
    else:
        return "No response"


