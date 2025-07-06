from selenium.webdriver.common.by import By

from src.apps.web.component.update_order import UpdateOrder
from src.apps.web.popup.bulk_close_popup import BulkClosePopup
from src.apps.web.popup.confirm_close_order_popup import ConfirmCloseOrderPopup
from src.apps.web.popup.trade_confirmation_popup import TradeConfirmationPopup
from src.data_object.trade_order import TradeOrder
from src.enums.order_enum import AssetOrderType, BulkCloseType
from src.utils import logger
from src.utils.element_util import WebActions
from src.utils.string_util import cook_element


class _AssetColumnProperty:
    OPEN_DATE = "open-date"
    CLOSE_DATE = "close-date"
    ORDER_ID = "order-id"
    STATUS = "status"
    ORDER_TYPE = "order-type"
    PROFIT = "profit"
    SIZE = "volume"
    UNITS = "units"
    ENTRY_PRICE = "entry-price"
    CURRENT_PRICE = "current-price"
    TAKE_PROFIT = "take-profit"
    STOP_LOSS = "stop-loss"
    SWAP = "swap"
    COMMISSION = "commission"
    REMARKS = "remarks"


class AssetOrder:
    def __init__(self, driver=None):
        self._driver = driver
        self.actions = WebActions(self._driver)
        self.logger = logger
        self.confirm_close_order_popup = ConfirmCloseOrderPopup(driver)
        self.bulk_close_popup = BulkClosePopup(driver)
        self.update_order = UpdateOrder(driver)
        self.trade_confirmation_popup = TradeConfirmationPopup(driver)

    __tab_open_position = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-open-positions']")
    __tab_pending_orders = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-pending-orders']")
    __tab_order_history = (By.CSS_SELECTOR, "div[data-testid='tab-asset-order-type-history']")
    __lbl_asset_open_column_dyn = (
        By.CSS_SELECTOR, "td[data-testid='asset-open-column-{0}'], th[data-testid='asset-open-column-{0}']"
    )
    __lbl_asset_history_column_dyn = (
        By.CSS_SELECTOR, "td[data-testid='asset-history-column-{0}'], th[data-testid='asset-history-column-{0}']"
    )
    __xpath_condition_by_order_id = "[./ancestor::th/preceding-sibling::th[@data-testid='asset-open-column-order-id' and text()='{}']]"
    __btn_close_asset_order_by_id = (
        By.XPATH, f"//div[@data-testid='asset-open-button-close']{__xpath_condition_by_order_id}"
    )
    __btn_edit_asset_order_by_id = (
        By.XPATH, f"//div[@data-testid='asset-open-button-edit']{__xpath_condition_by_order_id}"
    )
    __dd_bulk_close = (By.CSS_SELECTOR, "div[data-testid='bulk-close']")
    __dd_bulk_close_item_dyn = (By.CSS_SELECTOR, "div[data-testid='dropdown-bulk-close-{}']")
    __lbl_open_position_empty_message = (
        By.CSS_SELECTOR, "tbody[data-testid='asset-open-list'] div[data-testid='empty-message']"
    )
    __lbl_pending_order_empty_message = (
        By.CSS_SELECTOR, "tbody[data-testid='asset-open-list'] div[data-testid='empty-message']"
    )

    def select_asset_order(self, asset_order_type: AssetOrderType):
        locator = {
            AssetOrderType.PENDING_ORDERS: self.__tab_pending_orders,
            AssetOrderType.ORDER_HISTORY: self.__tab_order_history,
            AssetOrderType.OPEN_POSITIONS: self.__tab_open_position,
        }.get(asset_order_type)  # noqa
        self.actions.click(locator)

    def __get_row_value_based_on_column(self, asset_order_type: AssetOrderType, asset_property):
        root_locator = {
            AssetOrderType.PENDING_ORDERS: "",
            AssetOrderType.ORDER_HISTORY: self.__lbl_asset_history_column_dyn,
            AssetOrderType.OPEN_POSITIONS: self.__lbl_asset_open_column_dyn,
        }.get(asset_order_type)  # noqa
        locator = cook_element(root_locator, asset_property)
        return self.actions.get_list_text(locator)

    def get_open_date_list(self, asset_order_type: AssetOrderType) -> list:
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.OPEN_DATE)

    def get_latest_open_date(self, asset_order_type: AssetOrderType):
        return self.get_open_date_list(asset_order_type)[0]

    def get_close_date_list(self, asset_order_type: AssetOrderType) -> list:
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.CLOSE_DATE)

    def get_latest_close_date(self, asset_order_type: AssetOrderType):
        return self.get_close_date_list(asset_order_type)[0]

    def get_type_list(self, asset_order_type: AssetOrderType) -> list:
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.ORDER_TYPE)

    def get_latest_type(self, asset_order_type: AssetOrderType):
        return self.get_type_list(asset_order_type)[0]

    def get_take_profit_list(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.TAKE_PROFIT)

    def get_latest_take_profit(self, asset_order_type: AssetOrderType):
        return self.get_take_profit_list(asset_order_type)[0]

    def get_units_list(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.UNITS)

    def get_latest_units(self, asset_order_type: AssetOrderType):
        return self.get_units_list(asset_order_type)[0]

    def get_size_list(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.SIZE)

    def get_latest_size(self, asset_order_type: AssetOrderType):
        return self.get_size_list(asset_order_type)[0]

    def get_stop_loss_list(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.STOP_LOSS)

    def get_latest_stop_loss(self, asset_order_type: AssetOrderType):
        return self.get_stop_loss_list(asset_order_type)[0]

    def get_order_id_list(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.ORDER_ID)

    def get_latest_order_id(self, asset_order_type: AssetOrderType):
        return self.get_order_id_list(asset_order_type)[0]

    def get_status_list(self, asset_order_type: AssetOrderType):
        return self.__get_row_value_based_on_column(asset_order_type, _AssetColumnProperty.STATUS)

    def get_latest_status(self, asset_order_type: AssetOrderType):
        return self.get_status_list(asset_order_type)[0]

    def close_asset_order(self, order_id, confirm=True):
        locator = cook_element(self.__btn_close_asset_order_by_id, order_id)
        self.actions.click(locator)
        if confirm:
            self.confirm_close_order_popup.click_close_order()

    def update_asset_order(self, order_id, trade_order: TradeOrder, confirm=True):
        locator = cook_element(self.__btn_edit_asset_order_by_id, order_id)
        self.actions.click(locator)
        self.update_order.update(trade_order)
        if confirm:
            self.trade_confirmation_popup.confirm()

    def bulk_close_order(self, bulk_close_type: BulkCloseType, confirm=True):
        self.actions.click(self.__dd_bulk_close)
        suffix = {
            BulkCloseType.ALL_POSITIONS: "all",
            BulkCloseType.PROFITABLE_POSITIONS: "profit",
            BulkCloseType.LOSING_POSITIONS: "loss",
        }.get(bulk_close_type)  # noqa
        locator = cook_element(self.__dd_bulk_close_item_dyn, suffix)
        self.actions.click(locator)
        if confirm:
            self.bulk_close_popup.click_confirm()

    def get_empty_message(self, asset_order_type: AssetOrderType):
        locator = {
            AssetOrderType.OPEN_POSITIONS: self.__lbl_open_position_empty_message,
            AssetOrderType.PENDING_ORDERS: self.__lbl_pending_order_empty_message,
        }.get(asset_order_type)  # noqa
        return self.actions.get_text(locator)
