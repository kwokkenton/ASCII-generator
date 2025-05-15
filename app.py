import tempfile

import streamlit as st

from img2img_color import main_new  # Assuming your function is in main.py

st.title("Image to ASCII Converter")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # Save uploaded file to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_file.getbuffer())
        input_path = tmp.name

    # Slider for number of columns
    num_cols = st.slider("Number of columns", min_value=10, max_value=300, value=150, step=10, help='Higher means font size is smaller')

    sentence = st.text_input("Enter your sentence", value="Message here.")

    # Output path
    output_path = input_path.replace(".jpg", "_ascii.jpg")

    options = {
        "input": input_path,
        "output": output_path,
        "sentence": sentence,
        "language": "english",
        "mode": "standard",
        "background": "black",
        "scale": 2,
        "num_cols": num_cols
    }

    if st.button("🎨 Convert to ASCII"):
        main_new(options)
        st.image(output_path, caption="ASCII Art Output", use_container_width=True)