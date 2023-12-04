import json
import shutil
import requests
import threading
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode

# Finding chromedriver path automatically
def find_chromedriver():
    chromedriver_path = shutil.which('chromedriver')
    if chromedriver_path:
        return chromedriver_path
    else:
        print("Chromedriver not found. Please make sure it's installed or provide the path manually.")
        return None

# Path to chromedriver
chromedriver_path = find_chromedriver()

# Read URLs from file
with open('scrape.txt', 'r') as file:
    urls_to_check = [line.strip() for line in file.readlines()]

# Function to get Swagger UI version
def get_swagger_version(swagger_url):
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(swagger_url)
        print(f"Accessing {swagger_url}")
        time.sleep(15)  # Wait for a longer period (adjust as needed) for the page to load

        version_script = """
            if (typeof versions !== 'undefined') {
                return JSON.stringify(versions);
            } else {
                return 'Version information not found';
            }
        """

        swagger_version = driver.execute_script(version_script)
        print(f"Swagger UI version for {swagger_url}: {swagger_version}")

        try:
            version_data = json.loads(swagger_version)
            if 'swaggerUi' in version_data and 'version' in version_data['swaggerUi']:
                swagger_version = version_data['swaggerUi']['version']
                if isinstance(swagger_version, str):  # Check if version is a string
                    version_parts = swagger_version.split('.')
                    major_version = int(version_parts[0]) if version_parts else 0
                    minor_version = int(version_parts[1]) if len(version_parts) > 1 else 0
                    if major_version < 3 or (major_version == 3 and minor_version < 60):
                        print(f"Version below 3.60.0 found for {swagger_url}: {swagger_version}")
                        with open('hits.txt', 'a') as hits_file:
                            hits_file.write(f"Version below 3.60.0 - {swagger_url}: {swagger_version}\n")
                        print(f"Logged URL to hits.txt: {swagger_url}")

        except json.JSONDecodeError:
            print(f"Error decoding JSON for {swagger_url}: {swagger_version}")

    except Exception as e:
        print(f"Error accessing {swagger_url}: {e}")

    finally:
        if driver:
            driver.quit()

# Function to check Swagger UI version for URLs
def check_swagger_versions():
    for url in urls_to_check:
        thread = threading.Thread(target=get_swagger_version, args=(url,))
        thread.start()
        time.sleep(random.uniform(3, 6))  # Random delay between 3 to 6 seconds

# Start checking Swagger UI versions for the URLs
threading.Thread(target=check_swagger_versions).start()
