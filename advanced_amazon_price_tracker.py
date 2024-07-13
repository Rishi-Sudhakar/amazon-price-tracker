import csv
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import schedule

# List of products to track (URL, name, threshold price)
products = [
    ("https://www.amazon.in/product_name/dp/somerandomnumber", "Example Product 1", 1000),
    ("https://www.amazon.in/product/db/somerandomnumber", "Example Product 2", 500),
    # Add more products as needed, ANY AMAZON product, I'll just leave it for now
]

def get_amazon_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))
        )
        price = price_element.text.replace(",", "")  # Remove commas from price
        return int(price)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        driver.quit()

def update_price_history(product_name, price):
    filename = "price_history.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, product_name, price])
    except Exception as e:
        print(f"Error writing to CSV: {e}")

def check_prices():
    for url, name, threshold in products:
        price = get_amazon_price(url)
        if price:
            print(f"The current price of {name} is: ₹{price}")
            update_price_history(name, price)
            if price < threshold:
                print(f"Price alert! {name} is below ₹{threshold}")
                # We'll add email notification here later (Well the authentication had to be done is secrets :( so its still under development)
        else:
            print(f"Failed to retrieve the price for {name}")

def run_price_checker():
    print("Checking prices...")
    check_prices()
    print("Done checking prices.")

# Schedule the price checker to run every hour
schedule.every(1).hours.do(run_price_checker)

if __name__ == "__main__":
    print("Amazon Price Tracker started. Press Ctrl+C to stop.")
    run_price_checker()  # Run once immediately (meaning that you just just manually do it by this)
    while True:
        schedule.run_pending()
        time.sleep(1)