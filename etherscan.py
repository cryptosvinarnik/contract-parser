from dataclasses import dataclass

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
