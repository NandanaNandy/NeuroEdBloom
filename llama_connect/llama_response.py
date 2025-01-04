import ollama

# Define the model and prompt
model_name = "llama3.2"

# Example OCR text (replace this with your actual OCR text)
ocr_text = """
Course Outcomes:
1. Understand the principles of programming.
2. Develop problem-solving skills.
3. Apply algorithms to solve real-world problems.

Questions:
Part A:
1. What is a variable? (Knowledge)
2. Explain the concept of loops. (Comprehension)

Part B:
1. How do you implement a sorting algorithm? (Application)
2. Discuss the importance of data structures. (Analysis)
"""

# Combine the OCR text with the prompt
prompt = (
    "I will give you an OCR text and you have to extract the following details from the given unstructured text:\n"
    "1. List of course outcomes with their descriptions.\n"
    "2. Questions along with their corresponding Bloom's Taxonomy knowledge levels, categorized by parts (e.g., Part A, Part B).\n"
    "Present the extracted details in JSON format.\n\n"
    f"OCR Text:\n{ocr_text}"
)

# Generate a response
response = ollama.generate(model=model_name, prompt=prompt, stream=False)

# Print the response
print(response['response'])