#selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import getpass

#Email sending
import smtplib
import easyimap
import webbrowser
import os

import time
#var
wait = 8
email = input('Email: ')
e_pwd = getpass.getpass("Email Password: ")
userName = input('Mosaic Username: ' )
pwd = getpass.getpass('Password: ')
complete = False
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

#function
def startUp():
    driver.get("https://epprd.mcmaster.ca/psp/prepprd/?cmd=login")
    assert "Mosaic" in driver.title
startUp()
driver.find_element_by_id('userid').send_keys(userName)
driver.find_element_by_id('pwd').send_keys(pwd , Keys.ENTER)

def sendEmail(subject, msg, target):
   try:
      server = smtplib.SMTP('smtp.gmail.com:587')
      server.ehlo()
      server.starttls()
      server.login(email, e_pwd)
      message = 'Subject: {}\n\n{}'.format(subject, msg)
      server.sendmail(email, target, message)
      server.quit()
   except Exception as e:
      print(e)
   print('Email sent')

#wbepage navigation
def navToGrades():
    try:
        element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, "win0groupletPTNUI_LAND_REC_GROUPLET$7")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    driver.find_element_by_id('win0groupletPTNUI_LAND_REC_GROUPLET$7').click()
    navPassRadioButtons()

def navPassRadioButtons():
    try:
        element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, "SSR_DUMMY_RECV1$sels$3$$0")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    driver.switch_to.frame(driver.find_element_by_id("ptifrmtgtframe"))
    driver.find_element_by_xpath('//*[@id="SSR_DUMMY_RECV1$sels$2$$0"]').click()
    driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()
    try:
        element = WebDriverWait(driver, wait).until(EC.presence_of_element_located((By.ID, "CLS_LINK$0")))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

def updateMsg():
    return ('Course: ' +driver.find_element_by_id('CLS_LINK$0').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$0').text + '\n' +
        'Course: ' +driver.find_element_by_id('CLS_LINK$1').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$1').text + '\n' +
        'Course: ' +driver.find_element_by_id('CLS_LINK$2').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$2').text + '\n' +
        'Course: ' +driver.find_element_by_id('CLS_LINK$3').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$3').text + '\n' +
        'Course: ' +driver.find_element_by_id('CLS_LINK$4').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$4').text + '\n' +
        'Course: ' +driver.find_element_by_id('CLS_LINK$5').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$5').text + '\n' +
        'Course: ' +driver.find_element_by_id('CLS_LINK$6').text + '   || Grade: ' + driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$6').text + '\n')

def fileWrite():
    f = open('grades.txt', 'w')
    f.write(updateMsg())
    f.close()

def fileRead():
    f = open('grades.txt', 'r')
    readText = f.read()
    f.close()
    return readText

def checkForUpdates():
    if(fileRead() != updateMsg()):
        f = open('grades.txt', 'w')
        f.write(updateMsg())
        f.close()
        sendEmail('Grades update', updateMsg(), email)
        return True
    else: 
        return False
def checkComplete():
    for i in range(7):
        if(driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$' + str(i)).text == ''):
            return False
    return True

navToGrades()
#driver.execute_script("arguments[0].innerText = ''", driver.find_element_by_id('STDNT_ENRL_SSV1_CRSE_GRADE_OFF$6')) #testScript
checkForUpdates()
fileWrite()

while(complete == False):
    fileRead()
    driver.refresh()
    navPassRadioButtons()
    checkForUpdates()
    time.sleep(1800)
    complete = checkComplete()
    
time.sleep(10)
driver.close()
