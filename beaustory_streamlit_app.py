#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:06:26 2024

@author: szabi
"""

import sys

sys.path.append(r'./code')

from bs4 import BeautifulSoup
import streamlit as st
from PIL import Image, ExifTags
# import base64
# import pandas as pd

from face_analysis import analyze
from morph import create_gif

base_width=800

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def click_button():
    st.session_state.process = True
    
def exif_rotate(image):
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break
    
    exif = image._getexif()
    if exif:

        if exif[orientation] == 3:
            image=image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image=image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image=image.rotate(90, expand=True)
        
    return image

# Set the title of the app
st.title('BeauSTORY')

if 'process' not in st.session_state:
    st.session_state.process = False

# Create two columns for uploading images
col1, col2 = st.columns(2)

with col1:
    # Create a file uploader to allow users to upload an image
    #uploaded_file1 = st.file_uploader("Kezelés előtti fotó...", type=['jpg', 'jpeg', 'png'], key='1')
    uploaded_file1 = st.file_uploader("Before treatment photo...", type=['jpg', 'jpeg', 'png'], key='1')
    if uploaded_file1 is not None:
        # Display the uploaded image
        image1 = Image.open(uploaded_file1)
        image1=exif_rotate(image1)
        wpercent = (base_width / float(image1.size[0]))
        hsize = int((float(image1.size[1]) * float(wpercent)))
        image1 = image1.resize((base_width, hsize), Image.LANCZOS)
        #st.image(image1, caption='Kezelés előtt', use_column_width=True)
        st.image(image1, caption='Before treatment', use_column_width=True)

with col2:
    # Create another file uploader for the second image
    #uploaded_file2 = st.file_uploader("Kezelés utáni fotó...", type=['jpg', 'jpeg', 'png'], key='2')
    uploaded_file2 = st.file_uploader("After treatment photo...", type=['jpg', 'jpeg', 'png'], key='2')
    if uploaded_file2 is not None:
        # Display the second uploaded image
        image2 = Image.open(uploaded_file2)
        image2=exif_rotate(image2)
        wpercent = (base_width / float(image2.size[0]))
        hsize = int((float(image2.size[1]) * float(wpercent)))
        image2 = image2.resize((base_width, hsize), Image.LANCZOS)
        #st.image(image2, caption='Kezelés után', use_column_width=True)
        st.image(image2, caption='After treatment', use_column_width=True)

# Check if both images have been uploaded to enable some processing or comparison
if uploaded_file1 and uploaded_file2:
    #st.success('Sikeres feltöltés')
    st.success('Successfull upload!')
    # You can add additional processing or comparison code here
    
    #st.button('Feldolgozás', on_click=click_button)
    st.button('Process!', on_click=click_button)
    
    if st.session_state.process:
        # The message and nested widget will remain on the page
        
        # with st.spinner('Elemezzük a képeket..'):
        with st.spinner('Analyzing images..'):
            html_data=analyze(image1,image2)
            
            # with open('./outputs/out.html','r') as f: 
            #     html_data = f.read()
            
            soup = BeautifulSoup(html_data)
            local_css(r'./frontend/analyze_style.css')
            
            # st.components.v1.html(soup.prettify(),width=768, scrolling=True)
            st.markdown(soup.prettify(),unsafe_allow_html=True)
        
        #with st.spinner('Készítjük a vizualizációt...'):
        with st.spinner('Creating visualization...'):
            gif=create_gif(image1,image2)
            
            if len(gif)>0:
                left_co,last_co = st.columns(2)
                col1, col2, col3 = st.columns([1,4,2])

                with col1:
                    st.write("")
                
                with col2:
                    st.image("./outputs/morph3b.gif",width=400,caption='BeauSTORY')
                
                with col3:
                    with open(r'./outputs/morph3b.gif', "rb") as file:
                        btn = st.download_button(
                                # label="Letöltés",
                                label="Download",
                                data=file,
                                file_name='beaustory.gif',
                                mime="gif"
              
          )
            else:
                # st.text("Sajnos a kezelés eredményét nem tudjuk vizualizálni!")
                st.text("Could not visualize the result of the treatment!")
        # with open("./outputs/morph3b.gif", "rb") as f:
        #     # contents = f.read()
        #     # data_url = base64.b64encode(contents).decode("utf-8")

        #     # st.markdown(
        #     #     f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        #     #     unsafe_allow_html=True,
        #     # )

        st.session_state.process=False