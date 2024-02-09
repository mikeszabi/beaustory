#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:06:26 2024

@author: szabi
"""

import streamlit as st
from PIL import Image

# Set the title of the app
st.title('BeauSTORY')

# Create two columns for uploading images
col1, col2 = st.columns(2)

with col1:
    # Create a file uploader to allow users to upload an image
    uploaded_file1 = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'], key='1')
    if uploaded_file1 is not None:
        # Display the uploaded image
        image1 = Image.open(uploaded_file1)
        st.image(image1, caption='Before image', use_column_width=True)

with col2:
    # Create another file uploader for the second image
    uploaded_file2 = st.file_uploader("Choose another image...", type=['jpg', 'jpeg', 'png'], key='2')
    if uploaded_file2 is not None:
        # Display the second uploaded image
        image2 = Image.open(uploaded_file2)
        st.image(image2, caption='After image', use_column_width=True)

# Check if both images have been uploaded to enable some processing or comparison
if uploaded_file1 and uploaded_file2:
    st.success('Both images have been uploaded successfully.')
    # You can add additional processing or comparison code here
