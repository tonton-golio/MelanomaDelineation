import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy import signal

data_path = "./data/"
sample_path = data_path + "your_sample/"
training_path = data_path + "training_data/"
pre_path = "./data/pre_run/"

@st.cache_data

def load_raw_data(s, path=pre_path):

    pai = np.load(path + f"pai_reduced_{s}.npy")
    us = np.load(path + f"us_{s}.npy")

    return pai, us

def pre_processing(path=pre_path):

    pai_ready = np.load(path + f"pai_ready_reduced_{s}.npy")
    us_ready = np.load(path + f"us_ready_{s}.npy")
    st.success('Data has been processed.')

    return us_ready, pai_ready

def plot_pai_us(pai, us, s, w, pai_log=True):
    
    if pai_log: pai = np.log(pai)
    pai_plot = pai[:, :, w]/pai.max()
    col1, col2 = st.columns(2)
    col1.image(pai_plot, clamp=True,use_column_width=True, caption = f"PA measurement: slice {s}, wavelength {wave} nm")
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
    pai, us = load_raw_data(s)

if run:  
    plot_pai_us(pai, us, s, w, True)

if pre:
    us_ready, pai_ready = pre_processing()
    plot_pai_us(pai_ready, us_ready, s, w, True)    
