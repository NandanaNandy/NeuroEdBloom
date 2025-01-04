# Import necessary libraries
from typing import Dict, Any, List, Tuple
import json
import re
from llama_cpp import Llama

def preprocess_ocr_text(text: str) -> str:
    """
    Clean and preprocess noisy OCR text.
    """
    # Remove special characters and unwanted symbols
    text = re.sub(r'[^\w\s\.\,\:\(\)\-\/%]', ' ', text)
    
    # Fix common OCR errors
    replacements = {
        'O0': '0',  # Replace letter O with number 0
        'I1': '1',  # Replace letter I with number 1
        'l1': '1',  # Replace lowercase l with number 1
        'S5': '5',  # Replace letter S with number 5
    }
    for error, correction in replacements.items():
        text = re.sub(f'[{error}]', correction, text)
    
    # Fix common spacing issues
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'\s*\.\s*', '. ', text)  # Fix period spacing
    text = re.sub(r'\s*\:\s*', ': ', text)  # Fix colon spacing
    
    return text.strip()

def extract_metadata(text: str) -> Dict[str, str]:
    """
    Extract metadata using pattern matching for noisy text.
    """
    metadata = {
        "course_code": "",
        "course_name": "",
        "professor": "",
        "date": "",
        "duration": "",
        "total_marks": "",
        "semester": ""
    }
    
    patterns = {
        "course_code": r"(?i)(?:course|code)[\s:]*([A-Z0-9]{6,8})",
        "professor": r"(?i)(?:prof|professor|instructor)[\s:]*([A-Za-z\s\.]+)",
        "date": r"(?i)(?:date|dated)[\s:]*(\d{1,2}[\s/\-\.]+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s/\-\.]+\d{2,4})",
        "duration": r"(?i)(?:duration|time)[\s:]*(\d+[\s]*(?:hours|hrs|hr|hour))",
        "total_marks": r"(?i)(?:total marks|marks|maximum marks)[\s:]*(\d+)",
        "semester": r"(?i)(?:semester|sem)[\s:]*([a-zA-Z0-9\s\-]+)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metadata[key] = match.group(1).strip()
    
    # Extract course name (usually follows course code)
    course_code_match = re.search(patterns["course_code"], text)
    if course_code_match:
        course_name_pattern = f"{course_code_match.group(0)}(.*?)(?:professor|date|duration|marks|semester|$)"
        course_name_match = re.search(course_name_pattern, text, re.IGNORECASE | re.DOTALL)
        if course_name_match:
            metadata["course_name"] = course_name_match.group(1).strip()
    
    return metadata

def identify_questions(text: str) -> List[Dict[str, Any]]:
    """
    Identify questions and their components from noisy text.
    """
    question_patterns = [
        r'\d+\s*[\.\)]\s*[A-Za-z]',  # Matches "1. " or "1) "
        r'Q\s*\d+\s*[\.\:]',         # Matches "Q1." or "Q1:"
        r'Question\s*\d+\s*[\.\:]'    # Matches "Question 1." or "Question 1:"
    ]
    
    combined_pattern = '|'.join(f'({p})' for p in question_patterns)
    question_blocks = re.split(combined_pattern, text)
    question_blocks = [q.strip() for q in question_blocks if q and len(q.strip()) > 10]
    
    questions = []
    for block in question_blocks:
        question = {
            "question_number": "",
            "question_text": block,
            "marks_allocated": "",
            "knowledge_level": "",
            "course_outcome": "",
            "difficulty_level": "",
            "sub_questions": []
        }
        
        marks_match = re.search(r'[\(\[]?\s*(\d+)\s*marks?\s*[\)\]]?', block, re.IGNORECASE)
        if marks_match:
            question["marks_allocated"] = marks_match.group(1)
        
        co_match = re.search(r'(?i)(?:CO|Course Outcome)\s*[:\-]?\s*(\d+)', block)
        if co_match:
            question["course_outcome"] = f"CO{co_match.group(1)}"
        
        questions.append(question)
    
    return questions

def construct_prompt(question_text: str) -> str:
    """
    Construct analysis prompt for the Llama model.
    """
    return f"""
    Analyze this exam question and provide educational assessment details.
    The text may contain OCR errors.

    Question: {question_text}

    Provide JSON output only with this structure:
    {{
        "knowledge_level": "Remember/Understand/Apply/Analyze/Evaluate/Create",
        "difficulty_level": "Easy/Medium/Hard",
        "key_concepts": ["concept1", "concept2"],
        "bloom_category": "cognitive/affective/psychomotor",
        "question_type": "theoretical/numerical/programming/design",
        "expected_time": "time in minutes"
    }}
    """

def analyze_question_paper(ocr_text: str, model_path: str) -> Dict[str, Any]:
    """
    Main function to analyze question paper with OCR text.
    Args:
        ocr_text: The OCR extracted text
        model_path: Path to the Llama model file
    """
    # Clean the text
    cleaned_text = preprocess_ocr_text(ocr_text)
    
    # Extract basic metadata
    metadata = extract_metadata(cleaned_text)
    
    # Extract questions
    questions = identify_questions(cleaned_text)
    
    try:
        # Initialize Llama model
        llm = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=4
        )
        
        # Analyze each question
        for question in questions:
            prompt = construct_prompt(question["question_text"])
            
            response = llm(
                prompt,
                max_tokens=512,
                temperature=0.1,
                stop=["```"],
                echo=False
            )
            
            try:
                analysis = json.loads(response['choices'][0]['text'].strip())
                question.update(analysis)
            except json.JSONDecodeError:
                print(f"Failed to parse Llama response for question")
                
    except Exception as e:
        print(f"Error during Llama analysis: {str(e)}")
    
    # Calculate distributions
    total_marks = sum(int(q["marks_allocated"]) for q in questions if q["marks_allocated"].isdigit())
    
    co_coverage = {"CO1": 0, "CO2": 0, "CO3": 0, "CO4": 0, "CO5": 0}
    knowledge_distribution = {
        "Remember": 0, "Understand": 0, "Apply": 0,
        "Analyze": 0, "Evaluate": 0, "Create": 0
    }
    
    # Update distributions
    if total_marks > 0:
        for question in questions:
            if question["marks_allocated"].isdigit():
                marks = int(question["marks_allocated"])
                if question["course_outcome"]:
                    co_coverage[question["course_outcome"]] += (marks / total_marks * 100)
                if question["knowledge_level"]:
                    knowledge_distribution[question["knowledge_level"]] += (marks / total_marks * 100)
    
    return {
        "metadata": metadata,
        "questions": questions,
        "course_outcomes_coverage": co_coverage,
        "knowledge_level_distribution": knowledge_distribution
    }

# Example usage
if __name__ == "__main__":
    # Example OCR text
    sample_text = """
    VlT Unlverslty
    End Semester Examinatian - 2O24
    
    Course: CSElOO2 Pr0blem S0lving and Programming
    Prof: Dr, Sarah J0hnson
    Date: Aprll l5, 2O24
    Duratian: 3 hours
    T0tal Marks: l00
    Sem: Winter 2024
    
    l. Exp1ain the concept 0f recursion with an examp1e. (l0 marks)
       CO1 - Understanding recursive prob1em-solving
    
    2. Write a program t0 implement bubb1e s0rt a1gorithm. (l5 marks)
       CO2 - Implementation 0f s0rting alg0rithms
       
    3. Analyze the time complexity of quicksort algorithm. (20 marks)
       CO3 - Algorithm analysis
    """
    
    # Specify your model path here
    MODEL_PATH = "path/to/your/llama-model.bin"
    
    try:
        # Analyze the paper
        result = analyze_question_paper(sample_text, MODEL_PATH)
        
        # Print formatted output
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")