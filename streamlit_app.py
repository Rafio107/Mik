import io
import zipfile
from pathlib import Path
import streamlit as st
from PIL import Image
from rembg import remove
import uuid
import base64

# Constants
MAX_FILES = 5
ALLOWED_TYPES = ["png", "jpg", "jpeg"]

# Set up page configuration
st.set_page_config(page_title="Background Remover", page_icon="🌟")

def hide_streamlit_style():
    """Applies custom styles to the Streamlit app."""
    st.markdown(
        """
        <style>
        body {
            font-family: Arial, sans-serif;
        }
        .block-container {
            padding: 2rem;
        }
        header {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        .custom-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem;
            background-color: #f5f5f5;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        .custom-container .left {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        .custom-container h1 {
            margin: 0;
            font-size: 2rem;
            color: #333;
        }
        .custom-container p {
            margin: 0;
            color: #777;
        }
        .custom-container .right {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #555;
        }
        .footer a {
            color: #007bff;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Hide default styles and apply custom styles
hide_streamlit_style()

# Navigation menu
menu = st.sidebar.selectbox("Pilih Menu", ["Remove Background", "Anggota - Group 3"])

if menu == "Remove Background":
    uploaded_files = st.file_uploader(
        label="", type=ALLOWED_TYPES, accept_multiple_files=True
    )

    if st.button("Remove Background", key="remove_btn"):
        if uploaded_files:
            if len(uploaded_files) > MAX_FILES:
                st.warning(f"Maximum {MAX_FILES} files can be processed.")
                uploaded_files = uploaded_files[:MAX_FILES]

            results = []
            with st.spinner("Processing images..."):
                for uploaded_file in uploaded_files:
                    original_image = Image.open(uploaded_file).convert("RGBA")
                    result_image = remove(uploaded_file.getvalue())
                    results.append((original_image, Image.open(io.BytesIO(result_image)).convert("RGBA"), uploaded_file.name))

            for original, result, name in results:
                st.markdown(
                    f"<h4>Result for {name}</h4>", unsafe_allow_html=True
                )
                col1, col2 = st.columns(2)
                with col1:
                    st.image(original, caption="Original", use_column_width=True)
                with col2:
                    st.image(result, caption="Processed", use_column_width=True)

            if len(results) > 1:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                    for _, result, name in results:
                        buf = io.BytesIO()
                        result.save(buf, format="PNG")
                        zip_file.writestr(f"{Path(name).stem}_nobg.png", buf.getvalue())

                st.download_button(
                    label="Download All as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="background_removed_images.zip",
                    mime="application/zip",
                )
            else:
                result = results[0][1]
                buf = io.BytesIO()
                result.save(buf, format="PNG")
                st.download_button(
                    label="Download Processed Image",
                    data=buf.getvalue(),
                    file_name=f"{Path(results[0][2]).stem}_nobg.png",
                    mime="image/png",
                )
        else:
            st.warning("Please upload at least one image.")

    st.markdown(
        """
        <div style="margin-top: 2rem; padding: 1rem; background-color: #f5f5f5; border-radius: 10px;">
            <h3>Instructions:</h3>
            <ul>
                <li>Upload up to 5 images at once (JPG or PNG format).</li>
                <li>Click "Remove Background" to process the images.</li>
                <li>Download processed images individually or as a ZIP file.</li>
            </ul>
        </div>
        <div style="margin-top: 2rem;">
            <h3>Example:</h3>
            <div style="display: flex; flex-direction: row; gap: 1rem; align-items: center;">
                <div>
                    <h4>Original Image</h4>
                    <img src="images raiden ei.jpg" alt="Original" style="border: 1px solid #ddd; border-radius: 4px; padding: 5px; width: 150px;">
                </div>
                <div>
                    <h4>Processed Image</h4>
                    <img src="images raiden ei_nobg.png" alt="Processed" style="border: 1px solid #ddd; border-radius: 4px; padding: 5px; width: 150px;">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

elif menu == "Anggota - Group 3":
    # Mapping names to image paths
    anggota = {
        "Muhammad Rafi Akbar": "images/rafi.jpg",
        "Rifki Ibithal Eka Sambudi": "Gambar rifki.jpg",
        "Aulia Rahma Mulya": "images/aulia.jpg",
        "Florenza Natania": "images/florenza.jpg",
    }

    st.markdown("<h2>Anggota - Group 3</h2>", unsafe_allow_html=True)

    for name, image_path in anggota.items():
        if st.button(name):
            try:
                st.image(image_path, caption=name, width=150)  # Set width to make image smaller
            except FileNotFoundError:
                st.warning(f"Gambar untuk {name} tidak ditemukan.")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memuat gambar untuk {name}: {e}")

# Footer
st.markdown(
    """
    <div class="footer">
        Developed by <a href="mailto:rafiotsuka@gmail.com">rafiotsuka@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True,
)
