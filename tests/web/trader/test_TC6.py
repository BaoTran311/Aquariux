from src.enums.order_enum import AssetOrderType, BulkCloseType
from src.utils import logger
from src.utils.assert_util import verify_equals


def test_bulk_close_open_position_order(web, place_market_order):
    logger.info(f"Steps: Bulk close all orders at server time: {web.home_page.get_server_time()}")
    web.trade_page.asset_order.bulk_close_order(BulkCloseType.ALL_POSITIONS)
    web.trade_page.wait_for_loading_complete()

    verify_equals(
        web.trade_page.asset_order.get_order_id_list(AssetOrderType.OPEN_POSITIONS), [],
        f"Verify amount of open positions tab is 0 in {AssetOrderType.OPEN_POSITIONS} area"
    )
