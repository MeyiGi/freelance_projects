from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import winsound  # For Windows sound alert
import re

market_list = [
    "will-wicked-opening-weekend-gross-more-than-twice-gladiator-2",
    "presidential-election-winner-2024?tid=1730809861381",
    "mrbeast-x-ronaldo-video-views-on-day-1-nov-30",
    "bolsonaro-arrested-in-2024",
]


# Set up headless browser options
options = Options()
options.headless = True  # Run in headless mode

# Set up WebDriver (ensure the path to your ChromeDriver executable is configured if needed)
driver = webdriver.Chrome(options=options)

# Set an implicit wait time
driver.implicitly_wait(5)  # Wait up to 5 seconds for elements to load

# Target URL and the element's XPath to monitor
URL = 'https://polymarket.com/event/will-wicked-opening-weekend-gross-more-than-twice-gladiator-2'
TARGET_ELEMENT_XPATH = '__pm_layout'

def get_decimal_after_trump(text):
    # Regular expression to match "Donald Trump" followed by a decimal number
    match = re.search(r'Donald Trump\s+(\d+(\.\d+)?)', text)
    if match:
        return match.group(1)  # Returns the decimal number as a string
    else:
        return None  # If there's no match, return None

# Function to get element content
def get_element_content():
    try:
        driver.get(URL)
        # Wait until the element is present
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, TARGET_ELEMENT_XPATH)))
        text = get_decimal_after_trump(element.text)
        print(text)
        return text if element else None
    except Exception as e:
        print(f"Error retrieving element content: {e}")
        return None

# Initial fetch to get the current content
previous_content = get_element_content()

if previous_content is None:
    print("Could not find the target element.")
else:
    print("Monitoring for changes...")
    try:
        while True:
            time.sleep(1)  # Check every 1 second
            current_content = get_element_content()

            if current_content != previous_content:
                print("Element content has changed!")
                winsound.Beep(1000, 1000)  # Play a beep sound (1000 Hz for 1 second)
                # Update previous content to the new content to continue monitoring
                previous_content = current_content

    finally:
        driver.quit()  # Ensure the driver is closed when done