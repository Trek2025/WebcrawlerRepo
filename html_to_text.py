import os
from bs4 import BeautifulSoup

def extract_texts_from_html_folder(source_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith(".html"):
            filepath = os.path.join(source_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)

            output_filename = filename.replace('.html', '.txt')
            output_path = os.path.join(output_folder, output_filename)
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(text)

    print(f"Extraction completed! Text files saved to {output_folder}")
