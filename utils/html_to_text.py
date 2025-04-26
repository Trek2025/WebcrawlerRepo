# File: html_to_text.py

import os
from bs4 import BeautifulSoup

def extract_texts_from_html_folder(folder_path, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, "html.parser")
                # Remove script and style elements
                for script_or_style in soup(["script", "style", "noscript"]):
                    script_or_style.extract()

                text = soup.get_text(separator='\n')
                text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])

            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_folder, output_filename)

            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(text)

if __name__ == "__main__":
    input_folder = "datacolada_com_crawl"  # your crawl folder
    output_folder = "datacolada_com_texts"  # where the clean text files will go
    extract_text_from_html_folder(input_folder, output_folder)
    print(f"Extraction completed! Text files saved to {output_folder}")
