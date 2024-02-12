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
from PIL import Image
# import base64
# import pandas as pd

from face_analysis import analyze
from morph import create_gif

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def click_button():
    st.session_state.process = True

# Set the title of the app
st.title('BeauSTORY')

if 'process' not in st.session_state:
    st.session_state.process = False

# Create two columns for uploading images
col1, col2 = st.columns(2)

with col1:
    # Create a file uploader to allow users to upload an image
    uploaded_file1 = st.file_uploader("Kezelés előtti fotó...", type=['jpg', 'jpeg', 'png'], key='1')
    if uploaded_file1 is not None:
        # Display the uploaded image
        image1 = Image.open(uploaded_file1)
        st.image(image1, caption='Kezelés előtt', use_column_width=True)

with col2:
    # Create another file uploader for the second image
    uploaded_file2 = st.file_uploader("Kezelés utáni fotó...", type=['jpg', 'jpeg', 'png'], key='2')
    if uploaded_file2 is not None:
        # Display the second uploaded image
        image2 = Image.open(uploaded_file2)
        st.image(image2, caption='Kezelés után', use_column_width=True)

# Check if both images have been uploaded to enable some processing or comparison
if uploaded_file1 and uploaded_file2:
    st.success('Sikeres feltöltés')
    # You can add additional processing or comparison code here
    

    st.button('Feldolgozás', on_click=click_button)
    
    if st.session_state.process:
        # The message and nested widget will remain on the page
        html_data=analyze(image1,image2)

        
        # with open('./outputs/out.html','r') as f: 
        #     html_data = f.read()
        # soup = BeautifulSoup(html_data)
        # st.components.v1.html(soup.prettify(),width=768, scrolling=True)
        local_css(r'./frontend/analyze_style.css')
        # st.components.v1.html(html_data,width=768, scrolling=True)
        st.markdown(html_data,unsafe_allow_html=True)
        
        gif=create_gif(image1,image2)
        
        if len(gif)>0:
            st.image("./outputs/morph3b.gif",width=768)
        else:
            st.text("Sajnos az arc szépülését nem tudjuk vizualizálni!")
        # with open("./outputs/morph3b.gif", "rb") as f:
        #     # contents = f.read()
        #     # data_url = base64.b64encode(contents).decode("utf-8")

        #     # st.markdown(
        #     #     f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        #     #     unsafe_allow_html=True,
        #     # )

        st.session_state.process=False