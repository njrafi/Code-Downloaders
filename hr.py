from selenium import webdriver
import time
import os
from selenium.common.exceptions import NoSuchElementException
import getpass
import tkinter as tk
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import string
import platform

user_name = input('Enter Your User Name: ')
user_password = getpass.getpass()
wait_time = 2

def getClipboardText():
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    return root.clipboard_get()


def format_filename(s):
    valid_chars = "-_.()& %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename


def get_extension(language):
    if 'C++' in language:
        return '.cpp'
    elif 'C' in language:
        return '.c'
    elif 'MySQL' in language:
        return '.sql'
    elif 'Java' in language:
        return '.java'
    elif 'Python' in language:
        return '.py'
    elif 'Ruby' in language:
        return '.rb'
    elif 'Swift' in language:
        return '.swift'
    elif 'PHP' in language:
        return '.php'
    else:
        return '.txt'


cntrlOrCommand = Keys.CONTROL

if platform.system() == "Darwin":
    cntrlOrCommand = Keys.META

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

driver = webdriver.Chrome(options=options)

# logging in

print("Logging in")

driver.get("https://www.hackerrank.com/auth/login")
userForm = driver.find_element_by_id('input-1')
passwordForm = driver.find_element_by_id('input-2')
userForm.send_keys(user_name)
passwordForm.send_keys(user_password)
driver.find_element_by_class_name('auth-button').click()
time.sleep(wait_time)
if driver.current_url == "https://www.hackerrank.com/auth/login":
    print("Login failed")
    driver.quit()
    exit(0)

contests = []

# Getting all contests
driver.get("https://www.hackerrank.com/" + user_name)
time.sleep(wait_time)
while True:
    try:
        loadMoreButton = driver.find_element_by_xpath(
            '//*[@id="content"]/div/div/div[2]/div[3]/article/div/div[2]/section[6]/div/div[2]/button')
        loadMoreButton.click()
        time.sleep(wait_time)
        print('Load More Button Clicked')
    except:
        break

contestLinkWebElements = driver.find_elements_by_class_name('contest-name')
for i in range(len(contestLinkWebElements)):
    contests.append(contestLinkWebElements[i].get_attribute(
        'href').split('?')[0] + '/submissions')
contests.append("https://www.hackerrank.com/submissions")


# all global variables
problemNames = []
languages = []
sourceCodeLinks = []
submissionPage = 1

for contestPage in contests:
    driver.get(contestPage)
    time.sleep(wait_time)

    while True:
        print("In Submission Page " + str(submissionPage))
        submissionPage += 1
        problemNamesWebElements = driver.find_elements_by_xpath(
            '//*[@id="content"]/div/section/div/div/div[1]/div/div/div[1]')
        languagesWebElements = driver.find_elements_by_xpath(
            '//*[@id="content"]/div/section/div/div/div[1]/div/div/div[2]')
        sourceCodeLinksWebElements = driver.find_elements_by_class_name(
            'view-results')
        verdictsWebElements = driver.find_elements_by_xpath(
            '//*[@id="content"]/div/section/div/div/div[1]/div/div/div[4]')
        for i in range(len(problemNamesWebElements)):
            if "Accepted" in verdictsWebElements[i].text:
                sourceCodeLinks.append(
                    sourceCodeLinksWebElements[i].get_attribute('href'))
                problemNames.append(format_filename(
                    problemNamesWebElements[i].text))
                languages.append(languagesWebElements[i].text)
        # Go to Next Page If Available
        try:
            rightButton = driver.find_element_by_css_selector(
                "a[data-attr1 = 'Right']")
            if rightButton.get_attribute('href') is None:
                break
            print("Right Button Found")
            rightButton.click()
            time.sleep(wait_time)
        except:
            print("No Right Button")
            break


print("Total Accepted Codes : " + str(len(problemNames)))
for i in range(len(problemNames)):
    problemName = problemNames[i]
    language = languages[i]

    directory = os.path.join(
        os.getcwd(), 'HackerRank ' + user_name)
    path = os.path.join(directory, problemName +
                        get_extension(language))
    print("downloading " + problemName)

    if os.path.exists(path):
        print("Already Downloaded")
        continue

    driver.get(sourceCodeLinks[i])
    time.sleep(wait_time)

    # copying the source code
    try:
        codeWindow = driver.find_element_by_class_name('CodeMirror-lines')
        codeWindow.click()
        ActionChains(driver).key_down(cntrlOrCommand).send_keys(
            'a').send_keys('c').key_up(cntrlOrCommand).perform()
        sourceCode = getClipboardText()
    except:
        print("Error in Submission Page")

    if len(problemName) > 0 and len(sourceCode) > 0:
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(path, 'w+')
        f.write(sourceCode)
        f.close()
    print('Download completed: ' + str(float("%0.2f" %
                                             (((i+1) * 100) / len(problemNames)))) + "%")

driver.quit()
