from selenium import webdriver

from selenium.webdriver.common.by import By

import credentials

def get_driver(headless=True):
    opts = Options()
    opts.headless = True
    return webdriver.Firefox()


def login(driver, email, password):
    driver.get("https://www.facebook.com/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()


if __name__ == "__main__":
    driver = get_driver()
    login(driver, credentials.mail, credentials.password)
