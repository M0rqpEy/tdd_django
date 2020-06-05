from selenium import webdriver
import os

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

browser = webdriver.Firefox(executable_path=os.path.join(PROJ_DIR, 'geckodriver'))
browser.get('http://localhost:8000')

assert "Django" in browser.title
