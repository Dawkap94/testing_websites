from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium import webdriver


class SauceDemoTest:
    def __init__(self):
        self.login = "standard_user"
        self.password = "secret_sauce"
        self.service_obj = Service('C://Dev//chromedriver.exe')
        self.driver_options = webdriver.ChromeOptions()
        self.driver_options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=self.service_obj, options=self.driver_options)
        self.driver.get('https://www.saucedemo.com/')
        self.driver.implicitly_wait(3)

    def log_into(self):
        self.driver.find_element(By.ID, "user-name").send_keys(self.login)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "login-button").click()
        assert self.driver.find_element(By.CSS_SELECTOR,
                                        "span[class='title']").text == "PRODUCTS", "Cannot log in to account."
        print("Logging in works fine.")
        return True

    def sort_things_a_z(self):
        select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        select.select_by_value("az")
        product_names = [name.text for name in
                         self.driver.find_elements(By.CSS_SELECTOR, "div[class='inventory_item_name']")]
        product_names_sorted = product_names[::]
        product_names_sorted.sort()
        assert product_names == product_names_sorted
        print("Sorting A-Z works fine.")
        return True

    def sort_things_price_high_to_low(self):
        # self.select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        # self.select.select_by_value("za").click()
        self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']").click()
        self.driver.implicitly_wait(2)
        self.driver.find_element(By.CSS_SELECTOR, "option[value='hilo']").click()
        self.product_prices = [float(price.text.replace("$", "")) for price in
                         self.driver.find_elements(By.CSS_SELECTOR, "div[class='inventory_item_price']")]
        product_prices_sorted = self.product_prices[::]
        product_prices_sorted.sort()
        try:
            assert product_prices_sorted[::-1] == self.product_prices, "Sorting by price (high to low) doesnt work"
            print("Sorting by price works fine.")
            return True
        except AssertionError:
            print("Sorting by price (high to low) doesnt work")
            return False


sauce_obj = SauceDemoTest()
sauce_obj.log_into()
sauce_obj.sort_things_a_z()
sauce_obj.sort_things_price_high_to_low()