from src.enums.order_enum import AssetOrderType
from src.utils import logger
from src.utils.assert_util import verify_equals
from src.utils.string_util import count_decimal_places


def test_update_pending_order(web, place_market_order):
    asset_tab = AssetOrderType.OPEN_POSITIONS
    order_id = web.trade_page.asset_order.get_latest_order_id(asset_tab)
    place_market_order.stop_loss -= 1
    place_market_order.take_profit += 1

    logger.info(f"Step 1: Update pending order")
    web.trade_page.asset_order.update_asset_order(order_id, place_market_order)
    web.trade_page.wait_for_loading_complete()

    logger.info("Step 2: Focus on 'Open Position' area")
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
