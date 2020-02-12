import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os.path
from os import path

login_url='https://qa-sandbox.apps.htec.rs/login'
email_identifier="//*[@id='root']/div/div[2]/div/div/div/div/form/div[1]/input"
pass_identifier="//*[@id='root']/div/div[2]/div/div/div/div/form/div[2]/input"
btn_identifier="/html/body/div/div/div[2]/div/div/div/div/form/button"
sandbox_identifier='//*[@id="root"]/div/nav/div/a/b'
CaseLink_identifier='//*[@id="root"]/div/div[2]/div/div/div[2]/div[2]/div'
CaseList_identifier = "div[class='list-group mt-5']>a"
CaseTitle_identifier='//*[@id="root"]/div/div[2]/div/div/div/form/div[1]/input'
CaseDescription_identifier='//*[@id="root"]/div/div[2]/div/div/div/form/div[2]/textarea'
CaseExpected_identifier='//*[@id="root"]/div/div[2]/div/div/div/form/div[3]/input'
CaseStep1_identifier='//*[@id="stepId"]'
Delete_identifier='//*[@id="root"]/div/div[2]/div/div/div/form/span[2]/button'
Confirm_identifier='//*[@id="root"]/div/div[2]/div/div/div/form/span[2]/div/div[2]/p/span[2]/button'
CaseCreate_identifier='//*[@id="root"]/div/div[2]/div/a[2]'
submit_identifier='//*[@id="root"]/div/div[2]/div/div/div/form/button'
automated_identifier='/html/body/div/div/div[2]/div/div/div/form/div[4]/div/div/label'

class TestCaseInfo:
    
    def __init__(self,l='',t='',d='',e='',s=''):
        self.link=l
        self.title=t
        self.description=d
        self.expected=e
        self.step1=s

    def caseID(self):
        return self.link[-4:]
    
    def describe(self, putin):
        if putin is None:
            self.description=''
        else:
            self.description=putin
            
    def export(self):
        FileName=self.caseID()+'.tst'
        file = open(FileName,"w+")
        file.write(self.link+'"\n')
        file.write(self.title+'"\n')
        file.write(self.description+'"\n')
        file.write(self.expected+'"\n')
        file.write(self.step1+'"\n')
        file.close()

class FirefoxTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(login_url)
        self.browser.find_element_by_xpath(email_identifier).send_keys('irinelko@gmail.com')
        self.browser.find_element_by_xpath(pass_identifier).send_keys('knedlica')
        self.browser.find_element_by_xpath(btn_identifier).submit()
        waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, CaseLink_identifier)))
        
    def deleteTest(self):
        self.browser.find_element_by_xpath(Delete_identifier).click()
        waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, Confirm_identifier)))
        self.browser.find_element_by_xpath(Confirm_identifier).click()

    def test_LoadTests(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        self.browser.find_element_by_xpath(CaseLink_identifier).click()
        for f in files:
            if f.endswith('.tst'):
                waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, CaseCreate_identifier)))
                self.browser.find_element_by_xpath(CaseCreate_identifier).click()
                file = open(f,"r")
                link=file.readline()
                self.browser.find_element_by_xpath(CaseTitle_identifier).send_keys(file.readline())
                self.browser.find_element_by_xpath(CaseDescription_identifier).send_keys(file.readline())
                self.browser.find_element_by_xpath(CaseExpected_identifier).send_keys(file.readline())
                self.browser.find_element_by_xpath(CaseStep1_identifier).send_keys(file.readline())
                if file.readline().rstrip()=='true':
                    self.browser.find_element_by_xpath(automated_identifier).click()
                self.browser.find_element_by_xpath(submit_identifier).click()
                file.close()

    def test_EditTests(self):
        self.browser.find_element_by_xpath(CaseLink_identifier).click()   
        waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, CaseList_identifier)))
        CaseList=self.browser.find_elements_by_css_selector(CaseList_identifier)
        CaseLinks=[]

        for case in CaseList:
            CaseLink=case.get_attribute("href")
            CaseLinks.append(CaseLink)
        for link in CaseLinks:
            self.browser.get(link)
            waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, CaseTitle_identifier)))
            self.browser.find_element_by_xpath(CaseTitle_identifier).send_keys(' edited')
            self.browser.find_element_by_xpath(CaseDescription_identifier).send_keys(' edited')
            self.browser.find_element_by_xpath(CaseExpected_identifier).send_keys(' edited')
            self.browser.find_element_by_xpath(CaseStep1_identifier).send_keys(' edited')
            StepContainer=self.browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/form')
            for TestStep in StepContainer:
                print(TestStep.get_attribute("class"))
            self.browser.find_element_by_xpath(submit_identifier).click()

    def test_DeleteEdited(self):
        self.browser.find_element_by_xpath(CaseLink_identifier).click()   
        waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, CaseList_identifier)))
        CaseList=self.browser.find_elements_by_class_name(CaseList_identifier)
        CaseLinks=[]

        for case in CaseList:
            CaseLink=case.get_attribute("href")
            CaseLinks.append(CaseLink)
        for link in CaseLinks:
            self.browser.get(link)
            waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, CaseTitle_identifier)))
            title=self.browser.find_element_by_xpath(CaseTitle_identifier).get_attribute("value")      
            if title[-6:]=='edited':
                self.deleteTest()

    def tearDown(self):
        self.browser.quit()
"""
    def test_ExportCases(self):

        waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, CaseLink_identifier)))
        self.browser.find_element_by_xpath(CaseLink_identifier).click()   
        waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, CaseList_identifier)))
        CaseList=self.browser.find_elements_by_css_selector(CaseList_identifier)
        CaseLinks=[]

        for case in CaseList:
            CaseLink=case.get_attribute("href")
            CaseLinks.append(CaseLink)
        for link in CaseLinks:
            self.browser.get(link)
            Test=TestCaseInfo()
            waitcondition = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, CaseTitle_identifier)))
            TitleOfCase=self.browser.find_element_by_xpath(CaseTitle_identifier).get_attribute("value")
            DescriptionOfCase=self.browser.find_element_by_xpath(CaseDescription_identifier).text
            ExpectedOfCase=self.browser.find_element_by_xpath(CaseExpected_identifier).get_attribute("value")
            StepOfCase=self.browser.find_element_by_xpath(CaseStep1_identifier).get_attribute("value")
            print(TitleOfCase)
            Test.link=link
            Test.title=TitleOfCase
            Test.describe(DescriptionOfCase)
            Test.expected=ExpectedOfCase
            Test.step1=StepOfCase
            Test.export()
            self.deleteTest()
"""

    
if __name__ == "__main__":
    unittest.main()
