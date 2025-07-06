from datetime import datetime

from src.enums.order_enum import AssetOrderType
from src.utils import logger
from src.utils.assert_util import verify_equals, verify_contains
from src.utils.string_util import count_decimal_places


def test_partial_close_open_position_order(web, place_market_order, symbol):
    order_id = web.trade_page.asset_order.get_latest_order_id(AssetOrderType.OPEN_POSITIONS)

    time_fmt = "%Y-%m-%d %H:%M:%S"
    server_time = datetime.strptime(web.home_page.get_server_time(), time_fmt).replace(second=0, microsecond=0)

    logger.info(f"Step 1: Close order id: {order_id} at server time: {server_time}")
    web.trade_page.asset_order.close_asset_order(order_id)
    web.trade_page.wait_for_loading_complete()

    asset_tab = AssetOrderType.ORDER_HISTORY
    logger.info(f"Step 2: Select {asset_tab} and focus on latest row")
    web.trade_page.asset_order.select_asset_order(AssetOrderType.ORDER_HISTORY)
    web.trade_page.wait_for_loading_complete()

    actual_close_date = web.trade_page.asset_order.get_latest_close_date(asset_tab)

    verify_equals(
        datetime.strptime(actual_close_date, time_fmt).replace(second=0, microsecond=0), server_time,
        f"Verify 'close date' is match the server time when closing the order in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_order_id(asset_tab), order_id,
        f"Verify 'order id' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_status(asset_tab), "CLOSED",
        f"Verify 'status' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_type(asset_tab), place_market_order.order_side.upper(),
        f"Verify 'order type' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_units(asset_tab), str(place_market_order.get_volume_value()),
        f"Verify 'volume' is correct in {asset_tab} area"
    )
    actual_stop_loss = web.trade_page.asset_order.get_latest_stop_loss(asset_tab)
    decimal_places = count_decimal_places(str(actual_stop_loss))
    verify_equals(
        actual_stop_loss, f"{place_market_order.stop_loss:,.{decimal_places}f}",
        f"Verify 'stop loss' is correct in {asset_tab} area"
    )
    verify_equals(
        web.trade_page.asset_order.get_latest_take_profit(asset_tab),
        f"{place_market_order.take_profit:,.{decimal_places}f}",
        f"Verify 'take profit' is correct in {asset_tab} area"
    )

    logger.info("Step 3: Open notifications")
    web.home_page.top_navigation.open_notification()

    actual_result_noti = web.home_page.notification.get_latest_notification()
    verify_contains(
        actual_result_noti, "Position Closed",
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
        actual_result_noti, ' '.join(f'{k} {v}' for k, v in place_market_order.volume.items()),
        "Verify 'volume' is correct in notification"
    )
    web.trade_page.asset_order.select_asset_order(AssetOrderType.OPEN_POSITIONS)
