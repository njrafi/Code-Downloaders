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
headless = False


def format_filename(s):
    valid_chars = "-_.()& %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    return filename


def get_extension(language):
    if 'C++' in language:
        return '.cpp'
    elif 'Java' in language:
        return '.java'
    elif 'Python' in language:
        return '.py'
    elif 'C' in language:
        return '.c'
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

driver.get("https://www.hackerearth.com/login/")
userForm = driver.find_element_by_id('id_login')
passwordForm = driver.find_element_by_id('id_password')
userForm.send_keys(user_name)
passwordForm.send_keys(user_password)
driver.find_element_by_name('signin').click()

time.sleep(wait_time)
if driver.current_url == "https://www.hackerearth.com/login/":
    print("Login failed")
    driver.quit()
    exit(0)


driver.get('https://www.hackerearth.com/submissions/' + user_name)
time.sleep(wait_time + 5)


problemNames = []
languages = []
sourceCodeLinks = []

# Tracking AC Submission of problems
problemsAlreadyAC = set()

# Process Each Submission Page
def process_page():
    problemNameWebElements = driver.find_elements_by_xpath(
        '/html/body/div[11]/div[3]/div[1]/table/tbody/tr/td[2]/a')
    verdictWebElements = driver.find_elements_by_class_name('result-icon')
    languageWebElements = driver.find_elements_by_xpath(
        '/html/body/div[11]/div[3]/div[1]/table/tbody/tr/td[6]')
    sourceCodeLinkWebElements = driver.find_elements_by_xpath(
        '/html/body/div[11]/div[3]/div[1]/table/tbody/tr/td[7]/a')
    for i in range(len(verdictWebElements)):
        problemName = problemNameWebElements[i].text
        if "Accepted" in verdictWebElements[i].get_attribute('title') and problemName not in problemsAlreadyAC:
            problemNames.append(problemName)
            problemsAlreadyAC.add(problemName)
            languages.append(languageWebElements[i].text)
            sourceCodeLinks.append(
                sourceCodeLinkWebElements[i].get_attribute('href'))
    return


currentPage = 1
while True:
    try:
        print("Processing Page " + str(currentPage))
        process_page()
        nextButton = driver.find_element_by_xpath(
            '//*[@data-gotopage="' + str(currentPage + 1) + '"]')
        currentPage += 1
    except:
        break
    nextButton.click()
    time.sleep(wait_time + 2)


print("Total Accepted Submissions: " + str(len(sourceCodeLinks)))

for i in range(len(languages)):
    directory = os.path.join(os.getcwd(), "HackerEarth " + user_name)
    path = os.path.join(
        directory, format_filename(problemNames[i]) + get_extension(languages[i]))
    # only downloading recent ac submission of a problem
    if os.path.exists(path):
        print('Download completed: ' + str(float("%0.2f" %
                                                 (((i+1) * 100) / len(languages)))) + "%")
        continue
    
    driver.get(sourceCodeLinks[i])
    time.sleep(wait_time)
    sourceUrl = driver.find_element_by_xpath(
        '//*[@id="submission-iframe-light"]').get_attribute('src')
    driver.get(sourceUrl)
    time.sleep(wait_time)

    sourceCodeLines = driver.find_elements_by_xpath('/html/body/pre/ol/li')
    sourceCode = ""
    for line in sourceCodeLines:
        sourceCode += line.text + '\n'

    if not os.path.exists(directory):
        os.makedirs(directory)

    f = open(path, 'w+')
    f.write(sourceCode)
    f.close()
    print('Download completed: ' + str(float("%0.2f" %
                                             (((i+1) * 100) / len(languages)))) + "%")

driver.quit()
