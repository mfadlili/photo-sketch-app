import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from PIL import Image

st.set_page_config(
    page_title="Photo Sketch App",
    page_icon='✏️',
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/mfadlili',
        'Report a bug': "https://github.com/mfadlili",
        'About': "# This application was built by Fadlil"
    }
)

st.title('Photo Sketch App')
st.image('draw-with-one-pencil-final.jpg')

th = st.slider("Select Threshold", 0, 100, 10)

select = st.selectbox('Please select image source:', ('Upload image', 'Take a photo'))

def converter(input, thr):
    img = Image.open(input)
    imgGray = img.convert('L')
    dx1, dy1 = np.gradient(imgGray)

    magnitude = (dx1**2+dy1**2)**0.5
    threshold = np.where(magnitude>=thr, 0, 255)
    im = Image.fromarray(np.uint8(cm.gist_earth(threshold)*255))
    hasil = im.convert('1')

    return hasil

if select=='Upload image':
    file = st.file_uploader("", type=["jpg","png"])
    col1, col2, col3 = st.columns(3)

    with col2:
        if st.button('Show the image'):
            if file is not None:
                st.image(file)

    with col1:
        if st.button('Draw'):
            result = converter(file, th)
            st.image(result)
            result.save('result.jpg')
            with open("result.jpg", "rb") as file:
                btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name="result.jpg",
                    mime="image/png"
                )

else:
    picture = st.camera_input('Ambil foto anda.')
    if st.button('Draw'):
        result = converter(picture, th)
        st.image(result)
        result.save('result.jpg')
        with open("result.jpg", "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name="result.jpg",
                mime="image/png"
            )