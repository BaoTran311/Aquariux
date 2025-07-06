from datetime import datetime

from src.data_object.trade_order import StopTradeOrder
from src.enums.order_enum import OrderSide, VolumeType, AssetOrderType, ExpiryType
from src.utils import logger
from src.utils.assert_util import verify_equals
from src.utils.string_util import format_number_string, count_decimal_places, random_enum_value


def test_place_sell_STOP_order(web, symbol):
    logger.info(f"Step 1: Select {symbol!r}")
    web.trade_page.select_symbol(symbol)
    web.trade_page.place_order.collapse_trade_details()

    logger.info("Step 2: Get live buy price")
    live_price = float(format_number_string(web.trade_page.place_order.get_live_sell_price()))

    logger.info("Step 3: Place sell Stop order")
    trade_order = StopTradeOrder(
        OrderSide.SELL, {VolumeType.UNITS: 1}, live_price - 2, live_price + 5, live_price - 5,
        random_enum_value(ExpiryType)
    )

    web.trade_page.place_order.place_an_order(trade_order, False)

    verify_equals(
        web.trade_page.trade_confirmation_popup.get_confirmation_symbol(), symbol,
        f"Verify {symbol!r} is correct in confirmation popup"
    )

    actual_trade_order_info = web.trade_page.trade_confirmation_popup.get_confirmation_order_info()
    decimal_places = count_decimal_places(str(actual_trade_order_info[2]))
    verify_equals(
        actual_trade_order_info[0], f"{trade_order.order_side} stop",
        "Verify 'order type' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[1], str(trade_order.get_volume_value()),
        "Verify 'volume' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[2], f"{trade_order.price:,.{decimal_places}f}",
        "Verify 'Stop price' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[3], f"{trade_order.stop_loss:,.{decimal_places}f}",
        "Verify 'stop loss' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[4], f"{trade_order.take_profit:,.{decimal_places}f}",
        "Verify 'take profit' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[5], trade_order.expiry,
        "Verify 'expiry' is correct in confirmation popup"
    )

    time_fmt = "%Y-%m-%d %H:%M:%S"
    server_time = datetime.strptime(web.home_page.get_server_time(), time_fmt).replace(microsecond=0)

    logger.info(f"Step 4: Click 'Confirm' at server time: {server_time}")
    web.trade_page.trade_confirmation_popup.confirm()
    web.trade_page.wait_for_loading_complete()

    asset_tab = AssetOrderType.PENDING_ORDERS
    logger.info(f"Step 2: Select {asset_tab} and focus on latest row")
    web.trade_page.asset_order.select_asset_order(asset_tab)
    web.trade_page.wait_for_loading_complete()

    actual_open_date = web.trade_page.asset_order.get_latest_open_date(asset_tab)
    verify_equals(
        datetime.strptime(actual_open_date, time_fmt).replace(second=server_time.second, microsecond=0), server_time,
        f"Verify {actual_open_date!r} is match the server time when placing the order"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_type(asset_tab), f"{trade_order.order_side} stop".upper(),
        f"Verify 'order type' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_units(asset_tab), str(trade_order.get_volume_value()),
        f"Verify 'volume' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_expiry(asset_tab), trade_order.expiry,
        f"Verify 'expiry' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_price(asset_tab), f"{trade_order.price:,.{decimal_places}f}",
        f"Verify 'stop price' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_stop_loss(asset_tab), f"{trade_order.stop_loss:,.{decimal_places}f}",
        f"Verify 'stop loss' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_take_profit(asset_tab), f"{trade_order.take_profit:,.{decimal_places}f}",
        f"Verify 'take profit' is correct in {asset_tab} area"
    )
