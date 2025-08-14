from src.utils import assert_util
from src.utils import logger


def test_login_with_valid_credential(web):
    logger.info("Step 1: Navigate to AQX Trader")
    web.navigate_to_aquariux()

    logger.info("Step 2: Login with valid account")
    web.login_page.login_with_demo_account(wait_completed=True)
    assert_util.verify_equals(
        web.trade_page.top_navigation.is_setting_button_displayed(), True,
        "Verify setting button on Top Navigation displays"
    )
    assert_util.verify_equals(
        web.trade_page.top_navigation.is_switch_theme_button_displayed(), True,
        "Verify switch theme button on Top Navigation displays"
    )
    assert_util.verify_equals(
        web.trade_page.top_navigation.is_notification_button_displayed(), True,
        "Verify notification button on Top Navigation displays"
    )
