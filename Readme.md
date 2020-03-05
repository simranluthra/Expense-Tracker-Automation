# Expense Tracker Automation

## Description
Automated test cases for Expense tracker website.

## Dependencies
- Selenium
- Google Chrome
- Python 2.7
- Pytest
- pytest-ordering [pip install pytest-ordering]

## Instruction

### Overview
The test cases have been writen with `pytest` framework.
Dummy gmail account with less security has been used for testing
Happy flow is tested for the site 

### Getting started (Automated test cases)
- Replace value of `self.chrome_driver` with your own chrome driver path in `WebDriver.py`
- Open terminal in the project folder.
- Run `pytest ExpenseTrackerTestCases.py` for positive test cases.
- Run `pytest ExpenseTrackerNegativeTestCases.py` for negative test cases.

### Getting Started (manual test cases)
- Open `Expense Tracker.xlsx` file in project folder
- Refer to `Positive Test cases` sheet for happy flow
- Refer to `Negative Test cases` sheet for bugs found.


##### NOTE
To change the dummy account used for testing flow below steps:
- Open CommonUtil.py
- Replace the `TEST_ACCOUNT`,`TEST_PASSWORD` with your credentials resectively.
- Replaced dummy account should be less secured (login access on third party less secured browser)
- Mobile number should not be added for the account.