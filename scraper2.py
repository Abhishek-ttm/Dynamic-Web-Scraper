from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Start with maximized window

# Initialize the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the target URL
try:
    driver.get('https://www.otipy.com')
    time.sleep(10)
except Exception as e:
    print(f"Error while opening the website: {e}")

# Handle popup
try:
    close_button = driver.find_element(By.CLASS_NAME, 'style_icon__nNhfo')
    close_button.click()
    time.sleep(5)

    close_button = driver.find_element(By.CSS_SELECTOR, '.style_icon__nNhfo')
    close_button.click()

    print("Popup closed successfully.")
except Exception as e:
    print(f"Error while closing popup: {e}")

# Navigate to the vegetables category page
try:
    driver.get('https://www.otipy.com/category/vegetables-1')
    time.sleep(5)
except Exception as e:
    print(f"Error while navigating to the category page: {e}")

# Lazy scrolling to load all products
try:
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(7)
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
except Exception as e:
    print(f"Error during scrolling: {e}")

# Extract product details
try:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    products = []
    for product in soup.find_all('div', class_='style_card_details__qi0G9'):
        try:
            product_image = product.find('img', class_='style_card_img__RJxGM')['src']
            image_url = "https://www.otipy.com" + product_image
        except Exception as e:
            image_url = 'No image found'
            print(f"Error retrieving image: {e}")

        try:
            product_name = product.find('h3', class_='style_prod_name__QllSp').text.strip()
        except Exception as e:
            product_name = 'No name found'
            print(f"Error retrieving product name: {e}")

        try:
            product_acprice = product.find('span', class_='style_striked_price__4ghn5').text.strip()
            product_acprice = product_acprice.replace('\u20b9', 'Rs.').replace('\u00a0', ' ')
        except Exception as e:
            product_acprice = 'No MRP found'
            print(f"Error retrieving MRP: {e}")

        try:
            product_price = product.find('span', class_='style_selling_price__GaIsF').text.strip()
            product_price = product_price.replace('\u20b9', 'Rs.').replace('\u00a0', ' ')
        except Exception as e:
            product_price = 'No selling price found'
            print(f"Error retrieving selling price: {e}")

        try:
            product_final = product.find('p', class_='style_final_price__FERLK').text.strip()
            product_final = product_final.replace('\u20b9', 'Rs.').replace('\u00a0', ' ')
        except Exception as e:
            product_final = 'No final price found'
            print(f"Error retrieving final price: {e}")

        try:
            product_quantity = product.find('span', class_='style_prod_qt__cXcqe').text.strip()
        except Exception as e:
            product_quantity = 'No quantity found'
            print(f"Error retrieving quantity: {e}")

        # Append the product details to the list
        products.append({
            'Image': image_url,
            'Name': product_name,
            'MRP': product_acprice,
            'Standard Price': product_price,
            'Selling Price': product_final,
            'Quantity': product_quantity
        })
except Exception as e:
    print(f"Error during product extraction: {e}")

# Save the extracted data to a JSON file
with open('grocery_products.json', 'w') as json_file:
    json.dump(products, json_file, indent=4)

# Close the browser
driver.quit()

print("Product data has been saved to 'grocery_products.json'")