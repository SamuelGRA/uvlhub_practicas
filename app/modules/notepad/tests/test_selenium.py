import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestNotepad:

    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def teardown_method(self, method):
        self.driver.quit()

    def login(self):
        driver = self.driver
        wait = self.wait

        driver.get("http://127.0.0.1:5000/")
        driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(1)").click()

        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_input = driver.find_element(By.ID, "password")
        submit_btn = driver.find_element(By.ID, "submit")

        email_input.send_keys("user1@example.com")
        password_input.send_keys("1234")
        submit_btn.click()

    def test_notepad_crud(self):
        driver = self.driver
        wait = self.wait

        self.login()

        # Navegar a la url de create
        driver.get("http://127.0.0.1:5000/notepad/create")

        # Pruebas de create
        title_input = wait.until(EC.presence_of_element_located((By.ID, "title")))
        body_input = driver.find_element(By.ID, "body")
        submit_btn = driver.find_element(By.ID, "submit")

        title_input.send_keys("Esto es una prueba")
        body_input.send_keys("Hola, estoy probando")
        submit_btn.click()

        # Pruebas de editar
        edit_link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Edit")))
        edit_link.click()

        title_input = wait.until(EC.presence_of_element_located((By.ID, "title")))
        body_input = driver.find_element(By.ID, "body")
        submit_btn = driver.find_element(By.ID, "submit")

        title_input.clear()
        title_input.send_keys("Esto es una prueba otra vez")
        body_input.clear()
        body_input.send_keys("Hola, estoy probando de nuevo")
        submit_btn.click()

        # Prueba de borrar
        delete_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button")))
        delete_btn.click()
