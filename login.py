from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import unittest
import time


# create a class of login that takes in email and password
class Login:
    def __init__(self, f_name, l_name, phone, email, password):
        self.f_name = f_name
        self.l_name = l_name
        self.phone = phone
        self.email = email
        self.password = password


# create a new class that inherits from unittest.TestCase
class TestLogin(unittest.TestCase):

    # define setup method to run before each test
    def setUp(self):
        print("Setting up tests.")
        self.driver = Chrome()
        self.driver.get("http://opencart.abstracta.us/")

        # define field ids
        self.first_name_id = "input-firstname"
        self.last_name_id = "input-lastname"
        self.email_id = "input-email"
        self.phone_id = "input-telephone"
        self.password_id = "input-password"
        self.confirm_password_id = "input-confirm"
        # initialize Login class
        self.user1 = Login("Bob", "Doe", "123-456-7890", "testuser@gmail.com", "123456")

    # define teardown method to run after each test
    def tearDown(self):
        print("Ending tests.")
        self.driver.quit()

    # method reduces amount of code by taking in field_id and returning the shortened version
    def find_element_id(self, field_id):
        return self.driver.find_element(By.ID, field_id)

    # method reduces amount of code by taking in field_class and returning the shortened version
    def find_element_class(self, field_class):
        return self.driver.find_element(By.CLASS_NAME, field_class)

    def newsletter_radio_button(self, choice):
        if choice is True:
            self.driver.find_element(By.CSS_SELECTOR, "input[value='1'][name='newsletter']").click()
        elif choice is False:
            self.driver.find_element(By.CSS_SELECTOR, "input[value='0'][name='newsletter']").click()

    def privacy_policy(self, choice):
        if choice is True:
            checkbox = self.driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            checkbox.click()

    def test_register(self):
        # store element for dropdown containing element with title My Account with a wait time of 10
        wait = WebDriverWait(self.driver, 5)
        print("Searching for dropdown with title My Account.")
        account = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown-toggle[title='My Account']")))
        print("My account found. Selecting My Account.")
        account.click()
        print("Searching for Register button within dropdown.")
        register = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,
                                                          ".dropdown-menu-right li a[href*='route=account/register']")))
        print("Registration button found. Selecting it.")
        register.click()
        time.sleep(2)

        # initialize Login class with test user information
        user1 = Login("Bob", "Doe", "123-456-7890", "testuser@gmail.com", "123456")

        # store id for each field in a list to iterate through
        field_ids = [self.first_name_id, self.last_name_id, self.email_id, self.phone_id, self.password_id,
                     self.confirm_password_id]

        print("Storing user information into input_value list.")
        # store the user information in input_value list
        input_values = [user1.f_name, user1.l_name, user1.email, user1.phone, user1.password, user1.password]

        # iterate through each element in the fields list
        for i, field_id in enumerate(field_ids):
            print("Searching for field: " + field_id)
            # Find element by id and check if it exists on the page
            field = self.driver.find_elements(By.ID, field_id)
            time.sleep(2)
            if not field:
                raise AssertionError(f"Could not find element with id {field_id} on the page.")
            else:
                # Check for duplicates
                field = field[0]
                WebDriverWait(self.driver, 10).until(ec.visibility_of(field))
                field.send_keys(input_values[i])
                # Print statement that tells us which value is being inputted
                print("Inputting value into: " + field_id + " - " + input_values[i])

        # select Yes for the newsletter subscription
        self.newsletter_radio_button(True)

        # check the privacy policy checkbox
        self.privacy_policy(True)

        # submit the form
        submit = self.driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary[type='submit'][value='Continue']")
        submit.click()
        time.sleep(5)


# run unittest
if __name__ == '__main__':
    unittest.main()
