from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def get_driver(headless=True):
    opts = Options()
    opts.headless = True
    return webdriver.Firefox()
