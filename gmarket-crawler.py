import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def load_secrets(filename):
    with open(filename, "r") as f:
        secrets = json.load(f)
    
    return secrets["username"], secrets["password"]

def load_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--start-maximized")
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe", options=options)

    return driver

def login(driver, username, password):
    driver.get("https://gsigninssl.gmarket.co.kr/LogIn/LogIn")
    driver.implicitly_wait(20)
    username_element = driver.find_element_by_css_selector("input#id")
    username_element.send_keys(username)
    password_element = driver.find_element_by_css_selector("input#pwd")
    password_element.send_keys(password)

    submit = driver.find_element_by_css_selector("input#goCheckLogin")
    submit.click()
    
    driver.implicitly_wait(20)

def lucky_draw(driver):
    driver.get("http://gevent.gmarket.co.kr/promotion/AttendRoulette.asp")
    driver.implicitly_wait(20)

    button = driver.find_element_by_css_selector(".button_start")
    button.click()

    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        pass

def event_coupon(driver):
    driver.get("http://gpromotion.gmarket.co.kr/Plan/PlanView?sid=149355")
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"tophtml")))
    
    elements = driver.find_elements_by_css_selector(".btn_download")

    for button in elements:
        for i in range(5):
            val = button.get_attribute("onclick")
            if val != None:
                func = val.split(':')[1]
                driver.execute_script("{};".format(func))
            
            driver.implicitly_wait(3)

    elements = driver.find_elements_by_css_selector(".btn_coupon")

    for button in elements:
        val = button.get_attribute("onclick")
        if val != None:
            func = val.split(':')[1]

            driver.execute_script("{};".format(func))
        driver.implicitly_wait(3)


if __name__ == '__main__':
    username, password = load_secrets("secrets.json")
    driver = load_driver()
    login(driver, username, password)
    
    lucky_draw(driver)
    event_coupon(driver)