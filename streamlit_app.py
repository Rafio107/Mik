import os
import io
import zipfile
from pathlib import Path
import streamlit as st
from PIL import Image, ImageOps
from rembg import remove

# Constants
MAX_FILES = 5
ALLOWED_TYPES = ["png", "jpg", "jpeg"]

# Set up page configuration
st.set_page_config(page_title="Linear Algebra Group 6", page_icon="🌟")

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
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to resize and pad images
def resize_and_pad(image, target_size=(300, 300), color=(255, 255, 255)):
    """Resize and pad an image to the target size while maintaining aspect ratio."""
    return ImageOps.pad(image, target_size, color=color)

# Hide default styles and apply custom styles
hide_streamlit_style()

# Add a place for a top logo or image at the top of all pages
top_image_path = Path("Logo PUS.jpeg")  # Ganti dengan path gambar logo Anda
if top_image_path.exists():
    logo_image = Image.open(str(top_image_path))
    st.image(logo_image, width=150)  # Sesuaikan ukuran logo dengan width
else:
    st.warning("Top image not found.")

# Navigation menu
menu = st.sidebar.selectbox("Select a Page", ["Home", "Group Members", "Background Remover"])

if menu == "Home":
    # Content for the home page
    st.markdown("<h1>Linear Algebra Group 3</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Welcome to Background Remover</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        Instruksi untuk menggunakan fitur Background Remover:
        1. Unggah gambar dengan format **PNG**, **JPG**, atau **JPEG**.
        2. Anda dapat mengunggah hingga 5 gambar sekaligus.
        3. Tekan tombol **Remove Background** untuk memproses gambar.
        4. Setelah diproses, unduh gambar yang telah dihapus background-nya secara individual atau dalam bentuk file ZIP jika lebih dari satu gambar.
        """,
        unsafe_allow_html=True,
    )

elif menu == "Group Members":
    # Mapping names to image paths and roles
    anggota = [
        {"name": "Muhammad Rafi Akbar", "image": "M.Rafi Akbar.jpg", "position": "Kang Gendong"},
        {"name": "Rifki Ibithal Eka Sambudi", "image": "Gambar rifki.jpg", "position": "Leader"},
        {"name": "Aulia Rahma Mulya", "image": "Gambar aul 2.jpg", "position": "Beban"},
        {"name": "Florenza Natania", "image": "Gambar flo.jpg", "position": "Beban"},
    ]

    st.markdown("<h2 style='text-align: center;'>Group Members - Group 3</h2>", unsafe_allow_html=True)

    # Display members in a grid-like format
    col1, col2, col3, col4 = st.columns(4)  # Adjust column layout if needed
    columns = [col1, col2, col3, col4]

    for idx, member in enumerate(anggota):
        with columns[idx % 4]:
            image_path = Path(member["image"])
            if image_path.exists():
                original_image = Image.open(image_path)
                resized_image = resize_and_pad(original_image, target_size=(300, 300))  # Adjust size
                st.image(resized_image, caption=member["name"], use_container_width=False)
                st.markdown(
                    f"<p style='text-align: center;'>{member['position']}</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.warning(f"Image for {member['name']} not found: {member['image']}")

elif menu == "Background Remover":
    uploaded_files = st.file_uploader(
        label="Upload your images", type=ALLOWED_TYPES, accept_multiple_files=True
    )

    if uploaded_files:
        # Process the images and remove the background
        if st.button("Remove Background", key="remove_btn"):
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
                    st.image(original, caption="Original", use_container_width=True)
                with col2:
                    st.image(result, caption="Processed", use_container_width=True)

            # Provide option to download images as a zip file
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

        # Geometry transformation section
        st.markdown("<h3>Geometry Transformations</h3>", unsafe_allow_html=True)
        transform_option = st.selectbox("Select Transformation", ["None", "Rotasi", "Translasi", "Scaling", "Shear"])

        if transform_option != "None" and uploaded_files:
            for uploaded_file in uploaded_files:
                image = Image.open(uploaded_file)

                if transform_option == "Rotasi":
                    angle = st.slider("Pilih Sudut Rotasi", min_value=-180, max_value=180, value=0)
                    rotated_image = image.rotate(angle, expand=True)
                    st.image(rotated_image, caption=f"Rotated Image {angle}°", use_container_width=True)

                elif transform_option == "Translasi":
                    tx = st.slider("Translasi pada sumbu X", min_value=-100, max_value=100, value=0)
                    ty = st.slider("Translasi pada sumbu Y", min_value=-100, max_value=100, value=0)
                    translated_image = ImageOps.offset(image, tx, ty)
                    st.image(translated_image, caption=f"Translated Image ({tx}, {ty})", use_container_width=True)

                elif transform_option == "Scaling":
                    scale_x = st.slider("Skala pada sumbu X", min_value=0.5, max_value=2.0, value=1.0)
                    scale_y = st.slider("Skala pada sumbu Y", min_value=0.5, max_value=2.0, value=1.0)
                    scaled_image = image.resize((int(image.width * scale_x), int(image.height * scale_y)))
                    st.image(scaled_image, caption=f"Scaled Image ({scale_x}, {scale_y})", use_container_width=True)

                elif transform_option == "Shear":
                    shear_factor = st.slider("Shear Factor", min_value=-1.0, max_value=1.0, value=0.0)
                    shear_matrix = (1, shear_factor, 0, 0, 1, 0)
                    sheared_image = image.transform(image.size, Image.AFFINE, shear_matrix)
                    st.image(sheared_image, caption=f"Sheared Image (Factor: {shear_factor})", use_container_width=True)

    else:
        st.warning("Please upload at least one image.")

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 2rem;">
        Developed by <a href="mailto:rafiotsuka@gmail.com">rafiotsuka@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True,
)
