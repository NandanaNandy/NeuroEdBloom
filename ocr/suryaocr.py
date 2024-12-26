import os
import logging
from PIL import Image
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
detection_batch_size = 25
recognition_batch_size = 25
langs = ["en"]  # Supported languages
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Lazy-loaded model variables
det_processor, det_model, rec_model, rec_processor = None, None, None, None

def load_models_once():
    global det_processor, det_model, rec_model, rec_processor
    if not all([det_processor, det_model, rec_model, rec_processor]):
        logger.info("Loading models...")
        det_processor, det_model = load_det_processor(), load_det_model()
        rec_model, rec_processor = load_rec_model(), load_rec_processor()
        det_model.to(device)
        rec_model.to(device)
        logger.info("Models loaded successfully.")

def process_images_in_folder(folder_path):
    if not os.path.exists(folder_path):
        logger.error(f"Directory {folder_path} does not exist.")
        return

    # Load models
    load_models_once()

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            file_path = os.path.join(folder_path, filename)
            logger.info(f"Processing: {file_path}")

            try:
                # Load image
                image = Image.open(file_path)
                image.thumbnail((1024, 1024), Image.LANCZOS)

                # Run OCR
                predictions = run_ocr(
                    [image],
                    [langs],
                    det_model,
                    det_processor,
                    rec_model,
                    rec_processor,
                    detection_batch_size=detection_batch_size,
                    recognition_batch_size=recognition_batch_size,
                )

                # Extract and log text
                extracted_text = "\n".join([each.text for each in predictions[0].text_lines])
                logger.info(f"Extracted Text from {filename}:\n**Page {filename}**:\n{extracted_text}")
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    folder_path = "output_images"
    process_images_in_folder(folder_path)
