from selenium.webdriver.common.by import By

from src.data_object.trade_order import TradeOrder
from src.utils import logger
from src.utils.element_util import WebActions


class UpdateOrder:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger

    __txt_edit_stop_loss = (By.CSS_SELECTOR, "input[data-testid='edit-input-stoploss-price']")
    __txt_edit_take_profit = (By.CSS_SELECTOR, "input[data-testid='edit-input-takeprofit-price']")
    __btn_update_order = (By.CSS_SELECTOR, "button[data-testid='edit-button-order']")

    def update(self, trade_order: TradeOrder):
        self.actions.send_keys_by_action_chains(self.__txt_edit_stop_loss, trade_order.stop_loss)
        self.actions.send_keys_by_action_chains(self.__txt_edit_take_profit, trade_order.take_profit)
        self.actions.click(self.__btn_update_order)
