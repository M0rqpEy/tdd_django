from selenium import webdriver
import time
import unittest
import os


PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class NewVisitorTest(unittest.TestCase):
    """тест нового посетителя"""

    def setUp(self):
        """установки"""
        self.browser = webdriver.Firefox(
            executable_path=os.path.join(PROJ_DIR, 'geckodriver')
        )

    def tearDown(self):
        """демонтаж"""
        time.sleep(5)
        self.browser.quit()

    def test_can_start_a_list_and_retvieve_it_later(self):
        """тест: можно начать список и получить его позже"""
        # Эдит слышала про крутое новое онлайн-приложение со
        # списком неотложных дел. Она решает оценить его
        # домашнюю страницу
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)
        self.fail('Закончить тест')

        # Ей сразу же предлагается ввести элемент списка
        # Она набирает в текстовом поле "Купить павлиньи перья" (ее хобби –
        # вязание рыболовных мушек)
        # Когда она нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        # Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
        # Она вводит "Сделать мушку из павлиньих перьев"
        # (Эдит очень методична)
        # Страница снова обновляется, и теперь показывает оба элемента ее списка
        # Эдит интересно, запомнит ли сайт ее список. Далее она видит, что
        # сайт сгенерировал для нее уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        # Она посещает этот URL-адрес – ее список по-прежнему там.


if __name__ == "__main__":
    unittest.main(warnings="ignore")