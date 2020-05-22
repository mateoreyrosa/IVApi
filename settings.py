from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from dotenv import load_dotenv


def load_config():
    load_dotenv()


# Gets an instance of the webdriver and configures options
def getDriver(startUrl):
    driver = webdriver.Chrome(options=getOptions())
    driver.get(startUrl)
    return driver


# Sets the options for the webdriver
def getOptions():
    options = Options()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    width = 1500
    height = 900

    ua = UserAgent()
    userAgent = ua.random

    user_agent = f'user-agent={userAgent}'
    window_size = f"window-size={width},{height}"
    options.add_argument(user_agent)
    options.add_argument(window_size)

    print(user_agent)
    print(window_size)

    return options
