from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        text1 = 'Buy peacock feathers'
        input_box.send_keys(text1)
        input_box.send_keys(Keys.ENTER)

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, r'/lists/.+')

        self.check_for_row_in_list_table('1: ' + text1)

        input_box = self.get_item_input_box()
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        text2 = 'Use peacock feathers to make a fly'
        input_box.send_keys(text2)
        input_box.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: ' + text2)

        self.browser.quit()
        self.browser = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',
                                        desired_capabilities=DesiredCapabilities.CHROME)

        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(text1, page_text)
        self.assertNotIn('make a fly', page_text)

        input_box = self.get_item_input_box()
        text3 = 'Buy milk'
        input_box.send_keys(text3)
        input_box.send_keys(Keys.ENTER)

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, r'/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn(text1, page_text)
        self.assertIn(text3, page_text)
