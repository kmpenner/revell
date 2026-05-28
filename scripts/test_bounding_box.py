
import os
import base64
from openai import OpenAI
import json

# Configuration
API_KEY_PATH = r"g:\My Drive\Research\Revell\metadata\openrouter_api_key.txt"
IMAGE_PATH = r"g:\My Drive\Research\Revell\07a Articles\07a.27 - Lxx Mt Aspects\07a.27_p1_300dpi.png"

def get_api_key():
    if os.path.exists(API_KEY_PATH):
        with open(API_KEY_PATH, 'r') as f:
            return f.read().strip()
    return os.environ.get("OPENROUTER_API_KEY")

def image_to_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def detect_bounds(client, base64_image):
    prompt = (
        "Detect the bounding box of the main printed page area in this image (excluding the scanner margins and paper edges). "
        "Return the coordinates as a JSON object with keys [ymin, xmin, ymax, xmax]. "
        "The coordinates should be normalized from 0 to 1000. "
        "Return ONLY the JSON object."
    )

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001", # Using Gemini 2.0 Flash for spatial detection as it's generally good at it
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content.strip()

def main():
    api_key = get_api_key()
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    print(f"Detecting bounds for {IMAGE_PATH}...")
    b64_img = image_to_base64(IMAGE_PATH)
    result = detect_bounds(client, b64_img)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
