import ollama

# Define the model and prompt
model_name = "llama3.2"

# Example OCR text (replace this with your actual OCR text)
ocr_text = """
page 1

Autonomous - Approved by UGC and Anna University, Chennai Approved by AICTE and Affiliated to Anna University, Chennai Accredited by NAAC with 'A++' Accredited by NBA - (CSE, IT and ECE) An ISO 9001:2015 and ISO 14001:2015 Certified Institution DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE ACADEMIC YEAR: 2024 - 2025 (ODD SEMESTER) CONTINUOUS INTERNAL ASSESSMENT I (SET II) Branch / Year / Semester : AI & DS /III/V Max. Marks : 100 Marks Course Code & Name  .. CW3551&Data and Information Security  Duration : 3 hours Faculty Name & Designation : Dr.R.Nallakumar, ASP /AI & DS Date of Exam : 01.10.2024 FN Knowledge COs Course Outcome Level CO1 Understand the basics of information security. K2 Make the use of legal, ethical and professional issues in information security. K3 CO2 the various authentication schemes to simulate Understand different CO3 K2 application. PART A Knowledge S. No. COs Marks Level Answer all the Questions(10× 2 = 20 Marks ) List out the characteristics of CIA triangle. l KI CO1 2 2 KI Define Data Security. CO1 2 3 K2 Compare vulnerability with exposure. CO1 2 4 KI What is balancing security and access? CO1 2 5 K1 Define software privacy. CO2 2 6 KI List out some of the issues in Information Security. 2 CO2 7 K1 Recall the kev components of Computer Security. CO2 2 Outline the characteristics that distinguish different security policies CO2 8 K2 2 from one another. 9 K1 What is digital signature? CO3 2 Provide an overview of how different authentication methods enhance Kl CO3 10 2 security. Knowled PART B S. No. COs Marks ge Answer all the Questions(5 × 13 = 65 Marks ) Level Outline the components of Information System. K2 CO1 7 (i) lla K2 Explain in detail about the concepts of threat and attacks. (ii) CO1 6 (OR) Analyze the critical characteristics of information and explain how K2 COI 11b 13 they are used in the study of computer security. Illustrate SDLC waterfall methodology and its relation in respect to 12a K2 COI 13 information security. (OR) KIT/IQAC/AC11d/Rev.No.01/12.08.24
page 2 


Discuss the steps common to both the systems development life cycle 12b K2 CO1 13 and the security systems life cycle. Illustrate the intellectual property owned by an organization usually K2 CO2 13 13a have value if so, how can attackers threaten that value. (OR) K2 Summarize the confidentiality policies. 7 (i) CO2 13b (ii) K2 Explain in detail about legal, Ethical and professional issues. 6 CO2 Identify the model used for confidentiality policy and explain. 14a K2 CO2 13 (OR) (i) K2 Explain in detail about integrity polices. CO2 6 14b Summarize the methods available for managing authorization. K2 7 (ii) CO2 15a K2 Outline the RSA-PSS digital signature algorithm with example. CO2 13 (OR) 15b K2 Summarize the NIST digital signature algorithm with neat diagram. CO2 13 PART C Knowledge COs S.No. Marks Level Answer all the Questions (1 × 15 = 15 Marks ) Experiment the transformation in how hackers are viewed and K3 16a CO2 I રે characterize the profile of a hacker today. (OR) Construct an access control matrix system as part of a security K3 CO2 16b I ર investigation. Knowledge Level (Blooms Taxonomy) K1 Remember Understand K2 K3 Apply K4 Analyze K2 Evaluate K6 Create Signature of Faculty Member Signature of Scrutiny Member HOD KIT/IQAC/AC11d/Rev.No.01/12.08.24
"""

# Combine the OCR text with the prompt
prompt = (
    "I will give you an OCR text and you have to extract the following details from the given unstructured text:\n"
    "1. List of course outcomes with their descriptions.\n"
    "2. Questions along with their corresponding Bloom's Taxonomy knowledge levels, categorized by parts (e.g., Part A, Part B).\n"
    "3. List the knowledge and courseoutcome as well where knowledge level is the k1,k2,k3 k4 examples.\n"
    "4. List the marks and level of the questions.\n"
    "Present the extracted details in JSON format.\n\n"
    "**be accurate**\n\n"
    "**dont generate the response if the question is not clear or not available in the text**\n\n"
    "5.Finally give me all the question available in the text.\n\n"
    "6.dont give the question numbers\n\n"
    "if the question is not clear or not available in the text please mention it as 'Question not clear or not available in the text'\n\n"
    "if the marks not clear or not available in the text please mention it as 'Marks not clear or not available in the text'\n\n"
    f"OCR Text:\n{ocr_text}"
)

# Generate a response
response = ollama.generate(model=model_name, prompt=prompt, stream=False)

# Print the response
print(response['response'])