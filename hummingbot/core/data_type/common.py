from decimal import Decimal
from enum import Enum
from typing import NamedTuple


class OrderType(Enum):
    """
    订单类型枚举。
    MARKET: 市价订单
    LIMIT: 限价订单
    LIMIT_MAKER: 限价挂单
    """
    MARKET = 1
    LIMIT = 2
    LIMIT_MAKER = 3

    def is_limit_type(self):
        return self in (OrderType.LIMIT, OrderType.LIMIT_MAKER)


class OpenOrder(NamedTuple):
    """
    订单信息。
    client_order_id: 订单ID
    trading_pair: 交易对
    price: 价格
    amount: 数量
    executed_amount: 已成交数量
    status: 订单状态
    order_type: 订单类型
    is_buy: 是否买单
    time: 时间
    exchange_order_id: 交易所订单ID
    """
    client_order_id: str
    trading_pair: str
    price: Decimal
    amount: Decimal
    executed_amount: Decimal
    status: str
    order_type: OrderType
    is_buy: bool
    time: int
    exchange_order_id: str


class PositionAction(Enum):
    """
    持仓操作枚举。
    OPEN: 开仓
    CLOSE: 平仓
    NIL: 无
    """
    OPEN = "OPEN"
    CLOSE = "CLOSE"
    NIL = "NIL"


# For Derivatives Exchanges
class PositionSide(Enum):
    """
    持仓方向枚举。
    LONG: 多头
    SHORT: 空头
    BOTH: 双向
    """
    LONG = "LONG"
    SHORT = "SHORT"
    BOTH = "BOTH"


# For Derivatives Exchanges
class PositionMode(Enum):
    """
    持仓模式枚举。
    HEDGE: 对冲
    ONEWAY: 单向
    """
    HEDGE = "HEDGE"
    ONEWAY = "ONEWAY"


class PriceType(Enum):
    """
    价格类型枚举。
    MidPrice: 中间价格
    BestBid: 最佳买价
    BestAsk: 最佳卖价
    LastTrade: 最后成交价
    LastOwnTrade: 最后自己的成交价
    InventoryCost: 库存成本
    Custom: 自定义
    """
    MidPrice = 1
    BestBid = 2
    BestAsk = 3
    LastTrade = 4
    LastOwnTrade = 5
    InventoryCost = 6
    Custom = 7


class TradeType(Enum):
    """
    交易类型枚举。
    BUY: 买
    SELL: 卖
    RANGE: 区间
    """
    BUY = 1
    SELL = 2
    RANGE = 3


class LPType(Enum):
    """
    流动性提供者类型枚举。
    ADD: 添加
    REMOVE: 移除
    COLLECT: 收集
    """
    ADD = 1
    REMOVE = 2
    COLLECT = 3
