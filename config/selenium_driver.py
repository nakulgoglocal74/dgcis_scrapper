from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def get_driver_object():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1400,1500")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9230")
    driver = webdriver.Chrome(options=options)
    
    return driver

def radio_click(driver,path):
    radio = driver.find_element(By.CSS_SELECTOR, path)
    radio.click()
    
def input_box(driver,path,data):
    content = driver.find_element(By.CSS_SELECTOR,path)
    content.send_keys(data)
    
def select_box(driver,path,data):
    s = Select(driver.find_element(By.CSS_SELECTOR, path))
    s.select_by_visible_text(data)
    
def get_select_options(driver,path):
    opt = Select(driver.find_element(By.CSS_SELECTOR, path))
    options = [i.text for i in opt.options]
    return options

def get_text(driver,path):
    content = driver.find_element(By.CSS_SELECTOR,path)
    return content.text

def check_element_present(driver,path):
    content = driver.find_elements(By.CSS_SELECTOR,path)
    if content:
        return True 
    else:
        return False