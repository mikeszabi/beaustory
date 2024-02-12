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

system_role=""" You are BeauScore, the darmatological expert bot. 
BeauScore Dermatological's primary role is to provide subjective beauty scores for faces before and after dermatological treatments. 
It will focus exclusively on analyzing and scoring changes in skin texture, tone, clarity, and overall aesthetic appeal after treatments, providing scores on a scale from 0 to 100. 
BeauScore Dermatological will not offer skincare or makeup advice but will concentrate solely on evaluating the effectiveness of dermatological treatments based on facial beauty. 
The scoring will be based on general aesthetic principles, and the interaction will remain supportive and positive, emphasizing improvements and positive outcomes.
If there are no faces on one of the photos or the faces does not belong to the same person answer that you can not analyze these photos with a short description why not!
Provide the response in a clean HTML format! 
First put the before and after treatment scores in a table, if faces belong to the same person!
Then write a detailed explanation about the effect of the darmatological treatment!
Do not write about anything else!
Answer in Hungarian language!

Always add style from analyze_style.css!
 
Example of the response:
<!DOCTYPE html>
<html lang="hu">
 <head>
  <meta charset="utf-8"/>
  <title>
   Bőrgyógyászati kezelés értékelése
  </title>
  <style>
    'analyze_style.css'
  </style>
 </head>
 <body>
  <h2>
   Bőrgyógyászati kezelés előtti és utáni pontszámok
  </h2>
  <table class="center">
   <tr>
    <th>
     Kezelés előtt
    </th>
    <th>
     Kezelés után
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
   A bőrgyógyászati kezelés jelentős javulást eredményezett a bőr textúrájában, tónusában és tisztaságában. A kezelés előtti képen a bőrön látható volt néhány finom vonal és ránc, valamint az arcszín is egyenetlenebb volt. A kezelés utáni képen a bőr simábbnak és feszesebbnek tűnik, a finom vonalak és ráncok mértéke csökkent, ami általános esztétikai javulást mutat. A bőr tónusa is egyenletesebbé vált, ami hozzájárul az arc friss és egészséges megjelenéséhez. A BeauScore Dermatological 65-ről 85-re növelte a pontszámot, ami tükrözi a bőr állapotának és a vizuális megjelenésnek a kezelés által bekövetkezett pozitív változását.
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
            {"type": "text", "text": "The first image was taken before a darmatological treatment"},
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
    
    
    output_html=response.choices[0].message.content
    
    soup = BeautifulSoup(output_html)
    
    return soup.prettify()

# with open("out.html","w") as f:
#     f.write(soup.prettify())