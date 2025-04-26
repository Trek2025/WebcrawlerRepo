import subprocess
import os

def crawl_website(url, output_folder):
    if os.path.exists(output_folder):
        subprocess.run(['rm', '-rf', output_folder])
    os.makedirs(output_folder, exist_ok=True)

    subprocess.run([
        'wget',
        '--recursive',
        '--no-clobber',
        '--page-requisites',
        '--html-extension',
        '--convert-links',
        '--no-parent',
        url,
        '-P', output_folder
    ], check=True)
