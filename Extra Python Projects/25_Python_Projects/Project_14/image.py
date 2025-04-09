import streamlit as st
import numpy as np
from PIL import Image as PILImage
import io

# Resize image for faster processing
def resize_image(image, max_width=800, max_height=800):
    y, x, _ = image.shape
    scale = min(max_width / x, max_height / y, 1)
    new_x, new_y = int(x * scale), int(y * scale)
    resized_image = np.array(PILImage.fromarray((image * 255).astype(np.uint8)).resize((new_x, new_y))) / 255
    return resized_image

# Simple blur without scipy (using averaging kernel manually)
def simple_blur(image, kernel_size):
    pad = kernel_size // 2
    padded_image = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='reflect')
    blurred = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i+kernel_size, j:j+kernel_size]
            blurred[i, j] = np.mean(region, axis=(0, 1))
    return blurred

# Apply manipulations
def apply_manipulations(image, brightness=1.0, contrast=1.0, blur_kernel=1, grayscale=False, flip_h=False, sepia=False):
    manipulated_image = image.copy()

    if brightness != 1.0:
        manipulated_image *= brightness

    if contrast != 1.0:
        mid = 0.5
        manipulated_image = (manipulated_image - mid) * contrast + mid

    if blur_kernel > 1 and blur_kernel % 2 == 1:
        manipulated_image = simple_blur(manipulated_image, blur_kernel)

    if grayscale:
        gray = np.mean(manipulated_image, axis=2, keepdims=True)
        manipulated_image = np.repeat(gray, 3, axis=2)

    if flip_h:
        manipulated_image = np.fliplr(manipulated_image)

    if sepia:
        sepia_filter = np.array([[0.393, 0.769, 0.189],
                                 [0.349, 0.686, 0.168],
                                 [0.272, 0.534, 0.131]])
        manipulated_image = np.dot(manipulated_image[..., :3], sepia_filter.T)
        manipulated_image = np.clip(manipulated_image, 0.0, 1.0)

    manipulated_image = np.clip(manipulated_image, 0.0, 1.0)
    return manipulated_image

# Streamlit App
def main():
    st.title("Photo Studio Pro")
    st.sidebar.title("Photo Manipulation Options")

    uploaded_file = st.file_uploader("Upload an image file", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        original_image = np.array(PILImage.open(uploaded_file)) / 255
        st.subheader("Original Image")
        st.image(original_image, use_container_width=True)

        resized_image = resize_image(original_image)

        st.sidebar.subheader("Adjustments")
        brightness = st.sidebar.slider("Brightness", 0.1, 3.0, 1.0, 0.1)
        contrast = st.sidebar.slider("Contrast", 0.1, 3.0, 1.0, 0.1)
        blur_kernel = st.sidebar.slider("Blur Kernel Size (Odd Only)", 1, 15, 1, 2)
        grayscale = st.sidebar.checkbox("Convert to Grayscale")
        flip_h = st.sidebar.checkbox("Flip Horizontally")
        sepia = st.sidebar.checkbox("Apply Sepia Filter")

        manipulated_image = apply_manipulations(
            resized_image,
            brightness=brightness,
            contrast=contrast,
            blur_kernel=blur_kernel,
            grayscale=grayscale,
            flip_h=flip_h,
            sepia=sepia
        )

        st.subheader("Manipulated Image")
        st.image(manipulated_image, use_container_width=True)

        manipulated_image_pil = PILImage.fromarray((manipulated_image * 255).astype(np.uint8))
        buf = io.BytesIO()
        manipulated_image_pil.save(buf, format="PNG")
        st.download_button(
            label="Download Manipulated Image",
            data=buf.getvalue(),
            file_name="manipulated_image.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
