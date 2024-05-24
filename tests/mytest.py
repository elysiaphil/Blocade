from web3 import Web3
from web3.middleware import geth_poa_middleware
from solcx import compile_files

# Compile the Vyper contract
compiled_sol = compile_files(["MyNFT.vy"])

# Extract the contract ABI and bytecode
contract_interface = compiled_sol['MyNFT']

# Initialize web3 provider
web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # Connect to your local Ethereum node
web3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Inject PoA middleware for Ganache

# Set default account
web3.eth.defaultAccount = web3.eth.accounts[0]

# Deploy the contract
MyNFT = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx_hash = MyNFT.constructor().transact()
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
contract_address = tx_receipt.contractAddress

# Load the contract instance
contract_instance = web3.eth.contract(abi=contract_interface['abi'], address=contract_address)

# Define a function to test NFT transfer
def test_nft_transfer():
    # Mint some NFTs
    contract_instance.functions.mint(web3.eth.defaultAccount, 1).transact()
    contract_instance.functions.mint(web3.eth.defaultAccount, 2).transact()

    # Get balance before transfer
    balance_before = contract_instance.functions.balanceOf(web3.eth.defaultAccount).call()

    # Transfer NFT to another address
    contract_instance.functions.transferNFT(web3.eth.defaultAccount, "0x6CAAC11FeA147b0E3D4D6c9722F12e5e273fa130", tokenId).transact()  # Replace "0x123..." with recipient's address

    # Get balance after transfer
    balance_after = contract_instance.functions.balanceOf(web3.eth.defaultAccount).call()

    # Assert that balance decreased by 1 after transfer
    assert balance_before - balance_after == 1

# Run the test function
test_nft_transfer()
