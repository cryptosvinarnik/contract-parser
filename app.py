import asyncio
import csv

from etherscan import EtherScan, AsyncEtherScan

from utils import sync_save_contract, worker


if __name__ == "__main__":
    API_KEY = ""  # <--- input your API_KEY from etherscan.io

    match input("Choise parsing type(1 - sync, 2 - async (!WARNING!): "):
        case "1":
            address = input("Input address of a verified smart contract: ")

            try:
                sync_save_contract(EtherScan(API_KEY), address)
            except KeyboardInterrupt:
                pass
        case "2":
            with open("export-verified-contractaddress-opensource-license.csv") as file:
                reader = csv.reader(file)
                data = [row for row in reader]

            contracts = [contract for _, contract, _ in data[2:]]

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(worker(AsyncEtherScan(API_KEY), contracts))
            except KeyboardInterrupt:
                pass
        case _:
            exit()
