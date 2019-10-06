from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import os
import getpass
import string


user_name = input('Enter Your User Name: ')
user_password = getpass.getpass()
wait_time = 2
# change to False if you don't want headless chrome
headless = True


def format_filename(s):
    valid_chars = "-_.()& %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename


def get_extension(language):
    if language == 'C++':
        return '.cpp'
    elif language == 'C':
        return '.c'
    elif language == 'Java':
        return '.java'
    elif language == 'Python':
        return '.py'
    else:
        return '.txt'


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
if headless:
    options.add_argument("--headless")
    options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

# logging in

print("Logging in")

driver.get("https://vjudge.net")
driver.find_element_by_class_name('login').click()
time.sleep(wait_time)

userForm = driver.find_element_by_id('login-username')
passwordForm = driver.find_element_by_id('login-password')
userForm.send_keys(user_name)
passwordForm.send_keys(user_password)
driver.find_element_by_id('btn-login').click()
time.sleep(wait_time)

try:
    driver.find_element_by_id('login-alert')
    print("Login failed")
    driver.quit()
    exit(0)
except:
    print("Login Successful")

totalAcceptedSolutions = 0


driver.get("https://vjudge.net/status")
driver.find_element_by_class_name('search_text').send_keys(user_name)
Select(driver.find_element_by_id('res')).select_by_value('1')
time.sleep(7)

print("Iterating through all the submission page")
pageNumber = 1

while True:
    solutionPopUp = driver.find_elements_by_class_name('language')
    print("In Submission Page " + str(pageNumber))
    if len(solutionPopUp) == 1:
        break
    totalAcceptedSolutions += len(solutionPopUp) - 1
    driver.find_element_by_xpath('//*[@id="listStatus_next"]/a').click()
    pageNumber += 1
    time.sleep(wait_time)

# Going back to first submission page
driver.find_element_by_xpath(
    '//*[@id="listStatus_paginate"]/ul/li[2]/a').click()
time.sleep(wait_time)


print("Total Accepted Submission: " + str(totalAcceptedSolutions))

if totalAcceptedSolutions == 0:
    exit(0)

completed = 0

sourceCodes = []
problemLinks = []
OJs = []
languages = []

while True:
    solutionPopUp = driver.find_elements_by_class_name('language')
    if len(solutionPopUp) == 1:
        break
    OjNameWebElements = driver.find_elements_by_xpath(
        '/html/body/div[1]/div/div[2]/div/table/tbody/tr/td[3]')

    for i in range(len(OjNameWebElements)):
        OJs.append(OjNameWebElements[i].text)
        languages.append(solutionPopUp[i+1].text)
        # Ei jaygay bari khay :3
        solutionPopUp[i+1].click()
        time.sleep(wait_time)
        sourceCodes.append(driver.find_element_by_tag_name('pre').text)
        completed += 1
        print('Completed: ' + str(float("%0.2f" %
                                                 ((completed * 100) / (totalAcceptedSolutions * 2)))) + "%")
        problemLinks.append(driver.find_element_by_xpath(
            '//*[@id="solutionModalLabel"]/a[3]').get_attribute('href'))
        driver.find_element_by_class_name('close').click()
        time.sleep(wait_time)

    driver.find_element_by_xpath('//*[@id="listStatus_next"]/a').click()
    time.sleep(wait_time)

for i in range(len(problemLinks)):
    driver.get(problemLinks[i])
    time.sleep(wait_time)
    problemName = driver.find_element_by_xpath('//*[@id="prob-title"]/h2').text

    directory = os.path.join(os.getcwd(), 'Vjudge ' + user_name, OJs[i])

    path = os.path.join(
        directory, format_filename(problemName) + get_extension(languages[i]))

    # only downloading recent ac submission of a problem
    if os.path.exists(path):
        completed += 1
        print('Completed: ' + str(float("%0.2f" %
                                                 ((completed * 100) / (totalAcceptedSolutions * 2)))) + "%")
        continue

    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(path, 'w+')
    f.write(sourceCodes[i])
    f.close()
    completed += 1
    print('Completed: ' + str(float("%0.2f" %
                                             ((completed * 100) / (totalAcceptedSolutions * 2)))) + "%")


driver.quit()
