import builtins
from functools import partial
from operator import eq, ne, gt, ge, lt, le, contains

from pytest_check import check

from src.data_runtime import DataRuntime
from src.utils import logger, datetime_util

_passed_icon = "✓"
_failed_icon = "❌"


def ___verify___(actual, expected, message="", op_func=lambda a, b: a == b):
    result = op_func(actual, expected)
    icon = _passed_icon if result else _failed_icon

    msg = f"{icon} [Expected: {expected}] - [Actual: {actual}] {message.strip()}" \
        if not result else f"{icon} {message.strip()}"
    logger.info(msg)

    if not result:
        attachments = dict()
        for platform, driver in getattr(builtins, "dict_driver").items():
            attach_name = f"{platform}_{datetime_util.get_current_time(time_format='%d-%Y-%m_%H:%M:%S')}.png"
            attachments[msg] = [attach_name, driver.get_screenshot_as_png()]
        builtins.fail_check_point[DataRuntime.tc_info.name].append(attachments)  # noqa

    with check:
        assert result


verify_equals = partial(___verify___, op_func=eq)
verify_not_equals = partial(___verify___, op_func=ne)
verify_greater_than = partial(___verify___, op_func=gt)
verify_greater_equal = partial(___verify___, op_func=ge)
verify_less_than = partial(___verify___, op_func=lt)
verify_less_equal = partial(___verify___, op_func=le)
verify_contains = partial(___verify___, op_func=contains)
verify_not_contains = partial(___verify___, op_func=lambda a, b: b not in a)
