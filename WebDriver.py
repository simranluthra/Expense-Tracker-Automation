import os

from selenium import webdriver


class WebDriver:

    def __init__(self):
        """
        initialize the chrome driver path
        """
        self.chrome_driver = '/home/simran/PycharmProjects/SeleniumProjects/drivers/chromedriver.exe'

    def get_chrome_driver(self):
        """
        set up chrome driver
        :return:
        """
        os.environ["webdriver.chrome.driver"] = self.chrome_driver
        driver = webdriver.Chrome(self.chrome_driver)
        return driver

    @staticmethod
    def close_chrome_driver(driver):
        """
        close the chrome driver
        :param driver:
        """
        driver.close()