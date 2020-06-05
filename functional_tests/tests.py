import time
import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase


PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NewVisitorTest(LiveServerTestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установки"""
        self.browser = webdriver.Firefox(
            executable_path=os.path.join(PROJ_DIR, 'geckodriver')
        )

    def tearDown(self):
        """демонтаж"""
        time.sleep(3)
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        """check row in list table """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retvieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн-приложение со
        # списком неотложных дел. Она решает оценить его
        # домашнюю страницу
        self.browser.get(self.live_server_url)
        # Она видит, что заголовок и шапка страницы говорят о списках
        # неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ей сразу же предлагается ввести элемент списка
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            "Enter a to-do item"
        )

        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби –
        # вязание рыболовных мушек)
        input_box.send_keys('Купить павлиньи перья')

        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table("1: Купить павлиньи перья")

        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Сделать мушку из павлиньих перьев')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обновляется, и теперь показывает оба элемента ее списка
        self.check_for_row_in_list_table("1: Купить павлиньи перья")
        self.check_for_row_in_list_table("2: Сделать мушку из павлиньих перьев")
        self.fail('Закончить тест')
        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        # Она посещает этот URL-адрес – ее список по-прежнему там.