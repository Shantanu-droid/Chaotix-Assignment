from celery import shared_task
import os
from django.conf import settings
import requests
import base64

@shared_task
def generate_sdxl_images(text):
    '''uses stable diffusion request to generate images'''

    engine_id = "stable-diffusion-v1-6"
    api_host = 'https://api.stability.ai'
    api_key = "sk-fgPtG54WDQp9GhjRI8c6aFKOnWF57hypVsoqodrWD6XkBJ87"

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
                    "text": text
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    data = response.json()
    files = []
    # I am currently writting and reading data from media files
    # as this project is in debug mode
    # however for production use cases using a cloud hosted storage like
    # aws should be used with django-storages
    for i, image in enumerate(data["artifacts"]):
        file_path = os.path.join(settings.MEDIA_ROOT, f'{text.lower().replace(' ','_')}.png')
        with open(file_path, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        files.append(f'{text.lower().replace(' ','_')}.png')
    return files
