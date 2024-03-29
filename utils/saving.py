import json
import os
import shutil
from zipfile import ZipFile

import httpx
from bs4 import BeautifulSoup
from loguru import logger

from utils.scan_api import EVMScan


def is_json(string: str) -> bool:
    try:
        json.loads(string)
    except ValueError as e:
        return False
    return True


def get_contract_bytecode(endpoint: str, address: str) -> str:
    page = httpx.get(f"{endpoint}/address/{address}")
    soup = BeautifulSoup(page.text, "html.parser")

    return soup.find("div", {"id": "verifiedbytecode2"}).text


def get_contract_abi(ether: EVMScan, address: str):
    source = ether.get_source_code(address)

    return source["result"][0]["ABI"]


def save_contract(ether: EVMScan, address: str):
    source = ether.get_source_code(address)

    contract_name = source["result"][0]["ContractName"]
    abi = source["result"][0]["ABI"]

    if not os.path.exists(contract_name):
        os.mkdir(f"{contract_name}")

    # references with bad-json
    if source["result"][0]["SourceCode"].startswith("{{"):
        source_code = json.loads(source["result"][0]["SourceCode"][1:-1])

        for dirs_with_file in source_code["sources"]:
            dirs = "/".join(dirs_with_file.split("/")[:-1])
            filename = dirs_with_file.split("/")[-1]

            if not os.path.exists(f"{contract_name}/{dirs}"):
                os.makedirs(f"{contract_name}/{dirs}")

            with open(f"{contract_name}/{dirs}/{filename}", "w+", encoding="UTF-8") as f:
                f.write(source_code["sources"][dirs_with_file]["content"])

        with open(f"{contract_name}/abi.json", "w+") as f:
            f.write(abi)
    # source code in single file
    elif not is_json(source["result"][0]["SourceCode"]):
        source_code = source["result"][0]["SourceCode"]

        with open(f"{contract_name}/{contract_name}.sol", "w+", encoding="UTF-8") as f:
            f.write(source_code)

        with open(f"{contract_name}/abi.json", "w+") as f:
            f.write(abi)

    with ZipFile(f"contracts/{contract_name}.zip", "w") as zip:
        for dirname, _, files in os.walk(contract_name):
            zip.write(dirname)
            for filename in files:
                zip.write(os.path.join(dirname, filename))

    shutil.rmtree(contract_name)

    logger.success(f"{contract_name} saved!")

    return f"contracts/{contract_name}.zip"
