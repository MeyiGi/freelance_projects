from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import os
import shutil
import sys
import time
import requests
import random
import wget



def open_choose_category_txt():
    try:
        with open("choose_category.txt", "r") as file:
            content = file.read().strip()[-1]
        
        if content == "2":
            return {"status" : "success", "message" : "selected rent", "ctgr" : "1"}
        elif content == "1":
            return {"status" : "success", "message" : "selected room share", "ctgr" : "2"}
        else:
            raise ValueError("that was invalid number or char. Try again")
        
    except FileNotFoundError as e:
        return {"status" : "error", "message" : "The file 'choose_category.txt' was not found."}
    except ValueError as e:
        return {"status" : "error", "message" : str(e)}
    except Exception as e:
        return {"status" : "error", "message" : f"An unexpected error occurred: {e}"}
    
 

def get_data_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()  # Attempt to parse JSON

        # Safely extract data with default values if keys are missing
        title = data.get("title", "No title provided")
        body = data.get("body", "No body provided")
        city = data.get("city", "No city provided")
        state = data.get("state", "No state provided")
        postal = data.get("postal", "No postal code provided")
        imgs = data.get("imgs", [])

        # Ensure imgs is a list
        if not isinstance(imgs, list):
            raise ValueError("Expected a list of image URLs")

        img_names = [img.split("/")[-1] for img in imgs]

        return {
            "status": "success",
            "message": "Data retrieved successfully",
            "data": {
                "title": title,
                "body": body,
                "city": city,
                "state": state,
                "postal": postal,
                "imgs" : imgs,
                "img_names": img_names
            }
        }

    except requests.exceptions.MissingSchema as e:
        return {"status": "error", "message": f"Invalid URL error: {e}"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "message": f"HTTP error: {e}"}
    except requests.RequestException as e:
        return {"status": "error", "message": f"Network error: {e}"}
    except ValueError as e:
        return {"status": "error", "message": f"Value error: {e}"}
    except KeyError as e:
        return {"status": "error", "message": f"Missing key: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}
        
        
def create_driver():
    try:
        # Configure Chrome options
        options = webdriver.ChromeOptions()

        print("Navigating to the page...")
        driver = webdriver.Chrome(options=options)
        driver.get("https://accounts.craigslist.org/login")

        # Wait feature
        wait = WebDriverWait(driver, 10)

        return {
            "status": "success",
            "message": "WebDriver created and navigated to the page successfully.",
            "driver": driver,
            "wait": wait
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"An error occurred while creating the WebDriver: {e}"
        }
        
        

def login_to_craigslist(driver, wait, email_address, password_text):
    try:
        time.sleep(3)  # Delay to ensure the page is fully loaded

        if driver.current_url == "https://accounts.craigslist.org/login":
            # Handle email input
            try:
                email = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='inputEmailHandle']")))
                email.click()
                email.clear()  # Clear the field before entering text
                email.send_keys(email_address)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error finding input email: {e}"
                }

            # Handle password input
            try:
                password = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='inputPassword']")))
                password.click()
                password.clear()  # Clear the field before entering text
                password.send_keys(password_text)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error finding input password: {e}"
                }

            # Handle login button click
            try:
                button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login")))
                button.click()
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Error finding login button: {e}"
                }

            return {
                "status": "success",
                "message": "Login attempted successfully."
            }
        else:
            return {
                "status": "succes",
                "message": "Login page already bypassed."
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred during login: {e}"
        }
        
        
        
def select_location(driver, wait):
    try:
        # Wait for the button to be clickable and then click it
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[value='go']")))
        button.click()
        return {
            "status": "success",
            "message": "Location selected successfully."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error finding selection input: {e}"
        }
        
        
        
def handle_copy_from_another(driver, wait):
    try:
        print("Handling 'Copy from Another' page...")
        
        # Click the 'Brand New Post' button
        try:
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".brand_new_post")))
            button.click()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error finding 'Brand New Post' button: {e}"
            }
        
        # Click the 'Pick' button
        try:
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".pickbutton")))
            button.click()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error finding 'Pick' button: {e}"
            }
        
        return {
            "status": "success",
            "message": "'Copy from Another' handled successfully."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred while handling 'Copy from Another': {e}"
        }

