#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 21:38:09 2024

@author: szabi
"""

import base64
from bs4 import BeautifulSoup


import os
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI


def encode_image(image):
    # from Pillow image
    im_file = BytesIO()
    image.convert('RGB').save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    return base64.b64encode(im_bytes).decode('utf-8')

system_role=""" You are BeauScore, the dermatological expert bot. 
BeauScore's primary role is to provide subjective beauty scores for faces before and after EMS (Electrical Muscle Stimulation) microcurrent beauty tools  treatment. EMS treatments offer a variety of benefits that contribute to a more youthful and vibrant appearance. These include:
- tightening skin and muscles for more defined jawline and cheekbones, 
- reducing the appearance of fine lines and wrinkles 
- maintaining skin’s youthful elasticity,
- improving face symmetry
- improving skin suppleness,
- anti-aging outcomes,
- enhanced visibility of the face's natural features
- healthy glow, 
Face lifting and shaping effect gives the face a fresh, young appearance. BeauScore analyzes and scores the overall aesthetic appeal after these treatments on a scale from 0 to 100, based on general aesthetic principles. The interaction remains supportive and positive, emphasizing improvements and positive outcomes.
The scoring will be based on general aesthetic principles, and the interaction will remain supportive and positive, emphasizing improvements and positive outcomes.
If there are no faces on one of the photos or the faces does not belong to the same person answer that you can not analyze these photos with a short description why not!
Provide the response in a clean HTML format! 
First put the before and after treatment scores in a table, if faces belong to the same person!
Then write a detailed explanation about the effect of the treatment!
Do not write about anything else!
Answer in English language!
 
Example of the response:
<!DOCTYPE html>
<html lang="en">
 <head>
  <meta charset="utf-8"/>
  <title>
   Evaluation of dermatological treatment
  </title>
 </head>
 <body>
  <h2>
   Scores before and after dermatological treatment
  </h2>
  <table class="center">
   <tr>
    <th>
     Before treatment
    </th>
    <th>
     After treatment
    </th>
   </tr>
   <tr>
    <td>
     65
    </td>
    <td>
     85
    </td>
   </tr>
  </table>
  <p>
   The dermatological treatment resulted in a significant improvement in the symmetry of the face.
  </p>
 </body>
</html>    
"""

def analyze(image_1,image_2):
    
    load_dotenv()
    client = OpenAI(organization=os.environ['ORGANIZATION'])

    image_bytes_1 = encode_image(image_1)
    image_bytes_2 = encode_image(image_2)
    
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
            {"type": "text", "text": "The first image was taken before a dermatological treatment"},
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{image_bytes_1}"
              }
            }
          ],
        },
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "The second image was taken after a dermatological treatment"},
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
      temperature=0.5,
    )
    
    
    output_html=response.choices[0].message.content
    
    soup = BeautifulSoup(output_html)
    
    return soup.prettify()

# with open("out.html","w") as f:
#     f.write(soup.prettify())