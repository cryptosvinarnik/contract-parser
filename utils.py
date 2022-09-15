import json
import os

from loguru import logger

from scan_api import EVMScan


def is_json(string: str) -> bool:
    try:
        json.loads(string)
    except ValueError as e:
        return False
    return True


def save_contract(ether: EVMScan, address: str):
    source = ether.get_source_code(address)

    contract_name = source["result"][0]["ContractName"]
    abi = source["result"][0]["ABI"]

    if not os.path.exists(contract_name):
        os.mkdir(f"contracts/{contract_name}")

    # references with bad-json
    if source["result"][0]["SourceCode"].startswith("{{"):
        source_code = json.loads(source["result"][0]["SourceCode"][1:-1])

        for dirs_with_file in source_code["sources"]:
            dirs = "/".join(dirs_with_file.split("/")[:-1])
            filename = dirs_with_file.split("/")[-1]

            if not os.path.exists(f"contracts/{contract_name}/{dirs}"):
                os.makedirs(f"contracts/{contract_name}/{dirs}")

            with open(f"contracts/{contract_name}/{dirs}/{filename}", "w+", encoding="UTF-8") as f:
                f.write(source_code["sources"][dirs_with_file]["content"])

        with open(f"contracts/{contract_name}/abi.json", "w+") as f:
            f.write(abi)
    # source code in single file
    elif not is_json(source["result"][0]["SourceCode"]):
        source_code = source["result"][0]["SourceCode"]

        with open(f"contracts/{contract_name}/{contract_name}.sol", "w+", encoding="UTF-8") as f:
            f.write(source_code)

        with open(f"contracts{contract_name}/abi.json", "w+") as f:
            f.write(abi)

    logger.success(f'{contract_name} saved!')