def handle_subarea_selection(driver, wait):
    try:
        print("Handling 'Subarea' page...")
        
        # Select the subarea input
        try:
            select_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value="1"]')))
            select_element.click()
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error selecting subarea: {e}"
            }
        
        return {
            "status": "success",
            "message": "'Subarea' handled successfully."
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred while handling 'Subarea': {e}"
        }

def handle_page(driver, wait):
    time.sleep(3)
    
    current_url = driver.current_url
    if "copyfromanother" in current_url:
        result = handle_copy_from_another(driver, wait)
        print(result["status"], result["message"])
        if result["status"] == "error":
            sys.exit()
    
    time.sleep(3)
    
    if "subarea" in driver.current_url:
        result = handle_subarea_selection(driver, wait)
        print(result["status"], result["message"])
        if result["status"] == "error":
            sys.exit()
    
    
    
def select_type_by_text(driver, wait, text):
    try:
        print(f'Selecting type with text: {text}')
        
        # Locate the element by its text and click it
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, f'//span[contains(text(), "{text}")]')))
            element.click()
            return {
                "status": "success",
                "message": f"Successfully selected type with text '{text}'"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error finding type with text '{text}': {e}"
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred while selecting type: {e}"
        }
        
        
        
def select_category(driver, wait, ctgr):
    try:
        print(f'Selecting category based on ctgr value: {ctgr}')
        
        # Define the XPath based on ctgr value
        if ctgr == "1":
            xpath = '//span[contains(text(), "apartments / housing for rent")]'
        elif ctgr == "2":
            xpath = '//span[contains(text(), "rooms & shares")]'
        else:
            return {
                "status": "error",
                "message": f"Invalid ctgr value: {ctgr}"
            }
        
        # Locate the category element and click it
        try:
            category = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            category.click()
            return {
                "status": "success",
                "message": "Category selected successfully."
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error finding category element: {e}"
            }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred while selecting category: {e}"
        }
        
        

def fill_price_and_size(driver, wait, price_range, size_range):
    try:
        print("Filling price and size inputs.")
        random_price = random.randint(*price_range)
        random_sqft = random.randint(*size_range)
        
        price_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".short-input .json-form-input")))
        size_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".surface_area .json-form-input")))

        price_input.send_keys(random_price)
        size_input.send_keys(random_sqft)
        return {"status": "success", "message": "Price and size inputs filled."}
    except Exception as e:
        return {"status": "error", "message": f"Error filling price or size input: {e}"}

def select_option(driver, wait, button_selector, menu_item_selector, option_text):
    try:
        print(f"Selecting option '{option_text}'.")
        select_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, button_selector)))
        select_element.click()

        options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, menu_item_selector)))
        for option in options:
            if option_text in option.text:
                option.click()
                return {"status": "success", "message": f"Option '{option_text}' selected."}
        return {"status": "error", "message": f"Option '{option_text}' not found."}
    except Exception as e:
        return {"status": "error", "message": f"Error selecting option '{option_text}': {e}"}

def fill_text_fields(driver, wait, fields):
    try:
        print("Filling title, body, postal, and city.")
        posting_title = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#PostingTitle")))
        descriptions = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea#PostingBody")))

        posting_title.send_keys(fields["title"])
        descriptions.send_keys(fields["body"])

        zipcode = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#postal_code")))
        input_city = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#geographic_area")))

        zipcode.send_keys(fields["postal"])
        input_city.send_keys(fields["city"])

        return {"status": "success", "message": "Text fields filled."}
    except Exception as e:
        return {"status": "error", "message": f"Error filling text fields: {e}"}

def handle_checkboxes(driver, wait, checkboxes):
    try:
        print("Handling checkboxes.")
        for checkbox in checkboxes:
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, checkbox)))
            element.click()
        return {"status": "success", "message": "Checkboxes handled."}
    except Exception as e:
        return {"status": "error", "message": f"Error handling checkboxes: {e}"}

