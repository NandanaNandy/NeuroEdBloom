import subprocess
import sys
import time

DEFAULT_PDF_PATH = r"C:\Users\MuraliDharan S\OneDrive\Desktop\desktop\project\documents\DIS -1.pdf"

def main():
    pdf_path = DEFAULT_PDF_PATH
    if len(sys.argv) == 2:
        pdf_path = sys.argv[1]
    elif len(sys.argv) > 2:
        print("Usage: python orchestrator.py [<pdf_path>]")
        sys.exit(1)

    # Step 1: Run poppler.py with the PDF path
    start_time = time.time()
    subprocess.run(["python", "poppler.py", pdf_path])
    poppler_time = time.time() - start_time
    print(f"poppler.py execution time: {poppler_time:.2f} seconds")

    # Step 2: Run suryaocr.py to process the generated images
    start_time = time.time()
    subprocess.run(["python", "suryaocr.py"])
    suryaocr_time = time.time() - start_time
    print(f"suryaocr.py execution time: {suryaocr_time:.2f} seconds")

    total_time = poppler_time + suryaocr_time
    print(f"Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
