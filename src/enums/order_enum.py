class OrderType:
    MARKET = "Market"
    LIMIT = "Limit"
    STOP = "Stop"


class VolumeType:
    SIZE = "Size"
    UNITS = "Units"


class OrderSide:
    BUY = "Buy"
    SELL = "Sell"


class ExpiryType:
    GOOD_TILL_CANCELED = "Good Till Cancelled"
    GOOD_TILL_DAY = "Good Till Day"


class AssetOrderType:
    OPEN_POSITIONS = "Open Positions"
    PENDING_ORDERS = "Pending Orders"
    ORDER_HISTORY = "Order History"
