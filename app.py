from scan_api import EVMScan

from utils import save_contract

endpoints = {"1": "https://api.etherscan.io", "2": "https://api.bscscan.com", "3": "https://api.polygonscan.com"}


if __name__ == "__main__":
    API_KEY = ""  # <--- input your API_KEY from etherscan.io

    endpoint =  input("Choise endpoint (1 - ether, 2 - bsc, 3 - polygon): ")
    address = input("Input address of a verified smart contract: ")

    try:
        save_contract(EVMScan(API_KEY, endpoints[endpoint]), address)
    except KeyboardInterrupt:
        pass
