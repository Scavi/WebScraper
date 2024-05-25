from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


# TODO get rid of ugly sleep's
class ScrapeUtils:

    @staticmethod
    def find_button_and_click(browser: webdriver, by: str, value: str) -> None:
        try:
            sleep(1)
            button = browser.find_element(by, value)
            button.click()
        except Exception as ex:
            print("Unable to find the element of by '{by}' with the value '{value}".format(
                by=by,
                value=value))
            raise ex

    @staticmethod
    def find_field_and_enter(browser: webdriver, by: str, value: str, key: object) -> None:
        try:
            field = browser.find_element(by, value)
            sleep(1)
            field.send_keys(key)
            sleep(1)
            field.submit()
        except Exception as ex:
            print("Unable to find the element of by '%s' with the value '%s'".format(by, value))
            raise ex

    @staticmethod
    def find_by_xpath_and_click(browser: webdriver, by: str, value: str) -> None:
        try:
            sleep(1)
            field = browser.find_element(
                By.XPATH,
                value)
            field.click()
        except Exception as ex:
            print("Unable to find the element of by '%s' with the value '%s'".format(by, value))
            raise ex

    @staticmethod
    def field_contains_text(browser: webdriver, by: str, value: str, text: str):
        try:
            sleep(1)
            status = browser.find_element(
                by,
                value)
            return text not in status.get_attribute("textContent")
        except Exception as ex:
            print("Unable to find the element of by '%s' with the value '%s'".format(by, value))
            raise ex
