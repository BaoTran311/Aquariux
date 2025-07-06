from selenium.webdriver.common.by import By

from src.utils import logger
from src.utils.element_util import WebActions


class BulkClosePopup:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __btn_confirm = (By.CSS_SELECTOR, "button[data-testid='bulk-close-modal-button-submit-all']")

    def click_confirm(self):
        return self.actions.click(self.__btn_confirm)
