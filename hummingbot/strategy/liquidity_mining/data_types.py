#!/usr/bin/env python

"""
Liquidity mining data types...
"""

from decimal import Decimal


class PriceSize:
    """
    Order price and order size.
    中文：订单价格和订单数量
    """
    def __init__(self, price: Decimal, size: Decimal):
        self.price: Decimal = price
        self.size: Decimal = size

    def __repr__(self):
        return f"[ p: {self.price} s: {self.size} ]"


class Proposal:
    """
    An order proposal for liquidity mining.
    market is the base quote pair like "ETH-USDT".
    buy is a buy order proposal.
    sell is a sell order proposal.
    中文：一个流动性挖矿的订单提案
    """
    def __init__(self, market: str, buy: PriceSize, sell: PriceSize):
        self.market: str = market
        self.buy: PriceSize = buy
        self.sell: PriceSize = sell

    def __repr__(self):
        return f"{self.market} buy: {self.buy} sell: {self.sell}"

    def base(self):
        return self.market.split("-")[0]

    def quote(self):
        return self.market.split("-")[1]
