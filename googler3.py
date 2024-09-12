import os
import random
import subprocess
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

# Define your sudo password
user_password = "christ"

# Define the search query
search_query = "granite countertops melbourne fl"

# Get all VPN config files from the current directory
vpn_files = [f for f in os.listdir('.') if f.endswith('.ovpn')]

# Your original IP address
original_ip = "68.200.225.128"

# Function to get the current IP address
def get_current_ip():
    try:
        ip = requests.get("https://api.ipify.org").text
        print(f"Current IP address: {ip}")
        return ip
    except Exception as e:
        print(f"Could not retrieve IP address: {e}")
        return None

# Function to change IP address using OpenVPN
def change_ip():
    print("Checking if OpenVPN is running...")
    if subprocess.run(["pgrep", "openvpn"], capture_output=True).returncode == 0:
        print("OpenVPN is running. Killing the process...")
        subprocess.run(["sudo", "-S", "killall", "openvpn"], input=f"{user_password}\n", text=True, check=False)
        time.sleep(2)  # Wait for the process to be killed
        print("OpenVPN process killed.")
    else:
        print("OpenVPN is not running.")

    # Randomly select a VPN config file
    vpn_config = random.choice(vpn_files)
    print(f"Connecting to the VPN with config: {vpn_config}...")
    process = subprocess.Popen(["sudo", "-S", "openvpn", "--config", vpn_config], stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.stdin.write(f"{user_password}\n".encode('utf-8'))
    process.stdin.close()  # Close stdin to ensure the process runs independently
    time.sleep(10)  # Wait for the VPN connection to be established
    print("VPN connection established.")

    # Double-check if VPN is running by comparing IP addresses
    current_ip = get_current_ip()
    if current_ip == original_ip:
        print("VPN is not running. Restarting OpenVPN process...")
        change_ip()
    else:
        print("VPN is running successfully.")

# Function to click an element using JavaScript
def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)

# Function to check for CAPTCHA
def check_for_captcha(driver):
    try:
        captcha = driver.find_element(By.XPATH, '//*[contains(@class, "recaptcha")]')
        print("CAPTCHA detected. Restarting the script...")
        return True
    except NoSuchElementException:
        return False

# Main loop
click_count = 0
keyword_index = 0
keywords = ["hammond", "personal", "premium", "K & E", "stonecrafters", "elite", "mayan"]

while True:
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-minimized")  # Open Chrome in a minimized window

        # Set up the Chrome WebDriver
        print("Setting up the Chrome WebDriver...")
        service = Service('chromedriver')  # Update the path to your ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("Chrome WebDriver set up successfully.")

        # Change IP address at the beginning
        print("Changing IP address at the beginning...")
        change_ip()

        # Open Google
        print("Opening Google...")
        driver.get("https://www.google.com")
        print("Google opened successfully.")

        # Check for CAPTCHA
        if check_for_captcha(driver):
            driver.quit()
            continue

        # Find the search box and enter the search query
        print("Finding the search box...")
        search_box = driver.find_element(By.NAME, "q")
        print("Search box found. Entering the search query...")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        print("Search query entered successfully.")

        # Wait for the search results to load
        print("Waiting for the search results to load...")
        time.sleep(3)
        print("Search results loaded.")

        # Check for CAPTCHA after search results load
        if check_for_captcha(driver):
            driver.quit()
            continue

        # Find all the search result links
        print("Finding all the search result links...")
        links = driver.find_elements(By.XPATH, '//a[@href]')
        print(f"Found {len(links)} links.")

        # Debug: Print all captured URLs to understand what is being captured
        print("Printing all captured URLs:")
        for link in links:
            print(link.get_attribute('href'))

        # Filter links to only those containing relevant keywords
        relevant_links = [link for link in links if any(keyword in link.get_attribute('href').lower() for keyword in keywords)]
        print(f"Found {len(relevant_links)} relevant links based on keywords.")

        # Implement round-robin keyword cycling
        for i in range(len(keywords)):
            keyword = keywords[keyword_index]
            filtered_links = [link for link in relevant_links if keyword in link.get_attribute('href').lower()]
            print(f"Clicking on the first match for keyword '{keyword}'")

            if filtered_links:
                href = filtered_links[0].get_attribute('href')
                print(f"Clicking on: {href}")
                try:
                    js_click(driver, filtered_links[0])
                except ElementClickInterceptedException as e:
                    print(f"ElementClickInterceptedException: {e}")
                    continue

                print("Waiting for the page to load...")
                time.sleep(3)  # Wait for the page to load
                print("Page loaded. Going back to the search results page...")
                driver.back()  # Go back to the search results page
                print("Waiting for the search results to reload...")
                time.sleep(3)  # Wait for the search results to reload
                print("Search results reloaded.")

                click_count += 1
                keyword_index = (keyword_index + 1) % len(keywords)  # Move to the next keyword

                # After every 3 clicks, reset the VPN and open a new terminal
                if click_count % 3 == 0:
                    print(f"Completed {click_count} clicks, resetting VPN and opening a new terminal.")
                    driver.quit()  # Close the browser
                    change_ip()  # Change IP
                    # Open a new terminal session to restart the script
                    subprocess.Popen(["gnome-terminal", "--", "python3", "googler.py"])
                    exit()
            else:
                print(f"No match found for keyword '{keyword}'. Moving to the next keyword.")
                keyword_index = (keyword_index + 1) % len(keywords)  # Move to the next keyword

    except Exception as e:
        print(f"An error occurred: {e}. Restarting the script...")
        driver.quit()
        continue

    finally:
        # Close the browser
        print("Closing the browser...")
        driver.quit()
        print("Browser closed.")

        # Disconnect from the VPN
        print("Disconnecting from the VPN...")
        if subprocess.run(["pgrep", "openvpn"], capture_output=True).returncode == 0:
            subprocess.run(["sudo", "killall", "openvpn"], input=f"{user_password}\n", text=True, check=False)
            print("OpenVPN process killed.")
        else:
            print("OpenVPN is not running.")

