from selenium.webdriver.common.by import By

from src.utils import logger
from src.utils.element_util import WebActions


class Notification:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __lbl_notification_result_item_list = (By.CSS_SELECTOR, "div[data-testid='notification-list-result-item']")

    def get_notification_list(self) -> list:
        return self.actions.get_list_text(self.__lbl_notification_result_item_list)

    def get_latest_notification(self):
        return self.get_notification_list()[0]
