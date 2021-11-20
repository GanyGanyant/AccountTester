from termcolor import colored
import datetime
import tester
import os


def clear(): return os.system('cls')


def log(text):
    now = datetime.datetime.now()
    with open("log.txt", "a") as log:
        log.write("[" + now.strftime("%Y-%m-%d %H:%M:%S") + "] " + text + "\n")


def main():
    clear()
    print("loading...")
    log("startup")
    clear()
    print("Available websites:")
    print(colored("1 NETFLIX", "red"))
    print(colored("2 Disney+", "blue"))
    userInput = input("Choose website: ")
    log("User input == " + userInput)
    if (userInput.upper() == "NETFLIX" or userInput == "1"):
        tester.netflix()
    if (userInput.upper() == "DISNEY" or userInput.upper() == "DISNEYPLUS" or userInput.upper() == "DISNEY+" or userInput.upper() == "DISNEY PLUS" or userInput == "2"):
        print("comming soon")


if __name__ == '__main__':
    main()
