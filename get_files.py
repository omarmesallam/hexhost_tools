import requests
from PIL import Image
from io import BytesIO

def download_and_view(url):
    """
    Downloads an image from a URL and displays it using Pillow.
    
    Args:
        url (str): The URL of the image to download.
    """
    response = None
    try:
        print(f"Downloading image from: {url}")
        
        # Adding a User-Agent header can sometimes bypass basic bot protection
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        # Log status and content type to help debugging
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('Content-Type')}")

        # Raise an exception for 4xx or 5xx errors
        response.raise_for_status()

        # If the server returned HTML, it's likely a login page, not the image
        if "text/html" in response.headers.get("Content-Type", ""):
            print("\nWARNING: The URL returned an HTML page instead of an image.")
            print("This usually happens with cPanel URLs because they require a login session.")
            print("Try using the public website URL instead of the cPanel viewer link.")
            return

        # Open the image using Pillow from the byte stream
        img = Image.open(BytesIO(response.content))
        
        # Display the image
        img.show()
        print("Image displayed successfully.")
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        if response.status_code == 401 or response.status_code == 403:
            print("Access Denied: This URL requires authentication (login).")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # The URL below is for the cPanel File Manager, which is private.
    # To view this image in a script, you should use the public URL.
    # If your site is 'mohamed.hexhost.online', the public URL would be:
    # http://www.mohamed.hexhost.online/assets/assets/book/part1/K1-004.jpg
    
    cpanel_url = "http://www.mohamed.hexhost.online:2082/cpsess9872382387/viewer/home%2fmohamedm%2fpublic_html%2fassets%2fassets%2fbook%2fpart2/K2-014.jpg"
    
    # Try the public URL instead:
    public_url = "http://www.mohamed.hexhost.online/assets/assets/book/part2/K2-014.jpg"
    
    download_and_view(public_url)
