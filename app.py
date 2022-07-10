import json
import os

from etherscan import EtherScan


if __name__ == "__main__":
    ether = EtherScan("API_KEY") # <--- input your API_KEY from etherscan.io

    address = input("Input address of a verified smart contract: ")

    source = ether.get_source_code(address)

    contract_name = source["result"][0]["ContractName"]
    source_code = json.loads(source["result"][0]["SourceCode"])
    abi = source["result"][0]["ABI"]

    if not os.path.exists(contract_name):
        os.mkdir(contract_name)

    for filename in source_code:
        with open(f"{contract_name}/{filename}", "w+") as f:
            f.write(source_code[filename]["content"])

    with open(f"{contract_name}/abi.json", "w+") as f:
        f.write(abi)
