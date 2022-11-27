from loguru import logger

from config import API_KEY, ENDPOINTS, SCANS
from utils.deployment import deploy_contract
from utils.saving import get_contract_bytecode, save_contract
from utils.scan_api import EVMScan


if __name__ == "__main__":
    action = input("Select an action (1 - save the contract, 2 - deploy to testnet): ")

    endpoint =  input("Choise mainnet endpoint (1 - ether, 2 - bsc, 3 - polygon, 4 - rinkeby): ")
    address = input("Input address of a verified smart contract: ")

    if action.strip() == "1":
        save_contract(EVMScan(API_KEY, ENDPOINTS[endpoint]), address)

    elif action.strip() == "2":
        bytecode = get_contract_bytecode(SCANS[endpoint], address)

        chain_id = int(input(f"Choose chain_id (rinkeby - 4 , goerli - 5, kovan - 42, ropsten - 3, bsc_testnet - 97): "))
        rpc = input("Enter the RPC http: ")
        private_key = input("Enter the private key: ")
        gas_limit = int(input("Enter the gas limit: "))
        gwei = float(input("Enter the value of gwei: "))

        txn_hash = deploy_contract(rpc, private_key, bytecode, chain_id, gas_limit, gwei)

        logger.success(f"Hash: {txn_hash}")
