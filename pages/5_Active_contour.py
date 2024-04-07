import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from tqdm import tqdm
import time

def repeat_values(x_reduced, repeat_factor=4):
    return np.repeat(np.repeat(x_reduced, repeats=repeat_factor, axis=0), repeats=repeat_factor, axis=1)
    
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

colls = st.columns([3, 2])

if run == True:
    with colls[0]:
        st.container()
        st.video(pre_path + 'active_contour.mp4', loop = True)

    with colls[1]:
        time.sleep(4)
        pai_ready = np.load(pre_path + 'pai_ready_reduced_20.npy')
        t = np.load(pre_path + 'tumour_area.npy')
        pai_ready = repeat_values(pai_ready)
        fig, ax = plt.subplots(figsize=(5, 7))
        plt.axis('off')
        st.write('Final tumour ouline cross-section')
        plt.imshow(pai_ready[:, :, 0]/pai_ready[:, :, 0].max(), cmap='gray', norm=LogNorm(clip=True), aspect='auto') 
        plt.scatter(t[:, 1]//2, t[:, 0]//2, s = 0.5, color = 'orangered')
        st.pyplot(fig, use_container_width=True)

    tryit = st.toggle(f'Try it yourself!', key=51)
    cols_ = st.columns([3, 1])

    with cols_[1]:
        if tryit == True:
            st.image('./data/qr.png')