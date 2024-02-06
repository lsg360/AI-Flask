import base64
import os
import requests
from PIL import Image

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv("API_HOST", "https://api.stability.ai")
api_key = "sk-EPvQRup24mdQ607OsV1Ye6yWJ57ebLbLugqxFZABlmlwzqeY"  # Replace with your actual API key

if api_key is None:
    raise Exception("Missing Stability API key.")

out_directory = "./out"
os.makedirs(out_directory, exist_ok=True)

def generate_ai_image(data_url, prompt):
    # Convert base64 data URL to image file
    image_path = save_data_url_as_image(data_url)

    # Resize image to valid dimensions
    resized_image_path = resize_image(image_path)

    # Send the resized image to the AI API
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/image-to-image",
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        files={
            "init_image": open(resized_image_path, "rb")
        },
        data={
            "image_strength": 0.1,
            "init_image_mode": "IMAGE_STRENGTH",
            "text_prompts[0][text]": prompt,
            "cfg_scale": 15,
            "sampler": "K_DPMPP_2M",
            "samples": 1,
            "steps": 50,
            "style_preset": "anime",
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # Retrieve the base64-encoded image from the response
    base64_image = data["artifacts"][0]["base64"]
    return base64_image

def save_data_url_as_image(data_url):
    _, encoded = data_url.split(",", 1)
    image_path = "./out/drawn_image.png"
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(encoded))
    return image_path

def resize_image(image_path):
    img = Image.open(image_path)
    resized_img = img.resize((1024, 1024))  # Use the desired dimensions
    resized_image_path = "./out/resized_image.png"
    resized_img.save(resized_image_path)
    return resized_image_path
