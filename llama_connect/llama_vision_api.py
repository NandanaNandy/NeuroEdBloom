import requests
import base64
from PIL import Image, ImageEnhance, ImageFilter

# API configuration
API_KEY = "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"
INVOKE_URL = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions"
IMAGE_PATH = r"E:\Projects\Answersheet_image_1.jpg"
OUTPUT_FILE = "output.txt"
STREAM = False

# Preprocess the image to enhance readability
def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert("L")  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)  # Sharpen the image
    processed_image_path = "processed_image.png"
    image.save(processed_image_path)
    return processed_image_path

# Encode the preprocessed image as base64
processed_image_path = preprocess_image(IMAGE_PATH)
with open(processed_image_path, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

# Define headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "text/event-stream" if STREAM else "application/json",
    "Content-Type": "application/json"
}

# Define the payload with explicit instructions for question formatting
payload = {
    "model": "meta/llama-3.2-11b-vision-instruct",
    "messages": [
        {
            "role": "user",
            "content": f'''
                "Extract the following details from the given image of a student answer evaluation form:

                Register Number: Identify the number under 'REGISTER NUMBER'.
                Date and Session: Extract the 'Date & Session' field (e.g., '29-04-2024 F EN').
                Course Code and Name: Identify the course code and name under 'Course code/Title' (e.g., 'CCS342 - DEVOPS').
                Year/Department: Extract the 'Year/Dept/Section' field (e.g., 'III / AI & DS').
                Section: Extract the section explicitly if mentioned.
                Q.No, Relevant CO, and Marks: For each question (Q.No):
                Extract the question number.
                Extract the corresponding 'Relevant CO'.
                Extract the marks awarded (e.g., '11', '12', etc.).
                Ensure the data is structured clearly and aligns with the format in the image. Provide the results in a JSON format for easier processing."
                Here is the image content: <img src="data:image/png;base64,{image_b64}" />
            '''
        }
    ],
    "max_tokens": 1024,
    "temperature": 0.0,
    "top_p": 1.0,
    "stream": STREAM
}

# Make the API request
response = requests.post(INVOKE_URL, headers=headers, json=payload)

# Handle response
if STREAM:
    print("Streaming response:")
    for line in response.iter_lines():
        if line:
            print(line.decode("utf-8"))
else:
    if response.status_code == 200:
        print("Extraction successful. Raw response:")
        print(response.text)  # Debug the raw response

        # Parse and print structured data
        response_data = response.json()
        extracted_content = response_data.get("choices", [])[0].get("message", {}).get("content", "")
        print("\nExtracted Content in Structured Format:")
        print(extracted_content)

        # Save the output to a file
        with open(OUTPUT_FILE, "w") as file:
            file.write(extracted_content)
        print(f"\nOutput saved to {OUTPUT_FILE}")
    else:
        print(f"Error {response.status_code}: {response.text}")
        with open(OUTPUT_FILE, "w") as file:
            file.write(f"Error {response.status_code}: {response.text}")
