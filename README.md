# Code Downloaders

Download your Accepted codes from different online judges ( Current support : Codeforces, CodeChef, LightOj, HackerRank )

### Prerequisites

1. Install python 3 ( https://www.python.org/downloads/ )
2. Install Google Chrome ( Update to latest version if already installed)
3. Install Selenium : `pip install selenium`

### For Windows
1. download chromedriver.exe and copy it to project folder ( https://chromedriver.chromium.org/downloads )
2. Make Sure the chromedriver version support the chrome version you are using

### For Mac
1. install homebrew ` /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" `
2. install chromedriver using homebrew `brew cask install chromedriver`


### Codeforces
- for Windows `python cf.py`
- for Mac `python3 cf.py`

### CodeChef
- for Windows `python cc.py`
- for Mac `python3 cc.py`

### LightOj
- for Windows: `python loj.py`
- for Mac: `python3 loj.py`

### HackerRank
- for Windows: `python hr.py`
- Mac is not supported currently

## Note
- Check the code if you are afraid of inputting your userName and password
- Logging in is needed because of
  - Codeforces Gym submissions
  - CodeChef Captcha Check
  - LightOj Website is not even browsable without login

## Acknowledgments
* Got the idea from https://github.com/dipta007/codeforce-code-downloader_gym_regular , Does exactly the same thing. Just wanted to implement it on my own.
