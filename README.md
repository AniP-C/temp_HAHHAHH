# temp_HAHHAHH

import requests
from bs4 import BeautifulSoup
import time
import webbrowser

def check_url_presence(dictionary):
    # Headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Iterate through each key and its values in the dictionary
    for key, values in dictionary.items():
        if not isinstance(values, list):
            values = [values]  # Convert single value to list
            
        for value in values:
            # Construct the URL (replace this with your URL pattern)
            url = f"https://direct.asda.com/george/clothing/10,default,sc.html?q={value}"  # Modify this according to your needs
            
            try:
                # Open URL in browser
                webbrowser.open(url)
                
                # Wait for a few seconds to let the page load (adjust as needed)
                time.sleep(3)
                
                # Make the request
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception for bad status codes
                
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for searchfail_text class
                search_fail = soup.find(class_='searchfail_text')
                
                if search_fail:
                    print(f"Key: {key}, Value: {value} - Not present in website")
                else:
                    # Check for mini-container class
                    mini_container = soup.find(class_='mini-container')
                    if mini_container:
                        print(f"Key: {key}, Value: {value} - Present in website")
                    else:
                        print(f"Key: {key}, Value: {value} - Unable to determine presence (neither class found)")
                
            except requests.RequestException as e:
                print(f"Error processing {value}: {str(e)}")
            
            # Add a small delay between requests to be polite to the server
            time.sleep(1)

# Example usage
sample_dict = {
    "category1": ["G008020919"],
    # "category2": ["value4", "value5"],
    # "category3": "value6"
}

# Run the script
check_url_presence(sample_dict)
