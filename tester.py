from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from main import log
import time


def read():
    file1 = open('accounts.txt', 'r')
    count = 0
    accs = []

    for line in file1:
        count += 1
        accs.append(line.strip())

    file1.close()
    log("returning array with " + str(len(accs)) + " accounts")
    return accs


def netflix():
    log("launching webdriver for netflix")
    driver = webdriver.Chrome()
    driver.get("https://www.netflix.com/")
    signIn = driver.find_element_by_link_text("Sign In")
    signIn.click()
    emailInput = driver.find_element_by_id("id_userLoginId")
    passInput = driver.find_element_by_id("id_password")
    a = 0
    credentials = read()
    for acc in credentials:
        email = acc.split(":")[0]
        password = acc.split(":")[1]
# to be continued