def select_per(driver, wait):
    try:
        print("Selecting 'per' option.")
        per = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ui-id-1-button .ui-selectmenu-text")))
        per.click()

        options = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul[aria-labelledby="ui-id-1-button"] li')))
        for option in options:
            if "month" in option.text:
                option.click()
                return {"status": "success", "message": "Option 'month' selected."}
        return {"status": "error", "message": "Option 'month' not found."}
    except Exception as e:
        return {"status": "error", "message": f"Error selecting 'per': {e}"}
    
    
    
def submit_forms(driver, wait):
    try:
        print("Submitting forms.")
        
        # Click the submit button
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit-button")))
        submit_button.click()
        
        if "geoverify" in driver.current_url:
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.continue.bigbutton")))
            submit_button.click()
        
        # Wait for a significant time to ensure the form is processed (you might want to adjust this)
        time.sleep(3)
        # images
        path = os.path.join(os.getcwd(), "images_from_api")
        
        result = setup_image_directory(path)
        print(result["status"], result["message"])
        if result["status"] == "error":
            sys.exit()

        result = download_images(zip(data["img_names"], data["imgs"]), path)
        print(result["status"], result["message"])
        if result["status"] == "error":
            sys.exit()
            
        result = upload_images(driver, wait, 'input[type="file"]', path, "#doneWithImages")
        print(result["status"], result["message"])
        if result["status"] == "error":
            sys.exit()
            
        # Click the continue button
        continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.bigbutton")))
        time.sleep(3)
        continue_button.click()
        
        return {"status": "success", "message": "Forms submitted successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Error finding or clicking submit buttons: {e}"}
    
    
    
def setup_image_directory(directory_path):
    """
    Prepares the directory for image storage by clearing and recreating it.
    """
    try:
        if os.path.isdir(directory_path):
            shutil.rmtree(directory_path)
        os.mkdir(directory_path)
        return {"status" : "success", "message" : "directory created"}
    except Exception as e:
        return {"status" : "error", "message" : str(e)}

def download_images(img_urls, save_dir):
    """
    Downloads images from provided URLs and saves them in the specified directory.
    """
    try:
        for name, img_url in img_urls:
            save_as = os.path.join(save_dir, name)
            wget.download(img_url, save_as)
        return {"status" : "success", "message" : "Images downloaded successfully"}
    except Exception as e:
        return {"status" : "error" , "message" : str(e)}
def upload_images(driver, wait, file_input_selector, images_directory, done_button_selector):
    """
    Uploads images from the specified directory using the provided file input and done button selectors.
    """
    try:
        file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, file_input_selector)))
    except Exception as e:
        return {"status": "error", "message": f"Error finding file upload input: {e}"}
    
    # Upload images
    for img_file in os.listdir(images_directory):
        img_path = os.path.join(images_directory, img_file)
        file_input.send_keys(img_path)
    
    try:
        done_button = WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.CSS_SELECTOR, done_button_selector)))
        done_button.click()
        return {"status": "success", "message": "Images uploaded successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Error finding done with images button: {e}"}
    
    


def phone_number(driver, wait):
    if "?s=pn" not in driver.current_url:
        return {"status" : "succes", "message" : "phone number page not appeared"}
    try:
        # Get the response from the API
        response = requests.get("https://smsotp24.com/newapiimran/new.php")
        print(type(response.text))
        print(response.text)
        response.raise_for_status()  # Check for HTTP request errors
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # soup = "ACCESS_NUMBER:52278092:12142413721"
        
        text_content = soup.get_text().split(":")
        # text_content = soup.split(":")
        
        phone_number = text_content[-1][1:]
        codegen_url = f"https://smsotp24.com/newapiimran/getsms.php?id={text_content[1]}"
    except Exception as e:
        return {"status": "error", "message": f"Error extracting phone number: {e}"}
    
    try:
        # Enter the phone number
        phone_number_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="pn_number"]')))
        phone_number_input.send_keys(phone_number)
        
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.go.pickbutton')))
        button.click()
    except Exception as e:
        return {"status": "error", "message": f"Error interacting with phone number input: {e}"}
    
    if "?s=pn" in driver.current_url:
        error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'html.json-form-item.error'))).text
        
        return {"status" : "error", "message" : error}
    
    print("waiting for getting code")
    
    try:
        # Get the SMS code from the second API response
        for _ in range(12):
            time.sleep(5)
            response = requests.get(codegen_url)
            response.raise_for_status()  # Check for HTTP request errors
            
            soup = BeautifulSoup(response.text, "lxml")
            soup = soup.get_text()
            print(soup)
            if "error" not in soup:
                break
                
        code = soup.split(":")[-1].strip()
    except Exception as e:
        return {"status": "error", "message": f"Error extracting SMS code: {e}"}
    
    try:
        # Enter the SMS code
        code_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="userCode"]')))
        code_input.send_keys(code)
        
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[name="authstep"]')))
        button.click()
        return {"status": "success", "message": "Phone number and code entered successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Error interacting with code input: {e}"}
    
