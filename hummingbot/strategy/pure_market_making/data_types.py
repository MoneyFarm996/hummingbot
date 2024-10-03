from decimal import Decimal
from typing import (
    List,
    NamedTuple,
)

from hummingbot.core.data_type.common import OrderType

ORDER_PROPOSAL_ACTION_CREATE_ORDERS = 1
ORDER_PROPOSAL_ACTION_CANCEL_ORDERS = 1 << 1


class OrdersProposal(NamedTuple):
    """
    OrdersProposal 是一种数据类型，表示创建或取消订单的建议。
    """
    actions: int
    buy_order_type: OrderType
    buy_order_prices: List[Decimal]
    buy_order_sizes: List[Decimal]
    sell_order_type: OrderType
    sell_order_prices: List[Decimal]
    sell_order_sizes: List[Decimal]
    cancel_order_ids: List[str]


class PricingProposal(NamedTuple):
    """
    PricingProposal 是一种数据类型，表示买卖订单的价格建议。
    """
    buy_order_prices: List[Decimal]
    sell_order_prices: List[Decimal]


class SizingProposal(NamedTuple):
    """
    SizingProposal 是一种数据类型，表示买卖订单的大小建议。
    """
    buy_order_sizes: List[Decimal]
    sell_order_sizes: List[Decimal]


class InventorySkewBidAskRatios(NamedTuple):
    """
    InventorySkewBidAskRatios 是一种数据类型，表示买卖订单的库存偏差比率。
    """
    bid_ratio: float
    ask_ratio: float


class PriceSize:
    """
    PriceSize 是一种数据类型，表示价格和大小。
    """
    def __init__(self, price: Decimal, size: Decimal):
        self.price: Decimal = price
        self.size: Decimal = size

    def __repr__(self):
        return f"[ p: {self.price} s: {self.size} ]"


class Proposal:
    """
    Proposal 是一种数据类型，表示买卖订单的建议。
    """
    def __init__(self, buys: List[PriceSize], sells: List[PriceSize]):
        self.buys: List[PriceSize] = buys
        self.sells: List[PriceSize] = sells

    def __repr__(self):
        return f"{len(self.buys)} buys: {', '.join([str(o) for o in self.buys])} " \
               f"{len(self.sells)} sells: {', '.join([str(o) for o in self.sells])}"
