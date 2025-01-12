from pdf2image import convert_from_path
from PIL import Image
import numpy as np

def extract_images_from_pdf(pdf_path):
    """Convert PDF pages to images."""
    images = convert_from_path(pdf_path)
    return images

def calculate_pixel_distribution(image):
    """Calculate the pixel distribution of color, black, and white."""
    # Convert the image to RGB and a NumPy array
    image = image.convert("RGB")
    np_image = np.array(image)

    # Flatten the array for easy processing
    pixels = np_image.reshape(-1, 3)
    
    # Define thresholds
    white_threshold = 245
    black_threshold = 10

    # Count white pixels
    white_pixels = np.sum(np.all(pixels >= white_threshold, axis=1))
    
    # Count black pixels
    black_pixels = np.sum(np.all(pixels <= black_threshold, axis=1))
    
    # Count color pixels (non-black and non-white)
    color_pixels = len(pixels) - white_pixels - black_pixels

    # Calculate total pixels
    total_pixels = len(pixels)

    # Return the distribution
    return {
        "color": color_pixels / total_pixels * 100,
        "black": black_pixels / total_pixels * 100,
        "white": white_pixels / total_pixels * 100,
    }

def process_pdf(file_path):
    """Process a PDF and calculate pixel distribution."""
    images = extract_images_from_pdf(file_path)
    
    # Aggregate distributions for all pages
    total_distribution = {"color": 0, "black": 0, "white": 0}
    page_count = 0

    for image in images:
        page_count += 1
        distribution = calculate_pixel_distribution(image)
        for key in total_distribution:
            total_distribution[key] += distribution[key]

    # Average the distribution across all pages
    for key in total_distribution:
        total_distribution[key] /= page_count

    return total_distribution
