import requests
import os
import re
from urllib.parse import urlparse

def sanitize_filename(filename):
    """Remove invalid characters from filename and strip square brackets."""
    # Remove square brackets explicitly
    filename = filename.replace('[', '').replace(']', '')
    # Remove other invalid characters
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download_emotes(package_id):
    # API URL
    api_url = f"https://api.bilibili.com/x/emote/package?business=watch_full&ids={package_id}"
    
    # Create base directory
    base_dir = "bili_emote"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Define headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Referer": "https://www.bilibili.com/",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        # Fetch package info
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data["code"] != 0:
            print(f"Error: API returned code {data['code']} with message {data['message']}")
            return
        
        # Get package details
        package = data["data"]["packages"][0]
        package_name = sanitize_filename(package["text"])
        package_dir = os.path.join(base_dir, package_name)
        
        # Create package directory
        if not os.path.exists(package_dir):
            os.makedirs(package_dir)
        
        # Download each emote
        for emote in package["emote"]:
            # Use the full 'text' field for the filename, with brackets removed
            emote_name = sanitize_filename(emote["text"])
            emote_url = emote["url"]
            
            # Get file extension from URL
            parsed_url = urlparse(emote_url)
            file_ext = os.path.splitext(parsed_url.path)[1] or ".png"
            
            # Construct output path
            output_path = os.path.join(package_dir, f"{emote_name}{file_ext}")
            
            # Download and save emote
            print(f"Downloading {emote_name}...")
            try:
                emote_response = requests.get(emote_url, headers=headers)
                emote_response.raise_for_status()
                
                with open(output_path, "wb") as f:
                    f.write(emote_response.content)
                print(f"Saved {emote_name} to {output_path}")
            except requests.RequestException as e:
                print(f"Failed to download {emote_name}: {e}")
                
    except requests.RequestException as e:
        print(f"Failed to fetch package info: {e}")
    except KeyError as e:
        print(f"Unexpected API response structure: {e}")

def main():
    while True:
        package_id = input("Enter the emote package ID (or 'q' to quit): ").strip()
        if package_id.lower() == 'q':
            break
        if not package_id.isdigit():
            print("Please enter a valid numeric ID")
            continue
        download_emotes(package_id)

if __name__ == "__main__":
    main()
