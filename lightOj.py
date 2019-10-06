from selenium import webdriver
import time
import os
from selenium.common.exceptions import NoSuchElementException
import getpass


user_name = input('Enter Your Handle / Email: ')
user_password = getpass.getpass()
wait_time = 3


def get_extension(language):
    if language == 'C++':
        return '.cpp'
    elif language == 'C':
        return '.c'
    elif language == 'JAVA':
        return '.java'
    else:
        return '.txt'


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

driver = webdriver.Chrome(chrome_options=options)

# logging in

print("Logging in")

driver.get("http://lightoj.com/login_main.php")
userForm = driver.find_element_by_id('myuserid')
passwordForm = driver.find_element_by_id('mypassword')
userForm.send_keys(user_name)
passwordForm.send_keys(user_password)
driver.find_element_by_name('Submit').click()
time.sleep(wait_time)
if driver.current_url == "http://lightoj.com/login_main.php":
    print("Login failed")
    driver.quit()
    exit(0)


driver.get("http://lightoj.com/volume_usersubmissions.php")
driver.find_element_by_name('user_password').send_keys(user_password)
driver.find_element_by_name('submit').click()
time.sleep(wait_time)


links = driver.find_elements_by_xpath('//*[@id="mytable3"]/tbody/tr/th/a')
problemNamesWebElements = driver.find_elements_by_xpath(
    '//*[@id="mytable3"]/tbody/tr/td[2]/a')
languagesWebElements = driver.find_elements_by_xpath(
    '//*[@id="mytable3"]/tbody/tr/td[3]')
verdicts = driver.find_elements_by_xpath('//*[@id="mytable3"]/tbody/tr/td[6]')


urls = []
problemNames = []
languages = []
for i in range(len(links)):
    if i % 50 == 0 and i > 0 :
        print(str(i) + " Links processed")
    if verdicts[i].text == 'Accepted':
        urls.append(links[i].get_attribute('href'))
        problemNames.append(problemNamesWebElements[i].text.replace('?', ''))
        languages.append(languagesWebElements[i].text)


print("Total Accepted Codes : " + str(len(urls)))

for i in range(len(urls)):
    directory = os.path.join(os.getcwd(), 'LightOj ' + user_name)
    path = os.path.join(
        directory, problemNames[i] + get_extension(languages[i]))
    
    # only downloading recent ac submission of a problem
    if os.path.exists(path):
        continue
    
    driver.get(urls[i])
    sourceCode = driver.find_element_by_xpath(
        '/html/body/div[3]/div/table[2]/tbody/tr[2]/td/div[3]/div').text
    if not os.path.exists(directory):
        os.makedirs(directory)
    f = open(path, 'w+')
    f.write(sourceCode)
    f.close()
    print('Download completed: ' + str(float("%0.2f" %
                                             (((i+1) * 100) / len(urls)))) + "%")
    time.sleep(wait_time)

driver.quit()
