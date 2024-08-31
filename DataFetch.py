import os
import json
from PyPDF2 import PdfReader
import re

def loop_through_pdfs(directory):
    pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]
    return pdf_files

def get_pdf_content(pdf_path):
    reader = PdfReader(pdf_path)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

def divide_pdf_content(content):
    
    # Regex pattern to detect the start of part 2
    part2_pattern = r"HIGH COURT OF"
    match = re.search(part2_pattern, content)
    
    if match is None:
        raise ValueError("Couldn't find the start of part 2 using the provided pattern")

    part2_start = match.start()

    part1 = content[:part2_start].strip()
    part2 = content[part2_start:].strip()
    
    return part1, part2

def create_json(prompt, completion):
    return {
        "prompt": prompt,
        "completion": completion
    }

def main(directory, output_file):
    pdf_files = loop_through_pdfs(directory)
    json_data = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory, pdf_file)
        print(f"Processing file: {pdf_file}")
        
        try:
            content = get_pdf_content(pdf_path)
            part1, part2 = divide_pdf_content(content)
            json_entry = create_json(part1, part2)
            json_data.append(json_entry)
        
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
    
    with open(output_file, 'w') as f:
        for entry in json_data:
            f.write(json.dumps(entry) + "\n")
    
    print(f"Processed {len(json_data)} PDFs. Output written to {output_file}")

# Run the main function with the directory containing PDFs and the output file
if __name__ == "__main__":
    directory = "/Users/namankhurpia/Desktop/Taxmann/data"  # Update this path to your PDFs directory
    output_file = "output.jsonl"
    main(directory, output_file)
