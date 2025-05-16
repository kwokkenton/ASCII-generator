import streamlit as st

from img2img_color import main_new  # Your function

input_path = 'data/img.jpg'
output_path = 'data/out.jpg'

# Initialize session state
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Only show input elements if not submitted
if not st.session_state.submitted:
    st.title("Larissa at N+")

    sentence = st.text_input("What is a secret or something you would be scared to say?")
    if st.button("surprise!"):
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
        main_new(options)
        st.session_state.submitted = True  # Hide inputs in the next rerun
        st.rerun()
else:
    # Only show the output image if submission has occurred
    st.image(output_path, use_container_width=True)