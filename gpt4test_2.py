#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 21:03:50 2024

@author: szabi
"""

import requests
from PIL import Image
import io

api_key = "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"


# Function to convert an image to the format expected by the API (e.g., bytes)
def convert_image_to_bytes(image_path):
    img = Image.open(image_path)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img.format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

# URLs and authentication for the custom GPT API
api_url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    # Add other headers required by your API
}

# Paths to your images
image_path_1 = "/home/szabi/Projects/beaustory/resources/before_after_images/Picture2.b.png"
image_path_2 = "/home/szabi/Projects/beaustory/resources/before_after_images/Picture2.b.png"

# Convert images to the appropriate format for the API
image_bytes_1 = convert_image_to_bytes(image_path_1)
image_bytes_2 = convert_image_to_bytes(image_path_2)

# Assuming the API accepts a multipart/form-data request with images
files = {
    'image1': ('image1.jpg', image_bytes_1, 'image/jpeg'),
    'image2': ('image2.jpg', image_bytes_2, 'image/jpeg'),
}

# Send the request to the custom GPT API
response = requests.post(api_url, headers=headers, files=files)

# Check the response
if response.status_code == 200:
    print("Successfully called the custom GPT with two images.")
    # Process the response as needed, e.g., print the output or parse JSON
    print(response.json())
else:
    print(f"Failed to call the API. Status code: {response.status_code}, Response: {response.text}")