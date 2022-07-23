from dataclasses import dataclass

import aiohttp
import requests


@dataclass
class EtherScan():
    api_key: str

    def get_source_code(self, address) -> dict:
        return requests.get(
            "https://api.etherscan.io/api",
            params={"module": "contract", "action": "getsourcecode",
                    "address": address, "apikey": self.api_key}
        ).json()


@dataclass
class AsyncEtherScan():
    api_key: str

    async def get_source_code(self, address) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.etherscan.io/api",
                params={"module": "contract", "action": "getsourcecode",
                        "address": address, "apikey": self.api_key}
            ) as resp:
                return await resp.json()
