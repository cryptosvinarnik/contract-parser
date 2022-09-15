from dataclasses import dataclass

import requests


@dataclass
class EVMScan():
    api_key: str
    endpoint: str

    def get_source_code(self, address: str) -> dict:
        return requests.get(
            f"{self.endpoint}/api",
            params={"module": "contract", "action": "getsourcecode",
                    "address": address, "apikey": self.api_key}
        ).json()
