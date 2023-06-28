import requests
from bs4 import BeautifulSoup

def get_google_images(query):
    # Define the URL to search
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    
    # Make the request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to fetch the URL")
        return []
    
    # Parse the HTML content of the response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all of the image tags in the HTML
    images = soup.find_all("img")
    
    # Extract the source URL for each image
    image_urls = [image["src"] for image in images if image["src"].startswith("https")]
    
    return image_urls


# Search for Minecraft images
#image_urls = get_google_images("minecraft")

# Print the list of image URLs
# print("Image URLs:")
# print(image_urls)