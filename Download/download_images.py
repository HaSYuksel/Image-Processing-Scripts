import pandas as pd
import requests
import os

def download_image(url, directory):
    """Download an image and save it to the specified directory."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_name = url.split("/")[-1]
            file_path = os.path.join(directory, image_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return False

def download_images_from_excel(excel_path, output_dir):
    """Read image URLs from an Excel file and download them if they are unique."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read Excel file without headers
    df = pd.read_excel(excel_path, header=None)
    urls = df.iloc[:, 0].drop_duplicates().tolist()  # Assumes URLs are in the first column

    for url in urls:
        if download_image(url, output_dir):
            print(f"Downloaded {url}")
        else:
            print(f"Failed to download {url}")

# Path to the Excel file and the directory to save images
excel_file_path = 'D:\\UhCLASSWebDev\\download_image.xlsx'
save_directory = 'D:\\UhCLASSWebDev\\compression test'

# Call the function
download_images_from_excel(excel_file_path, save_directory)
