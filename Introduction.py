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
    col1.image(np.log(pai[:, :, w])/np.log(pai[:, :, w]).max(), clamp=True, use_column_width=True, caption = f"PA measurement: slice {s}, wavelength {wave} nm")
    col2.image(us, clamp=True, use_column_width=True, caption = f"US measurement: slice {s}")
    
# Title
st.set_page_config(layout="wide")
st.title('Automatic delineation framework for melanoma detection')

ccols = st.columns([3, 1])

with ccols[0]:
    """
    In this webapp you will find an overview of the full algorithm I developed to analyse phoacoustic imaging data and determine tumour thickness and outline. Step by step, you can explore the sample and interact the algorithm's parameters.
    """
with ccols[1]:
    st.image('./data/setup.png')

with st.sidebar:
    "Select a sample to process and find out how thick is the tumour!"
    # Sample choice
    q = st.selectbox("Pick a sample!", ['demo_sample'])

st.divider()

st.subheader("- Take a peak at the photoacoustic (PA) and ultrasound imaging data (US) -")
st.write("Measurements are acquired through consecutive cross imaging sections: move the slider to select which of the slices to visualise and run! Then click on pre-process data to segment the backgound noise from the sample.")

cols = st.columns(2)
with cols[0]:
    s = st.slider("Slice:", 0, 36, key=1)
    run = st.toggle('RUN', key=2) 
with cols[1]:
    wave = st.slider("PA Wavelength [nm]:", 670, 960, step=5, key=3)
    w = int(wave/59)
    pre = st.toggle("Pre-process data", key=4) 

if run or pre:
    pai = np.load(pre_path + f"pai_reduced_{s}.npy")
    pai_r = repeat_values(pai)
    us = np.load(pre_path + f"us_{s}.npy")

if run:  
    plot_pai_us(pai_r, us, s, w)

if pre:
    pai_ready = np.load(pre_path + f"pai_ready_reduced_{s}.npy")
    pai_ready_r = repeat_values(pai_ready)
    us_ready = np.load(pre_path + f"us_ready_{s}.npy")
    st.success('Data has been processed.')
    plot_pai_us(pai_ready_r, us_ready, s, w)    
