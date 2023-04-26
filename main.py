from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pprint
import credentials

class TCOL:
    # Foreground:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End colored text
    END = '\033[0m'
    NC = '\x1b[0m'  # No Color

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
    print(f"{TCOL.FAIL}tag_name{TCOL.END}[{element.tag_name}]")
    attrs=[]
    for attr in element.get_property('attributes'):
        attrs.append([attr['name'], attr['value']])
    for k,v in attrs:
        #if k not in ["class"]:
        print(f"  {TCOL.OKGREEN}{k}{TCOL.END}[{v}]")
    print(f"  {TCOL.OKBLUE}text{TCOL.END}[{element.text}]")
    all_children_by_xpath = element.find_elements(By.XPATH, "./*")
    all_family_by_xpath = element.find_elements(By.XPATH, ".//*")
    print(f"  {TCOL.WARNING}children{TCOL.END}[{len(all_children_by_xpath)}|{len(all_family_by_xpath)}]")

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
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'on your mind')]")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Welcome')]")))
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
    print_element(driver, main)
    feed = main.find_element(By.XPATH, "//div[@role = 'feed']")
    print_element(driver, feed)
    #links = feed.find_elements(By.XPATH, "//a[@role = 'link' and boolean(@aria-label) and contains(@href, '/events')]")
    links = feed.find_elements(By.XPATH, "//a[@role = 'link']")
    for link in links:
        print_element(driver, link)
    print("read_events end")

if __name__ == "__main__":
    driver = get_driver(headless=False)
    login(driver, credentials.mail, credentials.password)
    load_events(driver)
    read_events(driver)
