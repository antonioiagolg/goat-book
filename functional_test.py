import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def test_can_start_todo_list(self) -> None:
        # and it navigates to the To-do list app
        self.browser.get("http://localhost:8000")

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

        table = self.browser.find_element(By.ID, "id_list_table")
        trs = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any(row.text == "Do the dishes" for row in trs), "New to-do item does not appear in the list")
        # The field is still there for more items

        # The user is satisfied and close the app
        self.fail("Finish the tests")

if __name__ == "__main__":
    unittest.main()
