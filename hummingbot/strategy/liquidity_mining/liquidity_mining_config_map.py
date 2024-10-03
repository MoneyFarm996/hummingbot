"""
The configuration parameters for a user made liquidity_mining strategy.
"""

import re
from decimal import Decimal
from typing import Optional

from hummingbot.client.config.config_validators import validate_bool, validate_decimal, validate_exchange, validate_int
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.client.config.i18n import gettext as _
from hummingbot.client.settings import required_exchanges


def exchange_on_validated(value: str) -> None:
    required_exchanges.add(value)


def market_validate(value: str) -> Optional[str]:
    pairs = list()
    if len(value.strip()) == 0:
        # Whitespace
        return _("Invalid market(s). The given entry is empty.")
    markets = list(value.upper().split(","))
    for market in markets:
        if len(market.strip()) == 0:
            return _("Invalid markets. The given entry contains an empty market.")
        tokens = market.strip().split("-")
        if len(tokens) != 2:
            return _("Invalid market. {market} doesn't contain exactly 2 tickers.").format(market=market)
        for token in tokens:
            # Check allowed ticker lengths
            if len(token.strip()) == 0:
                return _("Invalid market. Ticker {token} has an invalid length.").format(token=token)
            if (bool(re.search('^[a-zA-Z0-9]*$', token)) is False):
                return _("Invalid market. Ticker {token} contains invalid characters.").format(token=token)
        # The pair is valid
        pair = f"{tokens[0]}-{tokens[1]}"
        if pair in pairs:
            return f"Duplicate market {pair}."
        pairs.append(pair)


def token_validate(value: str) -> Optional[str]:
    value = value.upper()
    markets = list(liquidity_mining_config_map["markets"].value.split(","))
    tokens = set()
    for market in markets:
        # Tokens in markets already validated in market_validate()
        for token in market.strip().upper().split("-"):
            tokens.add(token.strip())
    if value not in tokens:
        return f"Invalid token. {value} is not one of {','.join(sorted(tokens))}"


def order_size_prompt() -> str:
    token = liquidity_mining_config_map["token"].value
    return _("What is the size of each order (in {token} amount)? >>> ").format(token=token)
    # return _("每个订单的大小是多少（以 {token} 金额计）？ >>> ").format(token=token)


liquidity_mining_config_map = {
    "strategy": ConfigVar(
        key="strategy",
        prompt="",
        default="liquidity_mining"),
    "exchange":
        ConfigVar(key="exchange",
                  prompt=_("Enter the spot connector to use for liquidity mining >>> "),
                  # prompt=_("输入现货连接器用于流动性挖矿>>> "),
                  validator=validate_exchange,
                  on_validated=exchange_on_validated,
                  prompt_on_new=True),
    "markets":
        ConfigVar(key="markets",
                  prompt=_("Enter a list of markets (comma separated, e.g. LTC-USDT,ETH-USDT) >>> "),
                  # prompt=_("输入市场列表（逗号分隔，例如 LTC-USDT、ETH-USDT）>>> "),
                  type_str="str",
                  validator=market_validate,
                  prompt_on_new=True),
    "token":
        ConfigVar(key="token",
                  prompt=_("What asset (base or quote) do you want to use to provide liquidity? >>> "),
                  # prompt=_("您想使用什么资产（基础或报价）来提供流动性？ >>> "),
                  type_str="str",
                  validator=token_validate,
                  prompt_on_new=True),
    "order_amount":
        ConfigVar(key="order_amount",
                  prompt=order_size_prompt,
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, inclusive=False),
                  prompt_on_new=True),
    "spread":
        ConfigVar(key="spread",
                  prompt=_("How far away from the mid price do you want to place bid and ask orders? "
                           "(Enter 1 to indicate 1%) >>> "),
                  # prompt=_("您想要下买价和卖价订单时离中间价有多远？ "
                  #          "(Enter 1 to indicate 1%) >>> "),
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, 100, inclusive=False),
                  prompt_on_new=True),

    # enable dynamic spread
    "dynamic_spread":
        ConfigVar(key="dynamic_spread",
                  prompt=_("Would you like to enable dynamic spread? (Yes/No) >>> "),
                  # prompt=_("您想启用动态价差吗？ （是/否）>>>"),
                  type_str="bool",
                  default=False,
                  validator=validate_bool),

    "inventory_skew_enabled":
        ConfigVar(key="inventory_skew_enabled",
                  prompt=_("Would you like to enable inventory skew? (Yes/No) >>> "),
                  # prompt=_("您想启用库存偏差吗？ （是/否）>>>"),
                  type_str="bool",
                  default=True,
                  validator=validate_bool),
    "target_base_pct":
        ConfigVar(key="target_base_pct",
                  prompt=_("For each pair, what is your target base asset percentage? (Enter 20 to indicate 20%) >>> "),
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, 0, 100, inclusive=False),
                  prompt_on_new=True),
    "order_refresh_time":
        ConfigVar(key="order_refresh_time",
                  prompt=_("How often do you want to cancel and replace bids and asks "
                           "(in seconds)? >>> "),
                  type_str="float",
                  validator=lambda v: validate_decimal(v, 0, inclusive=False),
                  default=10.),
    "order_refresh_tolerance_pct":
        ConfigVar(key="order_refresh_tolerance_pct",
                  prompt=_("Enter the percent change in price needed to refresh orders at each cycle "
                           "(Enter 1 to indicate 1%) >>> "),
                  type_str="decimal",
                  default=Decimal("0.2"),
                  validator=lambda v: validate_decimal(v, -10, 10, inclusive=True)),
    "inventory_range_multiplier":
        ConfigVar(key="inventory_range_multiplier",
                  prompt=_("What is your tolerable range of inventory around the target, "
                           "expressed in multiples of your total order size? "),
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=Decimal("1")),
    "volatility_interval":
        ConfigVar(key="volatility_interval",
                  prompt=_(
                      "What is an interval, in second, in which to pick historical mid price data from to calculate "
                      "market volatility? >>> "),
                  type_str="int",
                  validator=lambda v: validate_int(v, min_value=1, inclusive=False),
                  default=60 * 5),
    "avg_volatility_period":
        ConfigVar(key="avg_volatility_period",
                  prompt=_("How many interval does it take to calculate average market volatility? >>> "),
                  type_str="int",
                  validator=lambda v: validate_int(v, min_value=1, inclusive=False),
                  default=10),
    "volatility_to_spread_multiplier":
        ConfigVar(key="volatility_to_spread_multiplier",
                  prompt=_("Enter a multiplier used to convert average volatility to spread "
                           "(enter 1 for 1 to 1 conversion) >>> "),
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=Decimal("1")),
    "max_spread":
        ConfigVar(key="max_spread",
                  prompt=_("What is the maximum spread? (Enter 1 to indicate 1% or -1 to ignore this setting) >>> "),
                  type_str="decimal",
                  validator=lambda v: validate_decimal(v),
                  default=Decimal("-1")),
    "max_order_age":
        ConfigVar(key="max_order_age",
                  prompt=_("What is the maximum life time of your orders (in seconds)? >>> "),
                  type_str="float",
                  validator=lambda v: validate_decimal(v, min_value=0, inclusive=False),
                  default=60. * 60.),
}
