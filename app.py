import json
import os

from etherscan import EtherScan


if __name__ == "__main__":
    ether = EtherScan("API_KEY")  # <--- input your API_KEY from etherscan.io

    address = input("Input address of a verified smart contract: ")

    source = ether.get_source_code(address)

    try:
        source_code = json.loads(source["result"][0]["SourceCode"])
    except json.decoder.JSONDecodeError:
        source_code = json.loads(source["result"][0]["SourceCode"][1:-1])

    source_code = source_code["sources"] if source_code.get("sources") else source_code

    contract_name = source["result"][0]["ContractName"]
    abi = source["result"][0]["ABI"]

    if not os.path.exists(contract_name):
        os.mkdir(contract_name)

    for filename in source_code:
        with open(f"{contract_name}/{filename.split('/')[-1]}", "w+") as f:
            f.write(source_code[filename]["content"])

    with open(f"{contract_name}/abi.json", "w+") as f:
        f.write(abi)
