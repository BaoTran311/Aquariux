from selenium.webdriver.common.by import By

from src.utils import logger
from src.utils.element_util import WebActions


class ConfirmCloseOrderPopup:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __btn_close_order = (By.CSS_SELECTOR, "button[data-testid='close-order-button-submit']")
    __txt_close_order_volume = (By.CSS_SELECTOR, "input[data-testid='close-order-input-volume']")

    def click_close_order(self):
        return self.actions.click(self.__btn_close_order)
