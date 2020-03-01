import time
import unittest

import pytest
from selenium.webdriver.support.ui import Select
from Assignment.WebDriver import WebDriver
from Assignment.CommonUtil import CommonUtil
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def setup_module(module):
    """
    Set up the chrome driver and login the user before running all test cases
    :param module:
    """
    URL = 'https://expense-tracker-demo-1.firebaseapp.com'
    module.TestWebsite.webdriver = WebDriver()
    module.TestWebsite.driver = module.TestWebsite.webdriver.get_chrome_driver()
    module.TestWebsite.driver.fullscreen_window()
    CommonUtil.sign_in_user(module.TestWebsite, URL)

def teardown_module(module):
    """
    Quit the chrome driver
    :param module:
    """
    module.TestWebsite.driver.quit()


class TestWebsite(unittest.TestCase):

    @pytest.mark.run(order=1)
    def test_login(self):
        """
        Verify if the user got logged in
        """
        print("test_login is running")
        self.driver.find_element_by_css_selector('a[href="/settings"]').click()
        ui_username = self.driver.find_element_by_xpath('/html/body/div/main/div/section/div/div/span[1]').text
        assert ui_username == 'Simran Test'

    @pytest.mark.run(order=2)
    def test_add_account(self):
        """
        Verify if the user is able to add account
        """
        print("test_add_account is running")
        try:
            if("/settings" in self.driver.current_url):
                self.driver.find_element_by_xpath("//a[@class='font-thin text-grey hover:text-grey-dark block h-6 w-6 cursor-pointer mr-4 sm:hidden']").click()
        except:
            self.driver.find_element_by_css_selector('a[href="/"]').click()

        self.driver.find_element_by_xpath("//div[@class='container mx-auto flex justify-between items-center']//a[@class='block h-6 w-6 cursor-pointer']").click()
        CommonUtil.WaitForDefaultTime(self.driver)
        username = "UserAccount"
        self.driver.find_element_by_id("grid-name").send_keys(username)
        select = Select(self.driver.find_element_by_id("grid-type"))
        select.select_by_visible_text('Savings Account')
        self.driver.find_element_by_xpath("//button[@class='w-1/2 bg-expense text-white p-3']").click()
        CommonUtil.WaitForDefaultTime(self.driver)
        ui_accountname = self.driver.find_element_by_xpath('//span[contains(text(),' + username + ')]').text
        assert ui_accountname == 'UserAccount'

    @pytest.mark.run(order=3)
    def test_update_settings(self):
        """
        Verify if the user is able to update settings
        """
        print("test_update_settings is running")
        CommonUtil.WaitForDefaultTime(self.driver)
        self.driver.find_element_by_css_selector('a[href="/settings"]').click()
        select_language = Select(self.driver.find_element_by_id("grid-language"))
        select_language.select_by_visible_text('English')
        select_currency = Select(self.driver.find_element_by_xpath("//div[2]//div[1]//select[1]"))
        select_currency.select_by_visible_text('USD - US Dollar')
        select_default_account = Select(self.driver.find_element_by_xpath("//div[3]//div[1]//select[1]"))
        select_default_account.select_by_visible_text('UserAccount')
        save_settings = self.driver.find_element_by_xpath("//button[@class='w-1/2 bg-expense text-white p-3']")
        save_settings.click()
        ui_settings_language = self.driver.find_element_by_xpath("//h2[@class='text-3xl font-hairline flex-1 flex items-center p-4']").text
        assert ui_settings_language == 'Settings' # because english is selected hence comparing the settings in english

    @pytest.mark.run(order=4)
    def test_add_entry_expense(self):
        """
        Verify if the user is able to add entry in expense
        """
        print("test_add_entry_expense is running")
        toggle_button_element = EC.presence_of_element_located((By.CLASS_NAME, 'circle_nav__toggle'))
        WebDriverWait(self.driver, 20).until(toggle_button_element)
        toggle_button_element = self.driver.find_element_by_class_name('circle_nav__toggle')
        toggle_button_element.send_keys(Keys.RETURN)
        CommonUtil.WaitForDefaultTime(self.driver)

        toggle_add_button = EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/add"]'))
        WebDriverWait(self.driver, 20).until(toggle_add_button)
        toggle_add_button = self.driver.find_element_by_css_selector('a[href="/add"]')
        toggle_add_button.send_keys(Keys.RETURN)
        CommonUtil.WaitForDefaultTime(self.driver)

        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@class='w-1/2 p-4 bg-expense text-grey-lightest']").click()
        time.sleep(1)
        drop_down_arrow_elements = self.driver.find_elements_by_class_name('multiselect__select')
        user_acc_drop_down_element = drop_down_arrow_elements[0]
        user_acc_drop_down_element.click()
        acc_ul_elements = self.driver.find_elements_by_css_selector('ul[class="multiselect__content"]')[0]
        li_elements = acc_ul_elements.find_elements_by_tag_name('span')
        for element in li_elements:
            if 'user' in element.text.lower():
                element.click()
                break

        self.driver.find_element_by_id("grid-amount").send_keys("20")

        drop_down_arrow_elements[1].click()
        input_elem = self.driver.find_element_by_id('grid-category')
        input_elem.send_keys('Education')
        input_elem.send_keys(Keys.RETURN)

        time.sleep(2)

        drop_down_arrow_elements[2].click()
        input_desc_elem = self.driver.find_element_by_id("grid-description")
        input_desc_elem.send_keys('Books')
        input_desc_elem.send_keys(Keys.RETURN)

        self.driver.find_element_by_id("grid-on-date").send_keys(CommonUtil.getFormattedDate(CommonUtil))
        time.sleep(1)
        self.driver.find_element_by_css_selector(
            'button[class="w-1/2 bg-expense text-white p-3"][type="submit"]').click()

        CommonUtil.WaitForGivenTime(self.driver, 5)
        time.sleep(3)
        ui_added_expense = self.driver.find_elements_by_class_name('text-expense')[0].text
        assert ui_added_expense == '- $20.00'

    @pytest.mark.run(order=5)
    def test_add_income(self):
        """
        Verify if the user is able to add entry in income
        """
        print("test_add_income is running")
        toggle_button_income_element = EC.presence_of_element_located((By.CLASS_NAME, 'circle_nav__toggle'))
        WebDriverWait(self.driver, 20).until(toggle_button_income_element)
        toggle_button_income_element = self.driver.find_element_by_class_name('circle_nav__toggle')
        toggle_button_income_element.send_keys(Keys.RETURN)
        CommonUtil.WaitForDefaultTime(self.driver)

        toggle_add_income_button = EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/add"]'))
        WebDriverWait(self.driver, 20).until(toggle_add_income_button)
        toggle_add_income_button = self.driver.find_element_by_css_selector('a[href="/add"]')
        toggle_add_income_button.send_keys(Keys.RETURN)

        time.sleep(3)

        self.driver.find_element_by_css_selector('button[class="w-1/2 p-4 bg-grey-light text-grey-dark"]').click()
        CommonUtil.WaitForDefaultTime(self.driver)

        drop_down_arrow_elements = self.driver.find_elements_by_class_name('multiselect__select')
        user_acc_drop_down_element = drop_down_arrow_elements[0]
        user_acc_drop_down_element.click()
        acc_ul_elements = self.driver.find_elements_by_css_selector('ul[class="multiselect__content"]')[0]
        li_elements = acc_ul_elements.find_elements_by_tag_name('span')
        for element in li_elements:
            if 'user' in element.text.lower():
                element.click()
                break

        self.driver.find_element_by_id("grid-amount").send_keys("50")

        drop_down_arrow_elements[1].click()
        input_elem = self.driver.find_element_by_id('grid-category')
        input_elem.send_keys('Salary')
        input_elem.send_keys(Keys.RETURN)

        time.sleep(1)

        drop_down_arrow_elements[2].click()
        input_desc_elem = self.driver.find_element_by_id("grid-description")
        input_desc_elem.send_keys('JOB')
        input_desc_elem.send_keys(Keys.RETURN)

        self.driver.find_element_by_id("grid-on-date").send_keys(CommonUtil.getFormattedDate(CommonUtil))


        time.sleep(1)
        self.driver.find_element_by_css_selector('button[class="w-1/2 bg-expense text-white p-3"][type="submit"]').click()

        CommonUtil.WaitForGivenTime(self.driver, 5)
        time.sleep(3)
        ui_added_income = self.driver.find_elements_by_class_name('text-income')[0].text
        assert ui_added_income == '$50.00'
        CommonUtil.WaitForDefaultTime(self.driver)
        CommonUtil.WaitForDefaultTime(self.driver)
        CommonUtil.WaitForDefaultTime(self.driver)

    @pytest.mark.run(order=6)
    def test_logout(self):
        """
        Verify if the user is able to logout
        """
        print("test_logout is running")
        CommonUtil.WaitForDefaultTime(self.driver)
        self.driver.find_element_by_css_selector('a[href="/settings"]').click()
        self.driver.find_element_by_css_selector('a[title="Logout"]').click()
        ui_logout_verify = self.driver.find_element_by_xpath("//span[@class='flex-1 ml-4']").text
        assert ui_logout_verify == 'Sign in with Google'