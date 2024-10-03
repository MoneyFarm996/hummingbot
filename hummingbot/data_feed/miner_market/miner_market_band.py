from __future__ import annotations
from typing import Any
import aiohttp
from hummingbot.data_feed.data_feed_base import DataFeedBase


class MinerMarketBandDataFeed(DataFeedBase):
    """
    Fetches Miner Market Band data
    """
    _mmdbdf_logger: str = "miner_market_band_data_feed"
    miner_market: dict[str, dict[str, int]] = {
        "binance": {
            "FIRO-USDT": 59,
            "BIFI-USDT": 304
        }
    }

    def __init__(self):
        super().__init__()
        self._api_url = "https://api.hummingbot.io/bounty/charts/market_band?market_id={market_id}&chart_interval=1"

    async def get_spread(self, connector: str, trading_pair: str) -> None | dict[str, Any]:
        """
        Get the spread of the trading pair
        :param connector:
        :param trading_pair:
        :return:
        """
        # 读取 miner_market 字段，获取对应交易所和交易对的 miner_market_id，忽略key大小写
        miner_market_id = self.miner_market.get(connector.lower(), {}).get(trading_pair.upper())
        # 检查miner_market_id是否有值
        if miner_market_id is None:
            return None
        try:
            async with aiohttp.ClientSession() as client:
                async with client.get(self._api_url.format(market_id=miner_market_id)) as response:
                    response: aiohttp.ClientResponse = response
                    if response.status != 200:
                        raise IOError(f"Error fetching Miner Market Band data. HTTP status is {response.status}.")
                    data = await response.json()
                    if data["status"] != "success":
                        raise IOError(f"Error fetching Miner Market Band data. API returned status {data['status']}.")
                    if len(data["data"]) == 0:
                        raise IOError("Miner Market Band data returned empty.")
                    first_data = data["data"][0]
                    self.logger().info(f"Miner Market Band data: {first_data}")
                    return {
                        "spread_ask": first_data["spread_ask"],
                        "spread_bid": first_data["spread_bid"],
                        "timestamp": first_data["timestamp"]
                    }
        except Exception:
            self.logger().error("Error fetching Miner Market Band data.", exc_info=True)
            return None


# 异步调用 MinerMarketBandDataFeed.get_spread 方法
# if __name__ == "__main__":
#     import asyncio
#
#     mmdbdf = MinerMarketBandDataFeed()
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(mmdbdf.get_spread('binance', "BIFI-USDT"))
#     print(result)
