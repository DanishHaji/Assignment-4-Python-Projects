import qrcode
import cv2

def generate_qr_code(data, file_name):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")  # Fixed typo "blobk" -> "black"
    img.save(file_name)
    print(f"QR code generated and saved as {file_name}")

def decode_qr_code(file_name):
    img = cv2.imread(file_name)
    qr_decoder = cv2.QRCodeDetector()

    data, _, _ = qr_decoder.detectAndDecode(img)
    if data:
        print(f"Decoded data: {data}")
        return data
    else:
        print("No QR code found in the image")
        return None

if __name__ == "__main__":
    qr_file = "hello_world.png"
    generate_qr_code("Hello, World!", qr_file)

    decoded_data = decode_qr_code(qr_file)
    if decoded_data:
        print(f"Successfully decoded: {decoded_data}")
