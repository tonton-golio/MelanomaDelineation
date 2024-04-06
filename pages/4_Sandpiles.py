import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from tqdm import tqdm
import plotly.graph_objs as go

# path stuff
data_path = "./data/"
sample_path = data_path + "your_sample/"
pre_path = "./data/pre_run/"

@st.cache_data
def load_sand():
    sand_init = np.load(pre_path + "sand_castle_init.npy")
    sand_final = np.load(pre_path + "sand_castle_final.npy")
    return sand_init, sand_final

# title and layout
st.set_page_config(layout="wide")
st.subheader("The sandpiles algorithm")   
st.divider()

s = 20
# load some data
sand_init, sand_final = load_sand()

def plot_2d(sand):
    fig, ax = plt.subplots()  
    plt.imshow(sand)
    plt.axis('off')
    plt.colorbar()
    return fig, ax

cols_ = st.columns([4, 1])

with cols_[0]:
    st.write('Imagine iteratively pouring sand on each pixel proportionally to our predictions and letting it share thourgh pixels. This alllows us to create a smooth 3D energy landscape for contouring.')

with cols_[1]:
    st.write('#')
    run = st.toggle(f'RUN', key=531)

cols = st.columns([1, 1])

with cols[0]:
    st.write('Sinks initialisation')
    fig_i, ax = plot_2d(sand_init)
    st.pyplot(fig_i, use_container_width=True)

with cols[1]:
    if run == True:
        st.write('Final sandpiles')
        fig_f, ax = plot_2d(sand_final)
        st.pyplot(fig_f, use_container_width=True)

if run == True:
    st.write('3D view of the final sandpiles')

    sand_2 = np.load(pre_path + 'sand_castle_final.npy')

    sand_2[20][sand_2[20] < -40] = -15
    x = np.arange(sand_2[20].shape[1])
    y = np.arange(sand_2[20].shape[0])
    X, Y = np.meshgrid(x, y)

    heatmap = go.Surface(x=X, y=Y, z=sand_2[20], colorscale='Viridis')

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z'),
            aspectratio=dict(x=1, y=1, z=0.7),
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.6)),
        )
    )

    fig = go.Figure(data=[heatmap], layout=layout)

    st.plotly_chart(fig)
