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
    module.NegativeTestCases.webdriver = WebDriver()
    module.NegativeTestCases.driver = module.NegativeTestCases.webdriver.get_chrome_driver()
    # module.NegativeTestCases.driver.fullscreen_window()
    CommonUtil.sign_in_user(module.NegativeTestCases, URL)

def teardown_module(module):
    """
    Quit the chrome driver
    :param module:
    """
    module.NegativeTestCases.driver.quit()

class NegativeTestCases(unittest.TestCase):

    @pytest.mark.run(order=1)
    def test_addExpense(self):
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

        self.driver.find_element_by_id("grid-amount").send_keys("0")

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
        ui_added_invalid_expense = self.driver.find_elements_by_class_name('text-expense')[0].text
        assert ui_added_invalid_expense == '- $0.00'  #user should not be allowed to add 0 as an expense but user is able to add using expense tracker. hence verifiing the same
        print("test_addExpense: Expense is getting added with amount 0 which should not be allowed")

        CommonUtil.WaitForGivenTime(self.driver, 5)
        CommonUtil.WaitForGivenTime(self.driver, 5)
        CommonUtil.WaitForGivenTime(self.driver, 5)

    @pytest.mark.run(order=2)
    def test_currency(self):
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
        amount_currency_in_expense = self.driver.find_element_by_xpath("//div[@class='pl-3 text-grey-darkest']").text
        assert amount_currency_in_expense != '$'
        print("test_currency_testcase: since we updated the currency to dollar in settings, currency should be in dollar at all places like in the amount field in expense. hence comparing the updated currency and actual currency")


        CommonUtil.WaitForGivenTime(self.driver, 5)
        CommonUtil.WaitForGivenTime(self.driver, 5)
        CommonUtil.WaitForGivenTime(self.driver, 5)

    @pytest.mark.run(order=3)
    def test_name_length(self):
        print("test_add_account is running")
        try:
            if ("/add" in self.driver.current_url):
                self.driver.find_element_by_xpath(
                    "//a[@class='font-thin text-grey hover:text-grey-dark block h-6 w-6 cursor-pointer mr-4 sm:hidden']").click()
        except:
            self.driver.find_element_by_css_selector('a[href="/"]').click()


        self.driver.find_element_by_xpath("//div[@class='container mx-auto flex justify-between items-center']//a[@class='block h-6 w-6 cursor-pointer']").click()
        CommonUtil.WaitForDefaultTime(self.driver)
        username = "UserAccountNameLengthTesting123456789"
        self.driver.find_element_by_id("grid-name").send_keys(username)
        select = Select(self.driver.find_element_by_id("grid-type"))
        select.select_by_visible_text('Savings Account')
        self.driver.find_element_by_xpath("//button[@class='w-1/2 bg-expense text-white p-3']").click()
        CommonUtil.WaitForDefaultTime(self.driver)
        username_text = self.driver.find_element_by_xpath('//span[contains(text(),' + username + ')]').text
        username_length = len(username_text)
        assert username_length != 20        # suppose length of username should not be more than 20, still the user is able to add account with name of length more than 20.hence comparing the actual length with 20
        print("Actual length should not be more than 20, but it is allowing the user to add account name with length more than 20")

    @pytest.mark.run(order=4)
    def test_date(self):
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
        input_elem.send_keys('Health')
        input_elem.send_keys(Keys.RETURN)

        time.sleep(2)

        drop_down_arrow_elements[2].click()
        input_desc_elem = self.driver.find_element_by_id("grid-description")
        input_desc_elem.send_keys('Medicine')
        input_desc_elem.send_keys(Keys.RETURN)

        self.driver.find_element_by_id("grid-on-date").send_keys("06/03/202020, 21:00")
        time.sleep(1)
        self.driver.find_element_by_css_selector(
            'button[class="w-1/2 bg-expense text-white p-3"][type="submit"]').click()

        CommonUtil.WaitForGivenTime(self.driver, 5)
        time.sleep(3)

        ui_fetch_category = self.driver.find_element_by_xpath("//div[contains(text(),'health')]").text
        assert ui_fetch_category == 'health'  # since date is not correct, user should not be able to add the expense. It should throw a validation saying date incorrect. But, here it is allowing the user to add the expense with this date. Hence verifying the same
        print("test_date: User is trying to add date with 6 digit year which should not be allowed")

        CommonUtil.WaitForGivenTime(self.driver, 5)
        CommonUtil.WaitForGivenTime(self.driver, 5)
        CommonUtil.WaitForGivenTime(self.driver, 5)

    @pytest.mark.run(order=5)
    def test_logoutNegative(self):
        CommonUtil.WaitForDefaultTime(self.driver)
        self.driver.find_element_by_css_selector('a[href="/settings"]').click()
        ui_settingsUrl = self.driver.current_url
        CommonUtil.WaitForDefaultTime(self.driver)
        self.driver.find_element_by_css_selector('a[title="Logout"]').click()
        CommonUtil.WaitForDefaultTime(self.driver)
        self.driver.back()
        CommonUtil.WaitForDefaultTime(self.driver)
        ui_currenturl = self.driver.current_url

        assert ui_settingsUrl == ui_currenturl  #it should not go back to previous page on clicking on browser back button. hence comparing the url of the site
        print("test_logoutNegative: User should not be able to go back to previous page on clicking on browser back button but expense tracker is allowing the same which is invalid")