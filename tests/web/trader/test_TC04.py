from datetime import datetime

from src.data_object.trade_order import MarketTradeOrder
from src.enums.order_enum import OrderSide, VolumeType, AssetOrderType
from src.utils import logger
from src.utils.assert_util import verify_equals, verify_contains
from src.utils.string_util import format_number_string, count_decimal_places


def test_place_sell_MARKET_order(web, symbol):
    asset_tab = AssetOrderType.OPEN_POSITIONS

    logger.info(f"Step 1: Select {symbol!r}")
    web.trade_page.select_symbol(symbol)
    web.trade_page.place_order.collapse_trade_details()

    logger.info("Step 2: Get live buy price")
    live_sell_price = float(format_number_string(web.trade_page.place_order.get_live_sell_price()))

    logger.info("Step 3: Place buy Market order")
    trade_order = MarketTradeOrder(OrderSide.SELL, {VolumeType.UNITS: 2}, live_sell_price + 5, live_sell_price - 5)
    web.trade_page.place_order.place_an_order(trade_order, False)

    verify_equals(
        web.trade_page.trade_confirmation_popup.get_confirmation_symbol(), symbol,
        f"Verify {symbol!r} is correct in confirmation popup"
    )

    actual_trade_order_info = web.trade_page.trade_confirmation_popup.get_confirmation_order_info()
    decimal_places = count_decimal_places(str(actual_trade_order_info[2]))
    verify_equals(
        actual_trade_order_info[0], trade_order.order_side,
        "Verify 'order type' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[1], str(trade_order.get_volume_value()),
        "Verify 'volume' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[2], f"{trade_order.stop_loss:,.{decimal_places}f}",
        "Verify 'stop loss' is correct in confirmation popup"
    )
    verify_equals(
        actual_trade_order_info[3], f"{trade_order.take_profit:,.{decimal_places}f}",
        "Verify 'take profit' is correct in confirmation popup"
    )

    time_fmt = "%Y-%m-%d %H:%M:%S"
    server_time = datetime.strptime(web.home_page.get_server_time(), time_fmt).replace(microsecond=0)

    logger.info(f"Step 4: Click 'Confirm' at server time: {server_time}")
    web.trade_page.trade_confirmation_popup.confirm()
    web.trade_page.wait_for_loading_complete()

    logger.info("Step 5: Focus on 'Open Position' area")
    order_id = web.trade_page.asset_order.get_latest_order_id(asset_tab)

    actual_open_date = web.trade_page.asset_order.get_latest_open_date(asset_tab)
    verify_equals(
        datetime.strptime(actual_open_date, time_fmt).replace(second=server_time.second, microsecond=0), server_time,
        f"Verify {actual_open_date!r} is match the server time when placing the order"
    )

    verify_equals(
        web.trade_page.asset_order.get_latest_type(asset_tab), trade_order.order_side.upper(),
        f"Verify 'order type' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_units(asset_tab), str(trade_order.get_volume_value()),
        f"Verify 'volume' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_stop_loss(asset_tab), f"{trade_order.stop_loss:,.{decimal_places}f}",
        f"Verify 'stop loss' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_take_profit(asset_tab), f"{trade_order.take_profit:,.{decimal_places}f}",
        f"Verify 'take profit' is correct in {asset_tab} area"
    )

    logger.info("Step 6: Open notifications")
    web.home_page.top_navigation.open_notification()

    actual_result_noti = web.home_page.notification.get_latest_notification()
    verify_contains(
        actual_result_noti, asset_tab[:-1],
        "Verify 'order type' is correct in notification"
    )
    verify_contains(
        actual_result_noti, order_id,
        "Verify 'order id' is correct in notification"
    )
    verify_contains(
        actual_result_noti, symbol,
        "Verify 'symbol' is correct in notification"
    )
    verify_contains(
        actual_result_noti, ' '.join(f'{k} {v}' for k, v in trade_order.volume.items()),
        "Verify 'volume' is correct in notification"
    )
    verify_contains(
        actual_result_noti, str(live_sell_price),
        "Verify 'entry price' is correct in notification"
    )
    web.home_page.top_navigation.close_notification()
