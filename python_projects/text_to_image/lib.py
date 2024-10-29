import requests

# Replace with your actual Hugging Face API token
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"  # replace model as desired
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def text_to_image_generation_api(prompt):
    """
    Generate an image from text using the Hugging Face API.
    
    Parameters:
        prompt (str): The text prompt to generate the image.
    
    Returns:
        bytes: The image data in binary format.
    """
    data = {
        "inputs": prompt,
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

