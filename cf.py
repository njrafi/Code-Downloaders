from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
from selenium.common.exceptions import NoSuchElementException
import getpass

# important
# update with your credentials
user_name = input('Enter Your Handle / Email: ')
user_password = getpass.getpass()


def get_extension(language):
    if 'C++' in language:
        return '.cpp'
    elif 'Java' in language:
        return '.java'
    elif 'Python' in language:
        return '.py'
    elif 'PyPy' in language:
        return '.py'
    elif 'C' in language:
        return '.c'
    elif 'C#' in language:
        return '.cs'
    elif 'Kotlin' in language:
        return '.kt'
    else:
        return '.txt'


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

driver = webdriver.Chrome(chrome_options=options)

# logging in

print("Logging in")

driver.get("https://codeforces.com/enter")
userForm = driver.find_element_by_id('handleOrEmail')
passwordForm = driver.find_element_by_id('password')
userForm.send_keys(user_name)
passwordForm.send_keys(user_password)
driver.find_element_by_class_name('submit').click()
time.sleep(3)
if driver.current_url == "https://codeforces.com/enter":
    print("Login failed")
    driver.quit()
    exit(0)

driver.get('https://codeforces.com/submissions/' +
           user_name)
pageIndexes = driver.find_elements_by_class_name('page-index')

totalPages = 0

for pageIndex in pageIndexes:
    totalPages = max(totalPages, int(pageIndex.get_attribute('pageindex')))

print("Total Pages " + str(totalPages))

urls = []
filenames = []
submissionIds = []

for page in range(totalPages):
    driver.get('https://codeforces.com/submissions/' +
               user_name + '/page/' + str(page + 1))
    sources = driver.find_elements_by_class_name('view-source')
    verdicts = driver.find_elements_by_class_name('submissionVerdictWrapper')
    problemNames = driver.find_elements_by_xpath('//td[@data-problemid]/a')
    assert(len(sources) == len(verdicts))
    for i in range(len(sources)):
        if verdicts[i].text == 'Accepted':
            url = problemNames[i].get_attribute('href').split(
                'problem')[0] + 'submission/' + sources[i].text
            # print(url)
            urls.append(url)
            submissionIds.append(sources[i].text)
            filenames.append(problemNames[i].text.replace('?', ''))

# print(urls)
print("Total Accepted Codes : " + str(len(urls)))

for i in range(len(urls)):
    print(urls[i])
    try:
        driver.get(urls[i])
        preText = driver.find_element_by_id('program-source-text').text
        directory = os.path.join(os.getcwd(), 'codes')
        language = driver.find_element_by_xpath(
            '//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[2]/td[4]').text
        probId = driver.find_element_by_xpath(
            '//*[@id="pageContent"]/div[2]/div[6]/table/tbody/tr[2]/td[3]/a').text
        path = os.path.join(directory, probId + " -" +
                            filenames[i][3:] + " - " + submissionIds[i] + get_extension(language))
        if not os.path.exists(directory):
            os.makedirs(directory)
        f = open(path, 'w+')
        f.write(preText)
        f.close()
    except NoSuchElementException as ex:
            print("Download Failed: No Such Element")
    except:
            print("Download Failed")
    print('Download completed: ' + str( float( "%0.2f" %  ( ( (i+1) * 100 ) / len(urls ) ) ) ) + "%")


driver.quit()
