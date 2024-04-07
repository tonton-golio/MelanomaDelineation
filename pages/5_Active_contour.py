import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from tqdm import tqdm
import base64

# path stuff
data_path = "./data/"
sample_path = data_path + "your_sample/"
pre_path = "./data/pre_run/"

# title and layout
st.set_page_config(layout="wide")
st.subheader("Active contour algorithm")   
st.divider()

cols_ = st.columns([4, 1])

with cols_[0]:
    st.write('The contour moves to minimise a weighted sum of energies: gravitational pull from the center of mass, stifness and homogeneousity of the contour and finally our sandpiles results.')

with cols_[1]:
    st.write('#')
    run = st.toggle(f'RUN', key=41)

colls = st.columns([2, 1])

if run == True:
    with colls[0]:
        st.video(pre_path + 'active_contour.mp4', loop = True)

    with colls[1]:
        st.write('#')

    tryit = st.toggle(f'Try it yourself!', key=51)
    cols_ = st.columns([3, 1])

    with cols_[1]:
        if tryit == True:
            st.image('./data/qr.png')