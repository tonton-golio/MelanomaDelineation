import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from tqdm import tqdm

# set paths
data_path = "./data/"
sample_path = data_path + "your_sample/"
training_path = data_path + "training_data/"
pre_path = "./data/pre_run/"

# load some data
thickness = np.load(pre_path + f'thickness.npy')

st.set_page_config(layout="wide")
st.subheader("Training points collection")   

st.divider()

cols = st.columns([1, 1])
with cols[0]:
    """
    This page presents the results of the 1-dimensional convolutional neural network on the spectra of each pixel.
    The predicted tumour thickness is determined for each slice of the sample: use the slider to guide your selection of the slice to look at.

    """

    if st.toggle(f'Deepest point: **{round(max(thickness),2)} mm**', key=1):   # set to toggle deepest point
        s = np.argmax(thickness)
    else:     
        s = st.slider("Sample's cross-section:", 0, 36, key=3, value=10)


    fig, ax = plt.subplots(figsize=(6, 1))
    ax.plot(thickness)
    ax.axvline(x=s, color='r', linestyle='--', label='Selected slice')
    plt.legend(loc='upper left')
    plt.grid()
    plt.title('Tumour thickness')
    plt.xlabel('Slice')
    plt.ylabel('Thickness [mm]')
    st.pyplot(fig, use_container_width=True)

# load some data
pai_ready = np.load(pre_path + f'pai_ready_reduced_{s}.npy')

t_coord = np.load(pre_path + f'predicted_tumour_coord_{s}.npy')

with cols[1]:

    fig, ax = plt.subplots(figsize=(5, 6))
    plt.axis('off')
    plt.imshow(pai_ready[:, :, 0], cmap='gray', norm=LogNorm(clip=True), aspect='auto') 
    plt.scatter(t_coord[:, 2], t_coord[:, 1], s = 0.5, color = 'orangered', label='Predicted tumour pixels')

    plt.legend(markerscale=15)
    if t_coord.size == 0:
        st.write('##### No tumour pixels here, try changing slice!')
    st.pyplot(fig, use_container_width=True)
