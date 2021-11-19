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
    print("NETFLIX")
    print("Disney+")
    userInput = input("Choose website: ")
    log("User input == " + userInput)
    if (userInput.upper() == "NETFLIX"):
        tester.netflix()


if __name__ == '__main__':
    main()
