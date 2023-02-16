import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from datetime import datetime
from decimal import Decimal


# screenshot decorator
def screenshot_on_error(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as exc_name:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            args[0].driver.save_screenshot(f"{func.__name__}Error{now}.png")
            print(f"An error with {func.__name__} occured.")
            raise exc_name

    return wrapper


class SauceDemoTest:
    def __init__(self):
        self.login = "standard_user"  # logins in use: locked_out_user, problem_user and performance_glitch_user
        self.password = "secret_sauce"
        self.service_obj = Service('C://Dev//chromedriver.exe')  # path to your chrome webdriver
        self.driver_options = webdriver.ChromeOptions()
        self.driver_options.add_argument('--headless') # testing works in background
        self.driver = webdriver.Chrome(service=self.service_obj, options=self.driver_options)
        self.driver.get('https://www.saucedemo.com/')
        self.driver.implicitly_wait(3)

    @screenshot_on_error
    def log_into(self):
        self.driver.maximize_window()
        self.driver.find_element(By.ID, "user-name").send_keys(self.login)
        self.driver.find_element(By.ID, "password").send_keys(self.password)
        self.driver.find_element(By.ID, "login-button").click()
        try:
            if self.driver.find_element(By.CSS_SELECTOR, "div[class='error-message-container error']"):
                print("User locked or incorrect password.")
                return False
        except selenium.common.exceptions.NoSuchElementException:
            assert self.driver.find_element(By.CSS_SELECTOR,
                                            "span[class='title']").text == "PRODUCTS", "Cannot log in to account."
            print("Logging in works fine.")
            return True

    @screenshot_on_error
    def items_displayed(self):
        assert self.driver.find_elements(By.CSS_SELECTOR, "div[class='inventory_item']"), "Cannot display items."
        print("Items displayed correctly.")
        return 6 == len(self.driver.find_elements(By.CSS_SELECTOR, "div[class='inventory_item']"))

    @screenshot_on_error
    def sort_things_a_z(self):
        select = Select(self.driver.find_element(By.CSS_SELECTOR, "select[class='product_sort_container']"))
        select.select_by_value("az")
        product_names = [name.text for name in
                         self.driver.find_elements(By.CSS_SELECTOR, "div[class='inventory_item_name']")]
        product_names_sorted = product_names[::]
        product_names_sorted.sort()
        assert product_names == product_names_sorted, "Sorting things a-z return incorrect values."
        print("Sorting A-Z works fine.")
        return True

    @screenshot_on_error
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
        assert product_prices_sorted[::-1] == self.product_prices, "Sorting by price (high to low) doesnt work"
        print("Sorting by price works fine.")
        return True

    @screenshot_on_error
    def add_item_to_cart(self):
        self.driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        self.driver.find_element(By.ID, "shopping_cart_container").click()
        assert "Sauce Labs Bolt T-Shirt" in self.driver.find_element(By.CSS_SELECTOR,
                                                                     "div[class='cart_item_label']").text, "No item " \
                                                                                                           "in cart "
        print("Item correctly added to cart")
        return True

    # only after "add to cart" func
    @screenshot_on_error
    def remove_from_cart(self):
        self.driver.find_element(By.ID, "remove-sauce-labs-bolt-t-shirt").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "div[class='removed_cart_item']"), "Cannot remove item " \
                                                                                            "from cart."
        print("Item removed from cart correctly.")
        # after the test is passed, return to home page
        self.driver.find_element(By.ID, "continue-shopping").click()
        return True

    @screenshot_on_error
    def proceed_to_checkout(self):
        self.driver.find_element(By.ID, "checkout").click()
        assert self.driver.find_element(By.ID, "first-name"), "Cannot proceed checkout"
        self.driver.find_element(By.ID, "first-name").send_keys("Examplefirstname")
        self.driver.find_element(By.ID, "last-name").send_keys("Examplesecondname")
        self.driver.find_element(By.ID, "postal-code").send_keys("30-300")
        self.driver.find_element(By.ID, "continue").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "div[class='summary_info']"), "Cannot proceed order form"
        subtotal = Decimal(
            self.driver.find_element(By.CSS_SELECTOR, "div[class='summary_subtotal_label']").text.split("$")[1])
        tax = Decimal(self.driver.find_element(By.CSS_SELECTOR, "div[class='summary_tax_label']").text.split("$")[1])
        total = Decimal(
            self.driver.find_element(By.CSS_SELECTOR, "div[class='summary_total_label']").text.split("$")[1])
        assert subtotal + tax == total, "Total price is incorrect"
        self.driver.find_element(By.ID, "finish").click()
        assert "THANK YOU FOR YOUR ORDER" in self.driver.find_element(By.ID, "checkout_complete_container").text
        print("Order completed")
        return True

    @staticmethod
    def finish():
        return False


if __name__ == "__main__":
    status = True
    while status:
        sauce_obj = SauceDemoTest()
        sauce_obj.log_into()
        sauce_obj.items_displayed()
        sauce_obj.sort_things_a_z()
        sauce_obj.sort_things_price_high_to_low()
        sauce_obj.add_item_to_cart()
        sauce_obj.remove_from_cart()
        sauce_obj.add_item_to_cart()
        sauce_obj.proceed_to_checkout()
        status = sauce_obj.finish()
