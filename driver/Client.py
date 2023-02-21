from appium import webdriver
from appium.webdriver.webdriver import WebDriver
import yaml
import custom_method.vpmethod as vm


class WinClient(object):
    driver: WebDriver

    @classmethod
    def launch_app(cls) -> WebDriver:
        desired_caps = {}
        # desired_caps["app"] = vm.read_yml('build')
        desired_caps["app"] = vm.yml_data['build']
        # desired_caps['platformName'] = 'Windows'
        # desired_caps['deviceName'] = 'windowsPC'
        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps)
        cls.driver.implicitly_wait(10)
        return cls.driver