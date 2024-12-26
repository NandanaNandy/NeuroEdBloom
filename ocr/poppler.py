import os
import time
import sys
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
import torch
from torchvision import transforms
import concurrent.futures

def main(pdf_path, output_dir="output_images", dpi=200, poppler_path=r"D:\Program Files\poppler-24.08.0\Library\bin"):
    # Validate the PDF path
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return
    
    # Get the number of pages in the PDF
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        last_page = len(reader.pages)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("Using CUDA" if torch.cuda.is_available() else "CUDA not available")

    start_time = time.time()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert PDF to images
    images = convert_from_path(pdf_path, dpi=dpi, first_page=1, last_page=last_page, poppler_path=poppler_path)

    # Define a transform to convert images to tensors
    transform = transforms.ToTensor()

    def process_image(i, image):
        image_start_time = time.time()
        image_tensor = transform(image)
        output_image = transforms.ToPILImage()(image_tensor.cpu())
        output_image.save(os.path.join(output_dir, f'page_{i + 1}.png'), quality=95)
        return time.time() - image_start_time

    # Process images in parallel using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_image, i, image) for i, image in enumerate(images)]
        [future.result() for future in concurrent.futures.as_completed(futures)]

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
    print(f"Images saved in: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python poppler.py <pdf_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    main(pdf_path)
