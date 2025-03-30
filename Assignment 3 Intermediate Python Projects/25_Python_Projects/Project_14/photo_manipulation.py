from PIL import Image, ImageEnhance, ImageFilter

def apply_filters(image_path, brightness=1.2, contrast=1.5, blur_radius=2):
    """Applies brightness, contrast, and blur effects to an image."""

    try:
        # Open the Image
        img = Image.open(image_path)
        img.show(title="Original Image") # show original image

        # Apply brightness enhancement
        enhancer = ImageEnhance.Brightness(img)
        img_bright = enhancer.enhance(brightness)

        # Apply contrast enhancement
        enhancer = ImageEnhance.Contrast(img_bright)
        img_contrast = enhancer.enhance(contrast)

        # Apply blus filter
        img_blur = img_contrast.filter(ImageFilter.GaussianBlur(blur_radius))

        # Show modified image
        img_blur.show(title = "Modified Image")

        # Save the modified image
        modified_image_path = "modified_image.jpeg"
        img_blur.save(modified_image_path)
        print(f"✅ Image processed successfully! Saved as {modified_image_path}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

image_path = "image.jpeg"
apply_filters(image_path)

