import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from tqdm import tqdm

def repeat_values(x_reduced, repeat_factor=4):
    return np.repeat(np.repeat(x_reduced, repeats=repeat_factor, axis=0), repeats=repeat_factor, axis=1)
    
# set paths
data_path = "./data/"
sample_path = data_path + "your_sample/"
training_path = data_path + "training_data/"
pre_path = "./data/pre_run/"

# load some data
thickness = np.load(pre_path + f'thickness.npy')

st.set_page_config(layout="wide")
st.header("The predictions")   

st.divider()

cols = st.columns([1, 1])
with cols[0]:
    """
    A 1D convolutional neural network is trained on the labelled spectra specific to the patient and used to classify each pixel in the sample. 
    Pixels classified as tumourous are colored in red. The thickness of the tumour is calculated for each slice through an automatic algorithm. 

    """

    if st.toggle(f'Go to slice where tumour is the thickest', key=1):   # set to toggle deepest point
        s = np.argmax(thickness)
    else:     
        s = st.slider("Sample's cross-section:", 0, 36, key=3, value=10)


# load some data
pai_ready = np.load(pre_path + f'pai_ready_reduced_{s}.npy')
pai_ready = repeat_values(pai_ready)
t_coord = np.load(pre_path + f'predicted_tumour_coord_{s}.npy')

with cols[1]:

    fig, ax = plt.subplots(figsize=(5, 6))
    plt.axis('off')
    plt.imshow(pai_ready[:, :, 0], cmap='gray', norm=LogNorm(clip=True), aspect='auto') 
    plt.scatter(t_coord[:, 2], t_coord[:, 1], s = 0.5, color = 'orangered', label='Predicted tumour pixels')

    plt.legend(markerscale=15)
    if t_coord.size == 0:
        with cols[0]:
            sub_cols = st.columns([1, 6, 1])
            with sub_cols[1]:
                st.markdown(':red[Only healthy pixels here, try changing slice!]')
            st.write('#')
    else:
        with cols[0]:
            st.write('#')
            st.write('#')

    st.pyplot(fig, use_container_width=True)

with cols[0]:
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.plot(thickness)
    ax.axvline(x=s, color='r', linestyle='--', label='Selected slice')
    plt.legend(loc='upper left')
    plt.grid()
    plt.title('Tumour thickness across slices')
    plt.xlabel('Slice')
    plt.ylabel('Thickness [mm]')
    st.pyplot(fig, use_container_width=True)

    st.subheader(f'Final melanoma thickness: :red[**{round(max(thickness),2)} mm**], slice 20')
