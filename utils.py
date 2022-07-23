import asyncio
import json
import os
from typing import List

import aiofiles
from aiofiles.os import mkdir
from loguru import logger

from etherscan import AsyncEtherScan, EtherScan


async def async_save_contracts(ether: AsyncEtherScan, queue: asyncio.Queue) -> None:
    while not queue.empty():
        contract = await queue.get()

        source = await ether.get_source_code(contract)

        contract_name = source["result"][0]["ContractName"]
        abi = source["result"][0]["ABI"]

        logger.info(f"Saving {contract_name}...")

        if not os.path.exists(contract_name):
            await mkdir(contract_name)

        # references with bad-json
        if source["result"][0]["SourceCode"].startswith("{{"):
            source_code = json.loads(source["result"][0]["SourceCode"][1:-1])

            for dirs_with_file in source_code["sources"]:
                dirs = "/".join(dirs_with_file.split("/")[:-1])
                filename = dirs_with_file.split("/")[-1]

                if not os.path.exists(f"{contract_name}/{dirs}"):
                    os.makedirs(f"{contract_name}/{dirs}")

                async with aiofiles.open(f"{contract_name}/{dirs}/{filename}", "w+", encoding="UTF-8") as f:
                    await f.write(source_code["sources"][dirs_with_file]["content"])

            async with aiofiles.open(f"{contract_name}/abi.json", "w+") as f:
                await f.write(abi)
        # source code in single file
        elif not is_json(source["result"][0]["SourceCode"]):
            source_code = source["result"][0]["SourceCode"]

            async with aiofiles.open(f"{contract_name}/{contract_name}.sol", "w+", encoding="UTF-8") as f:
                await f.write(source_code)

            async with aiofiles.open(f"{contract_name}/abi.json", "w+") as f:
                await f.write(abi)

        await asyncio.sleep(1)


async def worker(ether: AsyncEtherScan, contracts: List[str]) -> None:
    queue = asyncio.Queue()

    for email in contracts:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(async_save_contracts(
             ether, queue)) for _ in range(5)]

    await asyncio.gather(*tasks)


def is_json(string: str) -> bool:
    try:
        json.loads(string)
    except ValueError as e:
        return False
    return True


def sync_save_contract(ether: EtherScan, address: str):
    source = ether.get_source_code(address)

    contract_name = source["result"][0]["ContractName"]
    abi = source["result"][0]["ABI"]

    if not os.path.exists(contract_name):
        os.mkdir(contract_name)

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

    logger.success(f'{contract_name} saved!')
