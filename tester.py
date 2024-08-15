from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

import os
import platform
import pathlib
import logging,sys

def start_webdriver(driver_path=""):
    os.environ['PATH'] += r"C:\SeleniumDrivers\edgedriver"
    # set_driver_path(driver_path)
    try:
        options = Options()
        # Store login in a Chrome profile
        if platform.system() == "Windows":
            wd = pathlib.Path().absolute()
            options.add_argument(f"user-data-dir={wd}\\chrome-profile")
        else:
            options.add_argument("user-data-dir=chrome-profile")
        driver = webdriver.Edge(options=options)
    except:
        logging.error("Web driver could not start. Have you installed ChromeDriver? Check README for details")
        sys.exit(1)
    logging.info("Opened Chrome browser")
    return driver



driver = start_webdriver()

driver.get("https://www.instagram.com/")

print("test done")
driver.quit()
