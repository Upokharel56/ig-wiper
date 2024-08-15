import logging
import pathlib
import platform
import random
import sys
import time
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#this imports all necessary functions from driver_functions.py file note name of file should be same even cases should be same
from driver_functions import *




logging.basicConfig(format="[%(levelname)s] instagram-activities-wipe: %(message)s", level=logging.INFO)

# Do not edit
MODE = -1
CHECK_EVERY = -1
LIKES_URL = "https://www.instagram.com/your_activity/interactions/likes"
COMMENTS_URL = "https://www.instagram.com/your_activity/interactions/comments"

# Default: delete 10 likes at once. You can change this if you want to delete more at once.
AT_ONCE_DELETE = 10


logging.info("Starting...")



#helper functions are these You may not know the logic so better not edit these



def main_loop():
    # Main loop
    while True:
        # Click select button
        is_clicked_select = False
        while not is_clicked_select:
            logging.info("Waiting for likes to load...")
            time.sleep(2)
            for i in driver.find_elements(By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'):
                if i.text == "Select":
                    for j in driver.find_elements(By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'):
                        if j.text == "No results":
                            logging.info("No " + ("comments" if MODE == 1 else "likes") + " found. DONE. Quitting")
                            driver.quit()
                            sys.exit(0)
                    driver.execute_script("arguments[0].click();", i)
                    time.sleep(2) # Wait for the select button to be clicked frequently prevents being clicked in short time
                    logging.info("Likes loaded")
                    logging.info("Clicked 'Select'")
                    is_clicked_select = True
                    break
                if i.text == "You haven't liked anything":
                    logging.info("No likes found. DONE. Quitting")
                    driver.quit()
                    sys.exit(0)

        # Select all content (Automatically)
        selected_count = 0
        while_it_count = 0
        is_refreshed = False
        while selected_count == 0:
            if is_refreshed:
                break
            time.sleep(1)
            for i in driver.find_elements(By.CSS_SELECTOR, 'div[data-bloks-name="ig.components.Icon"]'):
                if i.get_attribute("style").startswith('mask-image: url("https://i.instagram.com/static/images/bloks/icons/generated/circle__outline'):
                    driver.execute_script("arguments[0].click();", i)
                    time.sleep(1) # Wait and prevent for the select button to be clicked frequently prevents being clicked in short time
                    selected_count += 1
                    logging.info("Selected a like" + " (Total: " + str(selected_count) + ")")
                    if selected_count == AT_ONCE_DELETE:
                        break
            while_it_count += 1
            if while_it_count > 10:
                if CHECK_EVERY == -1:
                    logging.warning("Are you seeing this popup -> 'There was a problem with removing some or all of your content. Try removing it again.' If so, it looks like you have reached the rate limit for remove operations. This is a server-side restriction from Instagram. You can: [1] quit the script now and run it later, or [2] leave it running and it will refresh the page every x hours to check if the rate limit is lifted, and continue unliking posts if it is. (Untested. It may or may not work.)")
                    while (choice := input("Your choice [1/2]: ")).strip() not in ["1", "2"]:
                        pass
                    if choice == "1":
                        logging.info("Quitting...")
                        driver.quit()
                        sys.exit(0)
                    while True:
                        hours_check_every = input("Check every x hour(s) (decimal is allowed, enter nothing to default to 1 hour) [x]: ")
                        try:
                            hours_check_every = float(hours_check_every)
                            break
                        except:
                            pass
                    CHECK_EVERY = int(hours_check_every * 3600)
                    logging.info("Received. Will check every " + str(hours_check_every) + " hour(s). It might not be exact due to some randomization.")
                for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
                    if i.find_element(By.CSS_SELECTOR, "div").text == "OK":
                        driver.execute_script("arguments[0].click();", i)
                        logging.info("Clicked 'OK' on 'Something went wrong' dialog")
                        break
                logging.info("Now we wait...")
                # randomize CHECK_EVERY by a variance of 10%
                time.sleep(random.uniform(CHECK_EVERY * 0.9, CHECK_EVERY * 1.1))
                logging.info(str(hours_check_every) + " hour(s) have passed. Refreshing the page...")
                driver.refresh()
                is_refreshed = True
                continue
        if is_refreshed:
            continue

        # Click delete
        for i in driver.find_elements(By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'):
            if i.text == ("Delete" if MODE == 1 else "Unlike"):
                time.sleep(1)
                driver.execute_script("arguments[0].click();", i)
                time.sleep(3)
                logging.info("Clicked " + ("'Delete'" if MODE == 1 else "'Unlike'"))
                break

        # Confirm delete
        is_clicked_confirmation = False
        while not is_clicked_confirmation:
            time.sleep(3)
            for i in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
                if i.find_element(By.CSS_SELECTOR, "div").text == ("Delete" if MODE == 1 else "Unlike"):
                    driver.execute_script("arguments[0].click();", i)
                    logging.info("Clicked " + ("'Unlike'") + " on confirmation dialog")
                    is_clicked_confirmation = True
                    break




# Start webdriver
driver = start_webdriver()

# Open Instagram likes page
driver.get(LIKES_URL)

# Sign in & Click 'Not now' on 'Save Your Login Info?' dialog
signin_to_instagram(driver, LIKES_URL)


logging.info("Opening " + LIKES_URL)



#start main logic of automation
try:
    main_loop()

except KeyboardInterrupt:
    print()
    logging.info("Quitting on keyboard interrupt...")
    driver.quit()
    sys.exit(0)
except NoSuchWindowException:
    logging.exception("Browser window closed unexpectedly")
    sys.exit(1)
except Exception:
    logging.exception("Unknown error occurred")
    try:
        driver.quit()
    except:
        pass
    sys.exit(1)

