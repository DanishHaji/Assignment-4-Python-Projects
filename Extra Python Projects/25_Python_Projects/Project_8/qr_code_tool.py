import streamlit as st
import qrcode
import cv2
from PIL import Image
import io
import numpy as np


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img


def decode_qr_code(img):
    qr_decoder = cv2.QRCodeDetector()
    data, _, _ = qr_decoder.detectAndDecode(img)
    return data


def main():
    # Title
    st.title("QR Code Generator and Decoder")
    st.write("This is a simple app to generate and decode QR codes.")

    
    option = st.sidebar.selectbox("Choose an option", ("Generate QR Code", "Decode QR Code"))

    if option == "Generate QR Code":
        st.subheader("Generate QR Code")

        
        data = st.text_area("Enter the data for the QR Code:", 
                          placeholder="Enter text or a link",
                          key="qr_data")
        
        # Generate QR code button
        generate_button = st.button("Generate QR Code")
        
        if generate_button and data:
            # Generate QR code if input is provided and button is clicked
            img = generate_qr_code(data)

            # Convert the image to bytes for Streamlit to handle it
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)

            # Display the generated QR code image
            st.image(buf, caption="Generated QR Code", use_container_width=True)

            # Save the QR code and give the option to download
            st.download_button("Download QR Code", buf, "qrcode.png", "image/png")
        elif generate_button and not data:
            st.warning("Please enter some data to generate a QR code")

    elif option == "Decode QR Code":
        st.subheader("Decode QR Code")

        # File uploader for QR code image
        uploaded_file = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])

        if uploaded_file:
            try:
                
                img = Image.open(uploaded_file)
                st.image(img, caption="Uploaded QR Code", use_container_width=True)

                # Convert the PIL image to a NumPy array
                img_cv = np.array(img)

                # Ensure the image is in the correct format for OpenCV
                if img_cv.ndim == 2:  
                    img_processed = img_cv
                elif img_cv.ndim == 3 and img_cv.shape[2] == 3:  # RGB image
                    img_processed = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
                elif img_cv.ndim == 3 and img_cv.shape[2] == 4:  # RGBA image
                    img_processed = cv2.cvtColor(img_cv, cv2.COLOR_RGBA2GRAY)
                else:
                    st.error("Unsupported image format.")
                    return

                # Convert image to OpenCV-compatible data type
                img_processed = np.ascontiguousarray(img_processed, dtype=np.uint8)

                # Resize if the image is too large (helps with detection)
                height, width = img_processed.shape[:2]
                max_size = 1000
                if height > max_size or width > max_size:
                    scale = max_size / max(height, width)
                    img_processed = cv2.resize(img_processed, None, fx=scale, fy=scale)

                _, img_processed = cv2.threshold(img_processed, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

                # Decode the QR code
                decoded_data = decode_qr_code(img_processed)

                if decoded_data:
                    st.success(f"Decoded Data: {decoded_data}")
                else:
                    _, img_inverted = cv2.threshold(img_processed, 127, 255, cv2.THRESH_BINARY_INV)
                    decoded_data = decode_qr_code(img_inverted)
                    
                    if decoded_data:
                        st.success(f"Decoded Data (after inversion): {decoded_data}")
                    else:
                        st.warning("No QR code detected in the image. Try with a clearer image.")

            except Exception as e:
                st.error(f"Error processing the image: {str(e)}")

if __name__ == "__main__":
    main()