import os
import timeit
import json
from web3 import Web3


def benchmark_tx_requests(w3: Web3, block_number: int):
    for i in range(block_number - 100, block_number):
        b = w3.eth.get_block(i)
        # print(f'{i}/{block_number}', b)


def benchmark_contract_call(w3: Web3):
    # USDC/ETH 0.05% pool
    uniswap_v3_pool_address = '0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640'  # checksum address
    uniswap_v3_pool_abi = [
        {
            'inputs': [],
            'name': 'factory',
            'outputs': [{'internalType': 'address', 'name': '', 'type': 'address'}],
            'stateMutability': 'view',
            'type': 'function'
        }
    ]
    pool = w3.eth.contract(address=uniswap_v3_pool_address, abi=uniswap_v3_pool_abi)
    factory_address = pool.functions.factory().call()
    # print(factory_address)


def get_endpoint_arr():
    with open('../rpc-benmark/endpoints.json') as f:
        d = json.load(f)
        return d


if __name__ == '__main__':
    all_rpc = get_endpoint_arr()
    dummy = Web3(Web3.HTTPProvider('https://eth.llamarpc.com'))

    # Ensure they start at the same block
    start_block = dummy.eth.get_block('latest').number
    for rpc in all_rpc:
        endpoint_name = rpc['name']
        endpoint_rpc_url = rpc['rpc_url']
        provider = Web3(Web3.HTTPProvider(endpoint_rpc_url))

        # TX requests
        tx_req_bm = timeit.timeit(lambda: benchmark_tx_requests(provider, start_block), number=1)

        # Contract calls
        contract_call_bm = timeit.timeit(lambda: benchmark_contract_call(provider), number=10)

        print(endpoint_name, tx_req_bm, contract_call_bm)


