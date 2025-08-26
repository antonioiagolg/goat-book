import unittest
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_TIME = 5

class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def wait_for_row_in_table(self, row_text) -> None:
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                trs = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(
                    row_text,
                    [row.text for row in trs], 
                )
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_TIME:
                    raise
                time.sleep(0.5)

    def test_can_start_todo_list(self) -> None:
        # and it navigates to the To-do list app
        self.browser.get(self.live_server_url)

        # The user can see that it is in the to-do list app by the title
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)


        # The user sees there is a field to add an item
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
    
        # The user adds an item "Do the dishes"
        inputbox.send_keys("Do the dishes")

        # The app reloads and it shows "1: Do the dishes"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_table("1: Do the dishes")

        # The field is still there for more items
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Dry the dishes and put them away")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The app reloads and shows two items in the list
        self.wait_for_row_in_table("2: Dry the dishes and put them away")
        self.wait_for_row_in_table("1: Do the dishes")

