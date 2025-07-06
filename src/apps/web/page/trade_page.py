from selenium.webdriver.common.by import By

from src.apps.web.component.asset_order import AssetOrder
from src.apps.web.component.place_order import PlaceOrder
from src.apps.web.page.home_page import HomePage
from src.apps.web.popup.confirm_close_order_popup import ConfirmCloseOrderPopup
from src.enums.watch_list_enum import WatchList
from src.utils import string_util


class TradePage(HomePage):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.place_order = PlaceOrder(driver)
        self.asset_order = AssetOrder(driver)

    __tgl_one_click_trading = (By.XPATH, "//div[starts-with(@data-testid, 'toggle-oct')]")
    __tab_watchlist_dyn = (By.CSS_SELECTOR, "div[data-testid='tab-{}']")
    __lbl_watchlist_symbol_dyn = (By.XPATH, "//div[@data-testid='watchlist-symbol' and text()='{}']")

    def is_one_click_trading_enable(self):
        return "-checked" in self.actions.get_attribute(self.__tgl_one_click_trading, "data-testid")

    def __set_one_click_trading(self, enable: bool):
        if self.is_one_click_trading_enable() != enable:
            self.actions.click(self.__tgl_one_click_trading)
        self.actions.wait_for_condition(
            lambda: self.is_one_click_trading_enable() == enable,
        )

    def enable_one_click_trading(self):
        self.__set_one_click_trading(True)

    def disable_one_click_trading(self):
        self.__set_one_click_trading(False)

    def select_watchlist(self, watchlist: WatchList):
        watchlist = (
            {"Favorites": "my-watchlist",
             "Top Picks": "popular",
             "Commodities": "comms"}.get(watchlist, watchlist)
            .lower().replace(" ", "-")
        )
        locator = string_util.cook_element(self.__tab_watchlist_dyn, watchlist)
        self.actions.click(locator)

    def select_symbol(self, item):
        locator = string_util.cook_element(self.__lbl_watchlist_symbol_dyn, item)
        self.actions.scroll_to_element(locator)
        self.actions.click(locator)
        self.wait_for_loading_complete()
