import time
from unittest import skip
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options  import Options
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 10
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FunctionalTest(StaticLiveServerTestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установки"""
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(
            executable_path=os.path.join(PROJ_DIR, 'geckodriver'),
            # options=options
        )
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        """демонтаж"""
        time.sleep(1)
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ожидать строку в списке таблицы """
        start_time = time.time()
        while 1:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def wait_for(self, func):
        start_time = time.time()
        while 1:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')