import argparse
import base64
import os
import subprocess
import sys
from io import BytesIO
from PIL import Image as PILImage

OUTPUT_FILE = 'output_simple.html'
THUMBNAIL_WIDTH = 200

def get_metadata(file_path):
    cmd = ["identify", "-format", "'%[parameters]'", file_path]
    result = subprocess.check_output(cmd).decode('utf-8')

    try:
        artist = result.split(":")[0].split("(")[1].strip()
    except IndexError:
        print(f"Error processing artist metadata for file '{file_path}'.")
        print(f"Offending output: '{result}'")
        artist = 'ERROR'

    try:
        prompt = result.split(")")[1].split("Negative")[0].strip()
    except IndexError:
        print(f"Error processing prompt metadata for file '{file_path}'.")
        print(f"Offending output: '{result}'")
        prompt = 'ERROR'

    try:
        negative_prompt = result.split("Negative prompt:")[1].split("Steps:")[0].strip()
        model = result.split("Model:")[1].split(",")[0].strip()
    except IndexError:
        print(f"Error processing metadata for file '{file_path}'.")
        print(f"Offending output: '{result}'")
        sys.exit(1)

    return artist, prompt, negative_prompt, model, result

def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

def create_html(data, folder_path):
    with open(os.path.join(folder_path, OUTPUT_FILE), "w") as f:
        f.write("<html><head><title>Stable Diffusion Benchmark</title></head><body>")
        f.write(f"<h1>Stable Diffusion Benchmark {data['date']}</h1>")
        f.write(f"<h2>Model: {data['model']}</h2>")
        
        # CSS for the modal
        f.write("""
        <style>
            .modal {
                display: none;
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0,0,0,0.4);
            }
            .modal-content {
                background-color: #fefefe;
                margin: 15% auto;
                padding: 20px;
                border: 1px solid #888;
                width: 80%;
            }
            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }
            .close:hover, .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
        """)
        
        f.write("<table border='1'>")
        f.write("<tr><th>Artist</th></tr>")
        
        for artist in sorted(data['artists'].keys()):
            prompts = data['artists'][artist]
            f.write("<tr>")
            f.write(f"<td>{artist}</td>")
            for prompt, png_file in prompts.items():
                img_path = os.path.join(folder_path, png_file)
                with PILImage.open(img_path) as img:
                    aspect_ratio = img.height / img.width
                    new_height = int(THUMBNAIL_WIDTH * aspect_ratio)
                    img.thumbnail((THUMBNAIL_WIDTH, new_height))
                    img_base64 = image_to_base64(img)
               

                # Retrieve the complete metadata for this file
                _, _, _, _, complete_metadata = get_metadata(img_path)

                modal_id = f"modal-{artist}-{png_file}"
                alert_message = f"File Name: {png_file}<br><br>Metadata:<br>{complete_metadata}"
                f.write(f"<td><img src='data:image/png;base64,{img_base64}' width='{THUMBNAIL_WIDTH}' onclick=\"document.getElementById('{modal_id}').style.display='block'\"></td>")

                # Modal HTML
                f.write(f"""
                <div id="{modal_id}" class="modal">
                    <div class="modal-content">
                        <span class="close" onclick="document.getElementById('{modal_id}').style.display='none'">&times;</span>
                        <p>{alert_message}</p>
                    </div>
                </div>
                """)

            f.write("</tr>")
        
        f.write("</table>")
        
        # JavaScript to close the modal when clicked outside
        f.write("""
        <script>
            window.onclick = function(event) {
                if (event.target.className === 'modal') {
                    event.target.style.display = 'none';
                }
            }
        </script>
        """)
        
        f.write("</body></html>")

def main():
    parser = argparse.ArgumentParser(description="Generate HTML page from PNG metadata.")
    parser.add_argument('-o', '--output', default=OUTPUT_FILE, help="Specify the name of the output file.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output.")
    args = parser.parse_args()

    folder_path = input("Enter the folder location (or press Enter for current directory): ")
    if not folder_path:
        folder_path = os.getcwd()

    if args.verbose:
        print(f"Using folder path: {folder_path}")

    if not os.access(folder_path, os.R_OK | os.W_OK):
        print("Error: No read/write permissions for the folder.")
        return

    if not os.path.isfile("/opt/homebrew/bin/identify"):
        print("Error: 'identify' program is not installed or not executable.")
        return

    png_files = [f for f in os.listdir(folder_path)\
            if f.endswith('.png')\
            and not f.startswith('.')]

    if not png_files:
        print("Error: No PNG files found in the folder.")
        return

    if args.verbose:
        print(f'Found {len(png_files)} PNG files in the folder.')

    data = {
        "date": os.path.basename(folder_path),
        "model": "",
        "negative_prompt": "",
        "prompts": [],
        "artists": {}
    }

    for png_file in png_files:
        artist, prompt, negative_prompt, model, _ = get_metadata(os.path.join(folder_path, png_file))

        if args.verbose:
            print(f"Found image {png_file} with artist {artist} ...")

        if not data["model"]:
            data["model"] = model

        if not data["negative_prompt"]:
            data["negative_prompt"] = negative_prompt

        if prompt not in data["prompts"]:
            data["prompts"].append(prompt)

        if artist not in data["artists"]:
            data["artists"][artist] = {}

        data["artists"][artist][prompt] = png_file

    create_html(data, folder_path)

if __name__ == "__main__":
    main()

 
