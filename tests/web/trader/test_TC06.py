from src.enums.order_enum import AssetOrderType, BulkCloseType
from src.utils import logger
from src.utils.assert_util import verify_equals


def test_bulk_close_open_position_order(web, place_market_order, symbol):
    logger.info(f"Steps: Bulk close all orders at server time: {web.home_page.get_server_time()}")
    web.trade_page.asset_order.bulk_close_order(BulkCloseType.ALL_POSITIONS)
    web.trade_page.wait_for_loading_complete()

    verify_equals(
        web.trade_page.asset_order.get_empty_message(AssetOrderType.OPEN_POSITIONS).strip(),
        f"No open positions for {symbol}",
        f"Verify empty message displays in {AssetOrderType.OPEN_POSITIONS} area"
    )
