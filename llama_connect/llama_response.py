import ollama

# Define the model and prompt
model_name = "llama3.2"

# Example OCR text (replace this with your actual OCR text)
ocr_text ="""
KIT/IQAC/AC1 1d/Rev.No.0 1/12.08. 24 
 
 
DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE                     
ACADEMIC YEAR: 2024-2025 (ODD SEMESTER ) 
 
CONTINUOUS INTERNAL ASSESSMENT I I (SET I I) 
 
 
COs  Course Outcome  Knowledge 
Level  
CO3  Understand the various authentication schemes to simulate different 
applications.  K2 
CO4  Understand various security practices  and system security standards . K2 
CO5  Make use of  the Web security protocols for E -Commerce applications . K3 
 
S.No.  Knowledge  
Level  PART  A  
Answer all the Questions  (10 × 2 = 20  Marks )  COs  Marks  
1 K1 Define  Key distribution center.  CO3  2 
2 K1 Label  the requirements for Kerberos.  CO3  2 
3 K1 What is PGP?  CO4  2 
4 K1 Recall replay attack.  CO4  2 
5 K2 List the steps for preparing signed  data. CO4  2 
6 K2 Compare  transport mode and tunnel mode.  CO4  2 
7 K1 Define web security.  CO5  2 
8 K1 List out the w ays of classifying web security threats . CO5  2 
9 K2 Outline  the role of security standards.  CO5  2 
10 K2 Infer  the use of Heartbeat protocol.  CO5  2 
 
S.No.  Knowledge  
Level  PART  B  
Answer all the Questions (5 × 13 = 65  Marks )  COs  Marks  
11a K2 Explain the Kerberos authentication protocol in detail  with an 
example.  CO3  13 
(OR)  
 
11b 
   K2 Illustrate the format of the X.509 certificate provide any real time 
case study for the use of  X.509 certificate.   
 CO3  
   13 
12a   K2 Demonstrate  about the Operati onal descriptions key  management in 
PGP operation with  neat diagram.  CO4  13 
(OR)  
12b   K2 Explain  the concept of tr ust models in network security in detail.  CO4  13 
13a   K2 Demonstrate  the AH   protocols  and mode with a neat diagram.       CO4  13 
(OR)  
13b  (i)   K2 Compare between AH and ESP.  CO4  7 Branch / Year / Semester        :  AI & DS /III/V                                         Max. Mark      : 100 Marks  
Course Code & Name             : CW3551&Data and Information Security Duration          : 3 hours  
Faculty Name & Designation :  Dr.R.Nallakumar  ASP /AI & DS             Date of Exam   : 19.11.2024 FN                                                                                                                         
 KIT/IQAC/AC1 1d/Rev.No.0 1/12.08. 24 
 13b  
  (ii)    K2 Summarize  the concept of ESP packet format.  CO4  6 
14a 
 
 K2 
 Explain the working of secure socket la yer in detail  with an example.  CO5  
 13 
 
(OR)  
14b K2 Illustrate  the SSL architecture in detail and explain how it helps in 
maintaining secure end -end communications.  CO5  13 
15a K2 Outline the working of SET with neat diagram and elaborate its  role 
in transaction processing.  CO5  13 
(OR)  
15b i) K2 Summarize  the concept of  Heartbeat protocol  CO5  7 
ii) K2 Explain th e working of Handshake protocol with the neat sketch.  CO5  6 
 
S.No.  Knowledge  
Level  PART  C 
Answer all the Questions  (1 × 15= 15 Marks )  COs  Marks  
16a K3 Build the process of the Transport Layer Protocol and discuss its key 
conc epts, functionalities,  protocols, and role in the OSI  model . CO5  15 
(OR)  
16b      K3 Make use of  web security protocols used in any real time e-commerce 
applications.  CO5  15 
 
Knowledge Level ( Blooms Taxonomy)  
K1 Remember  K2 Understand  K3 Apply  
K4 Analyze  K5 Evaluate  K6 Create  
 
Signature of Faculty Member                   Signature of Scrutiny  Member     HoD  
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
    "include the question numbers also"
    "include the co 's also"
    f"OCR Text:\n{ocr_text}"
)

# Generate a response
response = ollama.generate(model=model_name, prompt=prompt, stream=False)

# Print the response
print(response['response'])