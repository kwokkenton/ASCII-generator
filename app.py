import streamlit as st

from img2img_color import image_to_image
from video2video_color import video_to_video

IMAGE = False
if IMAGE:
    input_path = 'data/img.jpg'
    output_path = 'data/out.jpg'
else: 
    input_path = 'data/in.mp4'
    output_path = 'data/out.gif'

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Only show input elements if not submitted
if not st.session_state.submitted:
    st.title("Tell Me a Secret")

    sentence = st.text_input("Your secret is safe with me.")
    if st.button("Transform!"):

        if IMAGE:
            options = {
            "input": input_path,
            "output": output_path,
            "sentence": sentence,
            "language": "english",
            "mode": "standard",
            "background": "black",
            "scale": 2,
            "num_cols": 60,
        }
            image_to_image(options)
        else:
            options = {
            "input": input_path,
            "output": output_path,
            "sentence": sentence,
            "language": "english",
            "mode": "standard",
            "background": "black",
            "scale": 2,
            "num_cols": 60,
            'fps' : 0
        }
            video_to_video(options)
        st.session_state.submitted = True  # Hide inputs in the next rerun
        st.rerun()
else:
    if IMAGE:
        st.image(output_path, use_container_width=True)
    else:
        st.image(output_path, use_container_width=True)
        st.markdown("<p style='text-align: center; '>Don't worry, it's gone now</p>", unsafe_allow_html=True)