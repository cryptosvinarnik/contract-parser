from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware


class Deployer():

    def __init__(self, rpc_provider: str, private_key: str) -> None:
        self.w3 = Web3(Web3.HTTPProvider(rpc_provider))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.private_key = private_key

    def deploy_contract(self, bytecode: str, gas: int, chain_id: int, gwei: float) -> str:
        tx = {
            "data": bytecode,
            "chainId": chain_id,
            "nonce": self.w3.eth.get_transaction_count(Account().from_key(self.private_key).address),
            "gas": gas,
            "gasPrice": self.w3.toWei(gwei, "gwei")
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)

        return self.w3.eth.sendRawTransaction(signed_tx.rawTransaction).hex()


def deploy_contract(rpc: str, private_key: str, bytecode: str, chain_id: int, gas_limit: int, gwei: float) -> str:
    deployer = Deployer(rpc, private_key)

    return deployer.deploy_contract(bytecode, gas_limit, chain_id, gwei)
