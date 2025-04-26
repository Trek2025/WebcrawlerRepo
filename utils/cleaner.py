from bs4 import BeautifulSoup
import os

def extract_texts_from_html(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".html") or file.endswith(".htm"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, 'html.parser')

                for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                    tag.decompose()

                text = soup.get_text(separator=' ', strip=True)

                relative_path = os.path.relpath(path, input_folder)
                output_path = os.path.join(output_folder, relative_path.replace('.html', '.txt').replace('.htm', '.txt'))
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
