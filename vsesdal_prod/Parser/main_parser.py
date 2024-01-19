from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc

# Общий URL для всех профилей
URL = 'https://vsesdal.com/cabinet/'

# Общий путь к папке где хранятся профили Chrome
# PATH_TO_PROFILES = '/home/jora/snap/chromium/common/chromium/'

# Индивидуальные имена профилей
# profile1 = '1'

# "--user-data-dir='/frfr/'"
# "--profile-directory={profile}".format(profile=profile2)


def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=/home/jora/.config/google-chrome") #Path to your chrome profile
    options.add_argument("--profile-directory=Profile 2") #Path to your chrome profile
    options.add_argument("start-maximized")
    service = webdriver.ChromeService(executable_path='/opt/google/chrome/google-chrome')


    driver = uc.Chrome(headless=True ,service=service,options=options)
    driver.get(URL)
    sleep(5)
    el = driver.find_element(By.TAG_NAME , "body")
    el.screenshot('Profile2.png')
    driver.quit()
    driver.close()
