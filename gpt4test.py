#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 21:38:09 2024

@author: szabi
"""
import io
from PIL import Image
import base64

import os
from openai import OpenAI

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

system_role="You are BeauScore, the darmatological expert bot. \
BeauScore Dermatological's primary role is to provide subjective beauty scores for faces before and after dermatological treatments. \
It will focus exclusively on analyzing and scoring changes in skin texture, tone, clarity, and overall aesthetic appeal after treatments, providing scores on a scale from 0 to 100. \
BeauScore Dermatological will not offer skincare or makeup advice but will concentrate solely on evaluating the effectiveness of dermatological treatments based on facial beauty. \
The scoring will be based on general aesthetic principles, and the interaction will remain supportive and positive, emphasizing improvements and positive outcomes.\
Provide the response in HTML format!' \
First put the before and after treatment scores in a table,\
Then write a detailed explanation about the effect of the darmatological treatment!\
Do not write about anything else!\
Answer in Hungarian language!"

os.environ['OPENAI_API_KEY'] = "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"

client = OpenAI(organization='org-veI9jSaTe0emMKdfhQiSzs17')

image_path_1 = "/home/szabi/Projects/beaustory/resources/before_after_images/Picture2.b.png"
image_path_2 = "/home/szabi/Projects/beaustory/resources/before_after_images/Picture2.a.png"

# Convert images to the appropriate format for the API
image_bytes_1 = encode_image(image_path_1)
image_bytes_2 = encode_image(image_path_2)

# Assuming the API accepts a multipart/form-data request with images
# files = {
#     'image1': ('image1.jpg', image_bytes_1, 'image/jpeg'),
#     'image2': ('image2.jpg', image_bytes_2, 'image/jpeg'),
# }


response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
     "role": "system",
     "content": system_role
     
    },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "The first image was taken before a darmatological treatment"},
        {
          "type": "image_url",
          # "image_url": {
          #   "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
          "image_url": {
            "url": f"data:image/jpeg;base64,{image_bytes_1}"
          }
        }
      ],
    },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "The second image was taken after a darmatological treatment"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{image_bytes_2}"
          }
        }
      ],
    },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Provide scores for the images in a table and explain the effect of the darmatological treatment! "},
      ],
    }
  ],
  max_tokens=1024,
  temperature=0,
)


output=response.choices[0].message.content

with open("out.html","w") as f:
    f.write(output)