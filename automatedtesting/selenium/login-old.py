# #!/usr/bin/env python
import time
import syslog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

# Creating and Configuring Logger

Log_Format = "%(asctime)s - %(message)s"
logging.basicConfig(filename="seleniumTest",
                    filemode="w",
                    format=Log_Format,
                    level=logging.INFO)

logger = logging.getLogger()
def log(string):
    syslog.syslog(syslog.LOG_INFO, string);
    print(string)
    logger.info(string);

options = ChromeOptions()
options.add_argument("--headless")


delay = 30
browser = webdriver.Chrome(options=options)
log('Starting the browser...')

def login(email, password):
    try:
        loginButton = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.login")))
        loginButton.click()
        log('Navigating to login.')
        email_input = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#email")))
        email_input.send_keys(email)
        log('set email: ' + email)
        browser.find_element(by=By.CSS_SELECTOR,
                             value="#passwd").send_keys(password)
        log('set password: ' + password)
        browser.find_element(by=By.CSS_SELECTOR,
                             value="#SubmitLogin").click()
        log('Login successfully with username: ' +
                    email + ',password: ' + password)
    except TimeoutException:
        log("Loading took too much time in login!")


def goHome():
    log('Going home!')
    try:
        home = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#header_logo>a")))
        home.click()
    except TimeoutException:
        log("Home is too far to come back!")


def addProduct():
    
    log('Adding product!')
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#homefeatured li .button-container a.ajax_add_to_cart_button")))
        list_products = browser.find_elements(
            by=By.CSS_SELECTOR, value="#homefeatured li")
        for idx, product in enumerate(list_products):
            WebDriverWait(product, delay).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-container a.ajax_add_to_cart_button")))
            WebDriverWait(product, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".product-name")))
            productName = product.find_element(
                By.CSS_SELECTOR, ".product-name").text
            button = product.find_element(
                By.CSS_SELECTOR, ".button-container a.ajax_add_to_cart_button")
            button.click()
            time.sleep(0.3)
            try:
                WebDriverWait(browser, delay).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "#layer_cart")))
                WebDriverWait(browser, delay).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "span.continue.btn.btn-default.button.exclusive-medium"))).click()
            except TimeoutException:
                WebDriverWait(browser, delay).until(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".fancybox-outer h1"), "Resource Limit Is Reached"))
                log("Server is running out of memory")

            time.sleep(0.3)
            log(f'Add {productName} to cart')
        quantity = browser.find_element(
            by=By.CSS_SELECTOR, value=".shopping_cart .ajax_cart_quantity")
        log(f'Product has been added: {quantity.text}')
    except TimeoutException:
        log("Add product to cart failed because of timeout!")

def deleteProduct():
    try:
        WebDriverWait(browser, delay).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".shopping_cart > a"))).click()
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart_delete > div > a")))
        WebDriverWait(browser, delay).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart_delete > div > a")))
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table#cart_summary > tbody > tr")))
        list_products = browser.find_elements(
            By.CSS_SELECTOR, "table#cart_summary > tbody > tr")
        time.sleep(2)
        for idx, row_product in enumerate(list_products):
            WebDriverWait(row_product, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart_description > p.product-name > a")))
            productName = row_product.find_element(
                By.CSS_SELECTOR, ".cart_description > p.product-name > a").text

            WebDriverWait(row_product, delay).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart_delete > div > a"))).click()
            log(f"Delete {productName} from cart")

        WebDriverWait(browser, delay * 3).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "#order-detail-content")))
        WebDriverWait(browser, delay).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#center_column .alert.alert-warning"), "Your shopping cart is empty."))
        log(f"Cart is empty now!")
    except TimeoutException:
        log("Delete product failed because of timeout")

# tryTime = 1;
# totalTry = 10
# browser.get('http://automationpractice.com/')
# time.sleep(2)
# while tryTime <= totalTry:
#     if (browser.find_element(By.CSS_SELECTOR, "h1").text.lower() == "resource limit is reached"):
#         tryTime += 1
#         browser.get('http://automationpractice.com/')
#         log(f"Domain resource is reached, try {tryTime} time")
#         time.sleep(5)
#         continue
#     else:
#         break

# if (tryTime <= totalTry):
    login('bnh.bkap.2011@gmail.com', '123456aA@')
    goHome()
    addProduct()
    deleteProduct()
# else:
#     log(f"Test failed! Something went wrong!")
#     exit(1)