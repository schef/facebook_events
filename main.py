from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pprint
import credentials

pp = pprint.PrettyPrinter(indent=2)

def get_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("-headless")
    opts.add_argument("--disable-notifications")
    return Chrome(options=opts)

def get_web_element_attribute_names(web_element):
    """Get all attribute names of a web element"""
    # get element html
    html = web_element.get_attribute("outerHTML")
    # find all with regex
    pattern = """([a-z]+-?[a-z]+_?)='?"?"""
    return re.findall(pattern, html)

def print_element(driver, element):
    everything = driver.execute_script(
    'var element = arguments[0];'
    'var attributes = {};'
    'for (index = 0; index < element.attributes.length; ++index) {'
    '    attributes[element.attributes[index].name] = element.attributes[index].value };'
    'var properties = [];'
    'properties[0] = attributes;'
    'var element_text = element.textContent;'
    'properties[1] = element_text;'
    '// var styles = getComputedStyle(element);'
    '// var computed_styles = {};'
    '// for (index = 0; index < styles.length; ++index) {'
    '//     var value_ = styles.getPropertyValue(styles[index]);'
    '//     computed_styles[styles[index]] = value_ };'
    '// properties[2] = computed_styles;'
    'return properties;', element)
    pp.pprint(everything)

def accept_cookies(driver):
    print("accept_cookies start")
    search_text = "Allow essential and optional cookies"
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[@title=\"{search_text}\"]"))).click()
    print("accept_cookies end")

def login(driver, email, password):
    print("login start")
    driver.get("https://www.facebook.com/login")
    accept_cookies(driver)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.TAG_NAME, "form").submit()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'on your mind')]")))
    print("login end")

def load_events(driver):
    print("load_events start")
    driver.get("https://www.facebook.com/events/search/?q=%C4%8Cakovec")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='feed']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Dates')]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'This Weekend')]"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='feed']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@role = 'link' and boolean(@aria-label)]")))
    driver.implicitly_wait(5)
    print("load_events end")

def read_events(driver):
    print("read_events start")
    main = driver.find_element(By.XPATH, "//div[@role = 'main']")
    feed = main.find_element(By.XPATH, "//div[@role = 'feed']")
    links = feed.find_elements(By.XPATH, "//a[@role = 'link' and boolean(@aria-label) and contains(@href, 'events/')]")
    for link in links:
        print_element(driver, link)
        #print(link.get_attribute("aria-label"))
        #print(link.get_property('attributes')[0].keys())
    print("read_events end")

def open_facebook(driver):
    driver.get("https://www.facebook.com")

if __name__ == "__main__":
    driver = get_driver(headless=False)
    login(driver, credentials.mail, credentials.password)
    load_events(driver)
    read_events(driver)
