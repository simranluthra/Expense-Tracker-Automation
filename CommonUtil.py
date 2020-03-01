import datetime

class CommonUtil:
    WAIT_TIMEOUT = 10
    TEST_ACCOUNT = "testsimran5@gmail.com"
    TEST_PASSWORD = "testing@123"

    def sign_in_user(module, url):
        """
        Sign in the user in Expense tracker
        :param module (chrome driver):
        :param url:
        """
        module.driver.get(url)
        window_before = module.driver.window_handles[0]
        CommonUtil.WaitForDefaultTime(module.driver)

        google_auth_element = module.driver.find_element_by_xpath("//span[@class='flex-1 ml-4']")
        google_auth_element.click()
        CommonUtil.WaitForDefaultTime(module.driver)

        module.driver.switch_to.window(module.driver.window_handles[1])
        email_element = module.driver.find_element_by_xpath("//input[@id='identifierId']")
        email_element.send_keys(CommonUtil.TEST_ACCOUNT)
        next_button = module.driver.find_element_by_xpath('//*[@id="identifierNext"]')
        next_button.click()
        CommonUtil.WaitForDefaultTime(module.driver)

        password_element = module.driver.find_element_by_name("password")
        password_element.send_keys(CommonUtil.TEST_PASSWORD)
        next_button = module.driver.find_element_by_xpath('//*[@id="passwordNext"]')
        next_button.click()

        module.driver.switch_to.window(window_before)
        CommonUtil.WaitForDefaultTime(module.driver)

    def WaitForDefaultTime(driver):
        """
        Put a implicit wait of default time(5)
        :param driver (chrome driver)
        """
        driver.implicitly_wait(CommonUtil.WAIT_TIMEOUT)

    def WaitForGivenTime(driver, timeout):
        """
        Put a implicit wait of given time (timeout)
        :param driver (chrome driver)
        :param timeout
        """
        driver.implicitly_wait(timeout)

    def getFormattedDate(self):
        """
        format current date.
        :return: formatted date
        """
        today = datetime.date.today()
        return today.strftime('%d/%m/%Y\t %H:%M')