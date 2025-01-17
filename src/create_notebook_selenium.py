from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time
import logging

from constants import *

def setup() -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-first-run")
    options.add_argument("--start-maximized")
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(options=options)
    driver.get("https://notebooklm.google.com/")

    return driver

def teardown(driver: webdriver) -> None:
    driver.quit()

def find_and_click_button(wait: WebDriverWait, xpath: str) -> None:
    """Waits for given button xpath to be clickable and clicks"""
    wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def submit_form_input(wait: WebDriverWait, xpath: str, text: str) -> None:
    """Inserts text to input and hits 'RETURN' key"""
    elem = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elem.send_keys(text)
    time.sleep(1)  # Take a breath
    elem.send_keys(Keys.RETURN)

def create_notebooklm(paper_url: str) -> None:
    """Creates a new NotebookLM with audio summary of the 
    given paper in the url.

    Uses selenium webdriver to automate:
      opening the browser,
      navigate to NotebookLM website,
      login to google,
      generate a new Notebook with the given paper url,
      share with personal gmail.
    """
    log_path = "D:\\Git\\bioinfo_notebooklm\\logs\\log.txt"
    logger = logging.getLogger('selenium')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_path)
    logger.addHandler(handler)

    driver = setup()

    # Setup wait for later
    wait = WebDriverWait(driver, 20)

    # Login to google account
    print("Login to google account...")

    # Insert email
    submit_form_input(wait=wait, xpath=EMAIL_INPUT, text=GM_MAIL)

    # Insert pasword
    submit_form_input(wait=wait, xpath=PASSWORD_INPUT, text=GM_PASSWORD)

    # Create notebook
    print("Creating new notebook...")

    # Clicks 'Create' button
    find_and_click_button(wait=wait, xpath=CREATE_BUTTON)

    # Clicks 'website' button
    find_and_click_button(wait=wait, xpath=WEBSITE_BUTTON)

    # Paste link to paper
    submit_form_input(wait=wait, xpath=URL_INPUT, text=paper_url)
    time.sleep(30)  # implicit wait of a few seconds before going for audio

    # Generate audio
    print("Creating audio summary...")

    # Clicks 'Generate' button
    find_and_click_button(wait=wait, xpath=GENERATE_AUDIO_BUTTON)
    time.sleep(10) # implicit wait of additional 10 seconds before sharing

    # Share
    print("Sharing notebook...")

    # Clicks 'Share' button
    find_and_click_button(wait=wait, xpath=SHARE_BUTTON)

    # Submit target email and cick share
    submit_form_input(wait=wait, xpath=TARGET_MAIL_INPUT, text=TARGET_GMAIL)
    # Implicitly wait 2 seconds before attempting to click share button
    time.sleep(2)

    # Clicks second share button
    find_and_click_button(wait=wait, xpath=SHARE_TO_TARGET_BUTTON)

    print(f"Notebook created and shared to {TARGET_GMAIL}!")

    teardown(driver)