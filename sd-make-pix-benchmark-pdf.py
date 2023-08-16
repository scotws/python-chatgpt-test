# Create Stable Diffusion Benchmark Pictures as PDF
# Scot W. Stevenson <scot.stevenson@gmail.com>
# First version: 2023-08-13
# This version: 2023-08-13

import os
import subprocess
from fpdf import FPDF
from PIL import Image

FONT_SIZE = 10
THUMB_SIZE = 40

def get_metadata(file_path):
    cmd = ["identify", "-format", "'%[parameters]'", file_path]
    result = subprocess.check_output(cmd).decode('utf-8')
    artist = result.split(":")[0].split("(")[1].strip()
    prompt = result.split(")")[1].split("Negative")[0].strip()
    negative_prompt = result.split("Negative prompt:")[1].split("Steps:")[0].strip()
    model = result.split("Model:")[1].split(",")[0].strip()

    return artist, prompt, negative_prompt, model

def create_pdf(data, folder_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=FONT_SIZE)

    # Title
    pdf.cell(200, 10, txt=f"Stable Diffusion Benchmark {data['date']}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Model: {data['model']}", ln=True, align='L')

    # Table header
    pdf.cell(THUMB_SIZE, 10, "Artist", 1)
    for prompt in data['prompts']:
        pdf.cell(THUMB_SIZE, 10, prompt, 1)
    pdf.ln()

    # Table content
    for artist, prompts in data['artists'].items():
        pdf.cell(THUMB_SIZE, THUMB_SIZE, artist, 1)
        for prompt in data['prompts']:
            if prompt in prompts:
                thumbnail_path = os.path.join(folder_path, prompts[prompt])
                pdf.image(thumbnail_path, x=pdf.get_x(), y=pdf.get_y(), w=THUMB_SIZE)
            pdf.cell(THUMB_SIZE, THUMB_SIZE, "", 1)
        pdf.ln()

    pdf.cell(200, 10, txt=f"Negative prompt: {data['negative_prompt']}", ln=True, align='L')

    pdf.output(os.path.join(folder_path, "output.pdf"))

def main():
    folder_path = input("Enter the folder location (or press Enter for current directory): ")
    if not folder_path:
        folder_path = os.getcwd()

    if not os.access(folder_path, os.R_OK | os.W_OK):
        print("Error: No read/write permissions for the folder.")
        return

    if not os.path.isfile("/opt/homebrew/bin/identify"):
        print("Error: 'identify' program is not installed or not executable.")
        return

    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    if not png_files:
        print("Error: No PNG files found in the folder.")
        return

    data = {
        "date": os.path.basename(folder_path),
        "model": "",
        "negative_prompt": "",
        "prompts": [],
        "artists": {}
    }

    for png_file in png_files:
        artist, prompt, negative_prompt, model = get_metadata(os.path.join(folder_path, png_file))

        if not data["model"]:
            data["model"] = model
        if not data["negative_prompt"]:
            data["negative_prompt"] = negative_prompt

        if prompt not in data["prompts"]:
            data["prompts"].append(prompt)

        if artist not in data["artists"]:
            data["artists"][artist] = {}

        data["artists"][artist][prompt] = png_file

    create_pdf(data, folder_path)

if __name__ == "__main__":
    main()


 
