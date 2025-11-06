from web3 import Web3, HTTPProvider
import json

web3 = Web3(HTTPProvider('http://127.0.0.1:7545'))
web3.eth.default_account = web3.eth.accounts[0]

compiled_contract_path = './build/contracts/register.json'
deployed_contract_address = '0xaaB498A19590544A563a3F7C611a97fD81ff1789'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

def to_bytes32(val):
    return Web3.to_bytes(text=val).ljust(32, b'\0')

tx_hash = contract.functions.addUser(
    to_bytes32('7893015625'),
    to_bytes32('madhu'),
    to_bytes32('hyderabad'),
    '0xF367d0653669067c9ACb3A07f3b653ED90231946'
).transact()

web3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction Hash:", tx_hash.hex())

_phonenos, _names, _places, _wallets = contract.functions.viewUsers().call()

# convert bytes32 → normal strings
def from_bytes32(b):
    return b.decode('utf-8').rstrip('\x00')

decoded_phones = [from_bytes32(x) for x in _phonenos]
decoded_names = [from_bytes32(x) for x in _names]
decoded_places = [from_bytes32(x) for x in _places]

print("Phone Numbers:", decoded_phones)
print("Names:", decoded_names)
print("Places:", decoded_places)
print("Wallets:", _wallets)
