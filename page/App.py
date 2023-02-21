from page.BasePage import BasePage
from page.MainPage import MainPage


class App(BasePage):
    @classmethod
    def main(cls):
        cls.getClient().launch_app()
        return MainPage()

