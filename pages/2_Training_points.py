import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def repeat_values(x_reduced, repeat_factor=4):
    return np.repeat(np.repeat(x_reduced, repeats=repeat_factor, axis=0), repeats=repeat_factor, axis=1)
    
# path stuff
data_path = "./data/"
sample_path = data_path + "your_sample/"
pre_path = "./data/pre_run/"

def load_coord(s, type):
    coord = np.load(pre_path + type + "_coord_" + str(s) + ".npy")
    return coord

# title and layout
st.set_page_config(layout="wide")
st.subheader("Training points collection")   
st.divider()

cols = st.columns([1, 1])
thickness = np.load(pre_path + f'thickness.npy')
with cols[0]:
    """
    This page shows how the training data for the neural network are systematically obtained from each individual sample.
    Given the absence of a ground truth, the data are labelled according to the results of k-means clustering.
    A thin border between the two clusters is left unlabelled due to the lack of ground truth data about the tumour outline.
    """

    if st.toggle(f'Slice with the largest non-healthy labelled cluster', key=99):   # set to toggle deepest point
        s = np.argmax(thickness)
    else:     
        s = st.slider("Sample's cross-section:", 0, 36, key=98, value=10)

# load some data

pai_ready = np.load(pre_path + f'pai_ready_reduced_{s}.npy')
pai_ready = repeat_values(pai_ready)
t_coord = load_coord(s, 'tumour')
h_coord = load_coord(s, 'healthy')

# compute average spectra
def average_spectra(s, pai_ready, t_coord, h_coord):
    wavelengths = np.linspace(670, 960, 59)  
    h_spectra = np.average(pai_ready[h_coord[:,1], h_coord[:,2]], axis = 0)
    t_spectra = np.average(pai_ready[t_coord[:,1], t_coord[:,2]], axis = 0)
    return wavelengths, t_spectra, h_spectra

def plot_pai_us(pai, us, s, w, pai_log=True):
    wavelengths, t_spectra, h_spectra = average_spectra(s, pai_ready, t_coord, h_coord)

    fig, ax = plt.subplots(figsize=(5,2))
    plt.grid()
    plt.title('Average spectra of visualised training points')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)   
    
    if t_coord.size != 0:
        plt.plot(wavelengths, t_spectra,color = 'orangered', label='Non-healthy cluster')
    plt.plot(wavelengths, h_spectra, color = 'green', label='Healthy cluster')
    plt.legend()
    plt.xlabel('wavelength [nm]')
    plt.ylabel('Photoacoustic intensity [a.u.]')
    st.pyplot(fig, use_container_width=True)

with cols[0]:
    plot_pai_us(pai_ready, pai_ready, s, 0, pai_log=True)

with cols[1]:
    fig, ax = plt.subplots(figsize=(5, 6))
    plt.axis('off')
    plt.imshow(pai_ready[:, :, 0], cmap='gray', norm=LogNorm(clip=True), aspect='auto')
    plt.scatter(t_coord[:, 2], t_coord[:, 1], s = 0.5, color = 'orangered', label='Non-healthy cluster')
    plt.scatter(h_coord[:, 2][::2], h_coord[:, 1][::2], s = 1, color = 'darkgreen', label='Healthy cluster', alpha=.12  )

    # plot legend with larger markerrs, and increased alpha =1
    markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in ['orangered', 'darkgreen']]
    plt.legend(markers, ['Non-healthy cluster', 'Healthy cluster'], numpoints=1, loc='upper right', markerscale=1)
    if t_coord.size == 0:
        st.write('##### No non-healthy pixels here, try changing slice!')
    st.pyplot(fig, use_container_width=True)