# def click_final_button(driver, wait, button_selector):
#     """
#     Clicks the final button on the page after waiting for it to become clickable.
#     """
#     try:
#         button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector)))
#         button.click()
#         return {"status": "success", "message": "Final button clicked successfully."}
#     except Exception as e:
#         return {"status": "error", "message": f"Error finding final button: {e}"}

    
    
def extract_and_save_link(driver, link_category, filename="output.txt"):
    try:
        # Locate the link element
        link_element = driver.find_element(By.XPATH, f'//ul[@class="ul"]/li/a[contains(@href, "{link_category}/")]')
        link_url = link_element.get_attribute('href')
        
        # Print the extracted URL
        print('\n\nExtracted URL:', link_url)
        
        # Save the URL to the file
        with open(filename, 'a') as file:
            file.write(link_url + '\n')

        return {"status": "success", "message": "URL extracted and saved successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Error finding link_element"}
    
    
    
# Start data here    
email = "kanybekovdaniel949@gmail.com"
password = "sAmat.2004h"

# email = "kanybekovdaniel369@gmail.com"
# password = "sAmat.2004h"
api_url = "https://adspostin.com/webtest/clcontent/content.php"


# Run functions here
result = open_choose_category_txt()
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()
    
ctgr = result["ctgr"]
    
    
result = get_data_from_api(api_url=api_url)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()
    
data = result["data"]


result = create_driver()
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()

driver = result["driver"]
wait = result["wait"]


result = login_to_craigslist(driver, wait, email, password)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()

result = select_location(driver, wait)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()
    
handle_page(driver, wait)

result = select_type_by_text(driver, wait, "housing offered")
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()


result = select_category(driver, wait, ctgr)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()


if ctgr == "1":
    result = fill_price_and_size(driver, wait, (1600, 1700), (1300, 1400))
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-3-button .ui-selectmenu-text', '#ui-id-3-menu .ui-menu-item', "w/d in unit")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-4-button .ui-selectmenu-text', '#ui-id-4-menu .ui-menu-item',  "attached garage")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-5-button .ui-selectmenu-text', '#ui-id-5-menu .ui-menu-item', "2")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-6-button .ui-selectmenu-text', '#ui-id-6-menu .ui-menu-item',  "2")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
else:
    result = fill_price_and_size(driver, wait, (800, 900), (175, 200))
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-2-button .ui-selectmenu-text', '#ui-id-2-menu .ui-menu-item',  "private")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-4-button .ui-selectmenu-text', '#ui-id-4-menu .ui-menu-item', "private")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-5-button .ui-selectmenu-text', '#ui-id-5-menu .ui-menu-item', "w/d in unit")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
    result = select_option(driver, wait, '#ui-id-6-button .ui-selectmenu-text', '#ui-id-6-menu .ui-menu-item', "attached garage")
    print(result["status"], result["message"])
    if result["status"] == "error":
        sys.exit()
    
result = fill_text_fields(driver, wait, data)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()

result = handle_checkboxes(driver, wait, [
    'input[name="pets_cat"]',
    'input[name="pets_dog"]',
    'input[name="airconditioning"]',
    'input[name="ev_charging"]'
])
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()

result = select_per(driver, wait)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()

result = submit_forms(driver, wait)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()

result = phone_number(driver, wait)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()


time.sleep(2.5)

# Extracting link of post
if ctgr == "1":
    link_category = "apa"
    
if ctgr == "2":
    link_category = "roo"

result = extract_and_save_link(driver, link_category)
print(result["status"], result["message"])
if result["status"] == "error":
    sys.exit()