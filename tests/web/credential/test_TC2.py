import random

from src.data_runtime import DataRuntime
from src.utils import assert_util
from src.utils import logger


def test_login_with_invalid_credential(web):
    invalid_field = random.choice(["username", "password"])

    logger.info("Step 1: Navigate to AQX Trader")
    web.navigate_to_aquariux()

    logger.info(f"Step 2: Login with invalid {invalid_field}")
    credential = [DataRuntime.config.user, DataRuntime.config.password]
    credential[0 if invalid_field == "username" else 1] = f"invalid {invalid_field}"
    web.login_page.login_with_demo_account(*credential)

    expected_msg = "Invalid credentials, please try again"
    assert_util.verify_equals(
        web.login_page.get_alert_error_content(), expected_msg,
        f"Verify error text displays"
    )
