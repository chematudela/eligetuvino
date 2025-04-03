from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Function to save URLs to a file
def save_urls_to_file(urls, batch_number):
    filename = f'Vino Blanco 10200 {batch_number}.txt'
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')
    print(f"Las nuevas URLs han sido guardadas en '{filename}'.")

# Set up Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Read URLs from a .txt file
with open('/Users/josetudela/Projects/vinos_grupo2/Proyecto_grupo2_vinos/vinoblanco10200.txt', 'r') as file:
    urls_list = [line.strip() for line in file.readlines()]

# List to store new URLs
new_urls = []
batch_size = 100
batch_number = 6

# Process each URL in the list
for original_url in urls_list[600:]:
    print(f"Procesando URL: {original_url}")  # Show progress

    try:
        # Open the URL
        driver.get(original_url)

        # Wait for the page to load completely (adjust the condition as needed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        #time.sleep(3)
        

        # Get the new URL
        new_url = driver.current_url
        print(f"Nueva URL: {new_url}")
        
        # Add the new URL to the list
        new_urls.append(new_url)

        # Check if we reached the batch size
        if len(new_urls) >= batch_size:
            save_urls_to_file(new_urls, batch_number)
            new_urls = []  # Reset the list for the next batch
            batch_number += 1

    except Exception as e:
        print(f"Error procesando {original_url}: {e}")

# Save any remaining URLs
if new_urls:
    save_urls_to_file(new_urls, batch_number)

# Close the browser
driver.quit()

print("Proceso completado.")