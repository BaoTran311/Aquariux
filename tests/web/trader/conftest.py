import operator
import random

import pytest
from pygments.styles.dracula import yellow

from src.data_object.trade_order import MarketTradeOrder
from src.enums.order_enum import OrderSide, VolumeType
from src.enums.side_bar_enum import SideBar
from src.enums.watch_list_enum import WatchList
from src.utils import webdriver_util, logger
from src.utils.string_util import format_number_string, random_enum_value
from src.web_container import Web


@pytest.fixture(scope="package")
def web():
    driver = webdriver_util.init_webdriver()
    yield Web(driver)
    driver.quit()


@pytest.fixture(scope="package")
def symbol():
    return "DASHUSD.std"


@pytest.fixture(scope="package", autouse=True)
def navigate_n_login(web, symbol):
    logger.info("▶ Precondition:")

    logger.info("\t- Navigate & login to Aquariux")
    web.navigate_to_aquariux()
    web.login_page.login_with_demo_account(wait_completed=True)

    logger.info("\t- Open Trader")
    web.home_page.select_sidebar(SideBar.TRADE)
    web.home_page.wait_for_loading_complete()

    logger.info("\t- Select 'All' watchlist")
    web.trade_page.select_watchlist(WatchList.ALL)
    web.home_page.wait_for_loading_complete()

    logger.info("\t- Select 'Crypto'")
    web.trade_page.select_watchlist(WatchList.CRYPTO)

    logger.info("\t- Disable One-Click Trading")
    web.trade_page.disable_one_click_trading()


@pytest.fixture
def place_market_order(web, symbol):
    # Select symbol
    web.trade_page.select_symbol(symbol)
    web.trade_page.place_order.collapse_trade_details()

    # Init TradeOrder obj
    is_buy = ((order_side := random_enum_value(OrderSide)) == OrderSide.BUY)
    f = web.trade_page.place_order.get_live_buy_price if is_buy else web.trade_page.place_order.get_live_sell_price
    live_price = float(format_number_string(f()))
    stop_loss_ops = operator.sub if is_buy else operator.add
    take_profit_ops = operator.add if is_buy else operator.sub
    trade_order = MarketTradeOrder(
        order_side, {VolumeType.UNITS: random.randint(1, 5)}, stop_loss_ops(live_price, 5),
        take_profit_ops(live_price, 5)
    )

    # Place trade order
    web.trade_page.place_order.place_an_order(trade_order)
    web.trade_page.wait_for_loading_complete()
    return trade_order

# @pytest.fixture(scope="module", autouse=True, name=string_util.random_string())
# def navigate_to_trade_page_after_each_TC(web):
#     yield
#     web.home_page.select_sidebar(SideBar.TRADE)
