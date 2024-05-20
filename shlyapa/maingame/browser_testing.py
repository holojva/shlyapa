from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .views import room

class ProgramTest(StaticLiveServerTestCase) :
    @classmethod
    def setUpClass(cls) :
        super().setUpClass()
        cls.selenium=webdriver.Firefox()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls) :
        cls.selenium.quit()
        super().tearDownClass()
    def test_browser(self) :
        self.selenium.get(self.live_server_url)
        self.selenium.find_element(By.CSS_SELECTOR, "#id_password")
    
        