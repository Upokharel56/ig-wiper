
def set_driver_path(path):
    # os.environ['PATH'] += r"C:\SeleniumDrivers\chromedriver"
    try:
        os.environ['PATH'] += r"C:\SeleniumDrivers\edgedriver"
    except Exception as e:
        logging.error(f"Error setting path of driver: {e}")
        # sys.exit(1)


def start_webdriver(driver_path):
    set_driver_path(driver_path)
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



def signin_to_instagram(driver, LIKES_URL):
    # Sign in & Click 'Not now' on 'Save Your Login Info?' dialog
    while True:
        if driver.current_url.startswith(LIKES_URL):
            logging.info("Login detected")
            break
        try:
            logging.info(
                "Waiting for sign in... (Please go to the browser and sign in. Don't click anything else after signing in!)")
            wait = WebDriverWait(driver, 60)

            def is_not_now_div_present(driver):
                try:
                    div = driver.find_element(By.CSS_SELECTOR, "div[role='button']")
                except:
                    return False
                return div.text == "Not now"

            wait.until(is_not_now_div_present)
            logging.info("Login detected")
            driver.find_element(By.CSS_SELECTOR, "div[role='button']").send_keys(Keys.ENTER)
            time.sleep(2)
            logging.info("Clicked 'Not now' on 'Save Your Login Info?'")
            time.sleep(1)
            break
        except TimeoutException:
            pass


