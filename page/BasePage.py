import allure
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver.Client import WinClient
import custom_method.vpmethod as vm


class BasePage(object):

    def __init__(self):
        self.driver: WebDriver = self.getDriver()

    @classmethod
    def getDriver(cls):
        cls.driver = WinClient.driver
        return cls.driver

    @classmethod
    def getClient(cls):
        return WinClient

    def IsMain(self):
        return self.driver.find_element_by_accessibility_id('setting')

    def IsImportPage(self):
        return self.driver.find_element_by_accessibility_id('importbutton')

    def IsPreviewOpen(self):
        close_button = (
            By.XPATH,
            "//Custom[contains(@AutomationId, '_us')]//Button[contains(@AutomationId, 'BarCloseButton')]")
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(close_button))
            return True
        except:
            return False

    def IsPreviewClose(self):
        detail_button = (By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]")
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(detail_button))
            return True
        except:
            return False

    def IsSetTargetDialogOpen(self):
        t = (By.XPATH,
             "//Custom[contains(@AutomationId, 'SetTargetDialog')]//Button[contains(@AutomationId, 'okbutton')]")
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(t))
            return True
        except:
            return False

    def WaitProgressDialogClosed(self):
        d = (By.XPATH, "//Button[contains(@AutomationId, 'Detailsbutton')]")
        try:
            WebDriverWait(self.driver, 600).until(EC.element_to_be_clickable(d))
            self.screen(self.driver, 'AfterComplete')
            return True
        except:
            return False

    def find(self, by, value):
        try:
            for i in range(5):
                element = self.driver.find_element(by, value)
                # vm.log().debug('FOUND')
                return element
        except:
            vm.log().debug('NOT FOUND')
            return False

    def screen(self, driver, s):
        if s is not None:
            allure.attach(driver.get_screenshot_as_png(), s, allure.attachment_type.PNG)