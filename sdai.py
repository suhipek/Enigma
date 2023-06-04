import os
import requests
import re

engine_id = "stable-diffusion-v1-5"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = os.getenv('STABILITY_API_KEY')

def text2img(prompt):
    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    return data['artifacts'][0]['base64']

def text2img_html(match: re.Match):
    img = text2img(match.group(1))
    return f'<img src="data:image/png;base64,{img}"/>'

def insert_img(text):
    return re.sub(r'%%%([^%]+)%%%', text2img_html, text)
