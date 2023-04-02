import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Safari()

    def test_search_in_python_org(self):
        driver = self.driver
        for i in range(20):
            driver.get("https://ru.wikipedia.org/wiki/Заглавная_страница")
            el = driver.find_element(By.ID, 'n-randompage')
            link = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
            driver.get(link)
            el = driver.find_element(By.ID, 'coll-download-as-rl')
            link = el.find_element(By.TAG_NAME, 'a').get_attribute('href')
            driver.get(link)
            el = driver.find_element(By.TAG_NAME, 'button')
            el.click()
            time.sleep(10)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()