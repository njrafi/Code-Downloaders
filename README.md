# Code Downloaders

Download your Accepted codes from different online judges ( Current support : Codeforces, CodeChef, LightOj, HackerRank, Vjudge )

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
- for Windows `python codeForces.py`
- for Mac `python3 codeForces.py`

### CodeChef
- for Windows `python codeChef.py`
- for Mac `python3 codeChef.py`

### LightOj
- for Windows: `python lightOj.py`
- for Mac: `python3 lightOj.py`

### HackerRank
- for Windows: `python hackerRank.py`
- for Mac: `python3 hackerRank.py` 
- Mac version is not tested properly yet

### Vjudge
- for Windows: `python vjudge.py`
- for Mac: `python3 vjudge.py`
- If you want to watch what the browser is doing set `headless = False` and don't minimize the browser ( Or It will Crash)

### HackerEarth
- for Windows: `python hackerEarth.py`
- for Mac: `python3 hackerEarth.py`

## Note
- Check the code if you are afraid of inputting your userName and password
- Logging in is needed because of
  - Codeforces Gym submissions
  - CodeChef Captcha Check
  - LightOj Website is not even browsable without login

## Acknowledgments
* Got the idea from https://github.com/dipta007/codeforce-code-downloader_gym_regular , Does exactly the same thing. Just wanted to implement it on my own.
