import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
    
data_path = "./data/"
sample_path = data_path + "your_sample/"
pre_path = data_path + "pre_run/"

def repeat_values(x_reduced, repeat_factor=4):
    return np.repeat(np.repeat(x_reduced, repeats=repeat_factor, axis=0), repeats=repeat_factor, axis=1)

def plot_pai_us(pai, us, s, w):
    col1, col2 = st.columns(2)
    col1.image(pai[:, :, w], clamp=True, use_column_width=True, caption = f"PA measurement: slice {s}, wavelength {wave} nm")
    col2.image(us, clamp=True, use_column_width=True, caption = f"US measurement: slice {s}")
    
# Title
st.set_page_config(layout="wide")
st.title('Your melanoma analysis framework')
"""
This webapp presents a clearer overview of the processing framework step by step, allowing the user to interact with the sample and fully understand my algorithm.
"""

with st.sidebar:
    "Select a sample to process and find out how deep is the tumour!"
    # Sample choice
    q = st.selectbox("Pick a sample!", ['018'])

st.divider()

st.subheader("Take a peak at the raw data first...")
st.write("The 3-dimensional sample con be visualised slice by slice for an easier analysis. Pick a slice and wavelength to look at, and run!")

cols = st.columns(2)
with cols[0]:
    s = st.slider("Sample's cross-section:", 0, 36, key=1)
    run = st.toggle('RUN', key=2) 
with cols[1]:
    wave = st.slider("PA Wavelength [nm]:", 670, 960, step=5, key=3)
    w = int(wave/59)
    pre = st.toggle("Pre-process data", key=4) 

if run or pre:
    pai = np.load(pre_path + f"pai_reduced_{s}.npy")
    pai = repeat_values(pai)
    us = np.load(pre_path + f"us_{s}.npy")

if run:  
    plot_pai_us(pai, us, s, w)

if pre:
    pai_ready = np.load(pre_path + f"pai_ready_reduced_{s}.npy")
    pai_ready = repeat_values(pai_ready)
    us_ready = np.load(pre_path + f"us_ready_{s}.npy")
    st.success('Data has been processed.')
    plot_pai_us(pai_ready, us_ready, s, w)    
