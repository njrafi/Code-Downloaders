from selenium import webdriver
import time
import os
from selenium.common.exceptions import NoSuchElementException
import getpass
import tkinter as tk

user_name = input('Enter Your Handle / Email: ')
user_password = getpass.getpass()
wait_time = 2
user_to_download = user_name


def getClipboardText():
    root = tk.Tk()
    # keep the window from showing
    root.withdraw()
    return root.clipboard_get()


def get_extension(language):
    if 'C++' in language:
        return '.cpp'
    elif 'JAVA' in language:
        return '.java'
    elif 'PYTH' in language:
        return '.py'
    elif 'C' in language:
        return '.c'
    else:
        return '.txt'


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

driver = webdriver.Chrome(chrome_options=options)

# logging in

print("Logging in")

driver.get("https://www.codechef.com/")
userForm = driver.find_element_by_name('name')
passwordForm = driver.find_element_by_name('pass')
userForm.send_keys(user_name)
passwordForm.send_keys(user_password)
driver.find_element_by_name('op').click()
time.sleep(wait_time)


if driver.current_url == "https://www.codechef.com/":
    print("Login failed")
    driver.quit()
    exit(0)

if driver.current_url == "https://www.codechef.com/session/limit":
    boxes = driver.find_elements_by_class_name('form-checkbox')
    for i in range(len(boxes) - 1):
        boxes[i].click()
    driver.find_element_by_name('op').click()


driver.get("https://www.codechef.com/users/" + user_to_download)
submissions = driver.find_elements_by_tag_name('a')
links = []
for submission in submissions:
    link = submission.get_attribute('href')
    if link is not None and link.endswith(user_to_download):
        links.append(link)
        # print(link)

completed = 0
for link in links:
    driver.get(link)
    time.sleep(wait_time)
    try:
        verdicts = driver.find_elements_by_xpath(
            '//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[4]/span')
        source_links = driver.find_elements_by_xpath(
            '//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[8]/ul/li/a')
        languages = driver.find_elements_by_xpath(
            '//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[7]')
    except:
        print("Error Occured in submission page")
    problemName = ""
    sourceCode = ""
    probableProblemNameLinks = driver.find_elements_by_xpath(
        '//*[@id="breadcrumb"]/div/a')
    for probableProblemNameLink in probableProblemNameLinks:
        if "problems" in probableProblemNameLink.get_attribute('href'):
            problemName = probableProblemNameLink.text.replace('?', '')
    assert(len(verdicts) == len(source_links))

    for i in range(len(verdicts)):
        if verdicts[i].get_attribute('title') == "accepted" or "100" in verdicts[i].text:

            language = languages[i].text
            directory = os.path.join(
                os.getcwd(), 'CodeChef ' + user_to_download)
            path = os.path.join(directory, problemName +
                                get_extension(language))
            if os.path.exists(path) == False:
                try:
                    driver.get(source_links[i].get_attribute('href'))
                    time.sleep(wait_time)
                    driver.find_element_by_id(
                        'copy-button').click()
                    sourceCode = getClipboardText()
                except:
                    print("Error Occured in source code page")
            else:
                print(problemName + " Already Downlaoded")
            if len(problemName) > 0 and len(sourceCode) > 0:
                if not os.path.exists(directory):
                    os.makedirs(directory)
                f = open(path, 'w+')
                f.write(sourceCode)
                f.close()
            break
    completed += 1
    print('Download completed: ' + str(float("%0.2f" %
                                             ((completed * 100) / len(links)))) + "%")


driver.quit()
