import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8081")

class EventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1365,900")
        cls.driver = webdriver.Chrome(options=options)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(BASE_URL)
        self.driver.execute_script("localStorage.clear();sessionStorage.clear();")
        self.driver.refresh()
        self.wait.until(EC.presence_of_element_located((By.ID, "home")))

    def go(self, view):
        self.driver.find_element(By.CSS_SELECTOR, f'[data-view="{view}"]').click()

    def wait_message(self, phrase):
        self.wait.until(lambda d: phrase in d.find_element(By.ID, "message").text)

    def create_student(self):
        self.go("register")
        self.driver.find_element(By.ID, "reg-name").send_keys("Test Student")
        self.driver.find_element(By.ID, "reg-email").send_keys("student@example.com")
        self.driver.find_element(By.ID, "reg-password").send_keys("pass123")
        self.driver.find_element(By.CSS_SELECTOR, "#register-form button").click()

    def test_01_registration_page_opens(self):
        self.go("register")
        self.assertTrue(self.driver.find_element(By.ID, "register-form").is_displayed())

    def test_02_valid_student_registration(self):
        self.create_student()
        self.wait_message("Account created successfully")
        self.assertTrue(self.driver.find_element(By.ID, "dashboard").is_displayed())

    def test_03_empty_registration_validation(self):
        self.go("register")
        self.driver.find_element(By.CSS_SELECTOR, "#register-form button").click()
        self.assertTrue(self.driver.find_element(By.ID, "reg-name").get_attribute("validationMessage"))

    def test_04_invalid_email_validation(self):
        self.go("register")
        self.driver.find_element(By.ID, "reg-name").send_keys("Test")
        self.driver.find_element(By.ID, "reg-email").send_keys("bad-email")
        self.driver.find_element(By.ID, "reg-password").send_keys("pass123")
        self.driver.find_element(By.CSS_SELECTOR, "#register-form button").click()
        self.assertTrue(self.driver.find_element(By.ID, "reg-email").get_attribute("validationMessage"))

    def test_05_duplicate_email_is_rejected(self):
        self.create_student()
        self.driver.find_element(By.ID, "logout").click()
        self.go("register")
        self.driver.find_element(By.ID, "reg-name").send_keys("Another Student")
        self.driver.find_element(By.ID, "reg-email").send_keys("student@example.com")
        self.driver.find_element(By.ID, "reg-password").send_keys("pass123")
        self.driver.find_element(By.CSS_SELECTOR, "#register-form button").click()
        self.wait_message("already registered")

    def test_06_valid_login(self):
        self.create_student()
        self.driver.find_element(By.ID, "logout").click()
        self.go("login")
        self.driver.find_element(By.ID, "login-email").send_keys("student@example.com")
        self.driver.find_element(By.ID, "login-password").send_keys("pass123")
        self.driver.find_element(By.CSS_SELECTOR, "#login-form button").click()
        self.wait_message("Login successful")
        self.assertTrue(self.driver.find_element(By.ID, "dashboard").is_displayed())


    def test_07_registered_event_is_visible(self):
        self.create_student()
        self.go("events")

        join_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#event-list .join")
            )
        )
        join_button.click()

        self.wait_message("Registration confirmed")

        # Open dashboard directly using the JavaScript function.
        self.driver.execute_script("go('dashboard')")

        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.ID, "my-registrations"),
                "Tech Innovation Summit"
            )
        )

        self.assertIn(
            "Tech Innovation Summit",
            self.driver.find_element(By.ID, "my-registrations").text
        )



if __name__ == "__main__":
    unittest.main(verbosity=2)
