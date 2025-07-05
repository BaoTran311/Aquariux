from selenium.webdriver.common.by import By

from src.utils import logger
from src.utils.element_util import WebActions


class TopNavigation:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __btn_setting = (By.CSS_SELECTOR, "div[data-testid='setting-button']")
    __btn_switch_theme = (By.CSS_SELECTOR, "div[data-testid='switch-theme-button']")
    __btn_notification = (By.CSS_SELECTOR, "div[data-testid='notification-selector']")
    __dd_notification_result = (By.CSS_SELECTOR, "div[data-testid='notification-dropdown-result']")

    def wait_for_top_navigation_displays(self):
        self.actions.wait_for_element_visible(self.__btn_setting)

    def is_setting_button_displayed(self):
        return self.actions.is_displayed(self.__btn_setting)

    def is_switch_theme_button_displayed(self):
        return self.actions.is_displayed(self.__btn_switch_theme)

    def is_notification_button_displayed(self):
        return self.actions.is_displayed(self.__btn_notification)

    def __click_notification(self, open=True):
        is_opened = len(self.actions.find_element(self.__btn_notification).find_elements(
            *self.__dd_notification_result)) > 0
        if is_opened != open:
            self.actions.click(self.__btn_notification)

    def open_notification(self):
        self.__click_notification()

    def close_notification(self):
        self.__click_notification(False)
