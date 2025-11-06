from flask import Flask,render_template,request,redirect

from web3 import Web3, HTTPProvider
import json

web3=Web3(HTTPProvider('http://127.0.0.1:7545'))
web3.eth.default_account = web3.eth.accounts[0]

compiled_contract_path='./build/contracts/register.json'
deployed_contract_address='0x054F267F638C114897cd5480fE624319d48690Bd'

with open(compiled_contract_path) as file:
    contract_json=json.load(file)
    contract_abi=contract_json['abi']

contract=web3.eth.contract(address=deployed_contract_address,abi=contract_abi)

app=Flask(__name__)

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/needers')
def needersPage():
    return render_template('needers.html')

@app.route('/campaigns')
def campaigns():
    _phonenos,_names,_places,_wallets=contract.functions.viewUsers().call()
    _phonenosd=[]
    for i in _phonenos:
        i = i.hex().rstrip("0")
        if len(i) % 2 != 0:
            i = i + '0'
        i = bytes.fromhex(i).decode('utf8')
        print(i)
        _phonenosd.append(i)
    
    _namesd=[]
    for i in _names:
        i = i.hex().rstrip("0")
        if len(i) % 2 != 0:
            i = i + '0'
        i = bytes.fromhex(i).decode('utf8')
        print(i)
        _namesd.append(i)
    
    _placesd=[]
    for i in _places:
        i = i.hex().rstrip("0")
        if len(i) % 2 != 0:
            i = i + '0'
        i = bytes.fromhex(i).decode('utf8')
        print(i)
        _placesd.append(i)
    
    data=[]
    for i in range(len(_phonenosd)):
        dummy=[]
        dummy.append(_phonenosd[i])
        dummy.append(_namesd[i])
        dummy.append(_placesd[i])
        dummy.append(_wallets[i])
        data.append(dummy)
    return render_template('campaigns.html',result=data,len=len(data))


@app.route('/createNeedy', methods=['POST'])
def createNeedy():
    name = request.form['name']
    place = request.form['place']
    phonepe = request.form['phonepe']
    wallet = request.form['wallet']
    print(name, place, phonepe, wallet)

    # helper: convert text → bytes32
    def to_bytes32(val):
        return Web3.to_bytes(text=val).ljust(32, b'\0')

    tx_hash = contract.functions.addUser(
        to_bytes32(phonepe),
        to_bytes32(name),
        to_bytes32(place),
        wallet
    ).transact()

    web3.eth.wait_for_transaction_receipt(tx_hash)
    return render_template('needers.html', result='Needy Registered')


@app.route('/verifyNeedy',methods=['post'])
def verifyNeedy():
    phonepe=request.form['phonepe']
    print(phonepe)
    _phonenos,_names,_places,_wallets=contract.functions.viewUsers().call()
    _phonenosd=[]
    for i in _phonenos:
        i = i.hex().rstrip("0")
        if len(i) % 2 != 0:
            i = i + '0'
        i = bytes.fromhex(i).decode('utf8')
        print(i)
        _phonenosd.append(i)
    print(_phonenosd)
    if phonepe in _phonenosd:
        _uindex=_phonenosd.index(phonepe)
    else:
        _uindex=-1
    
    data=[]
    if(_uindex>=0):
        i=_names[_uindex]
        i = i.hex().rstrip("0")
        if len(i) % 2 != 0:
            i = i + '0'
        i = bytes.fromhex(i).decode('utf8')
        _named=i
        i=_places[_uindex]
        i = i.hex().rstrip("0")
        if len(i) % 2 != 0:
            i = i + '0'
        i = bytes.fromhex(i).decode('utf8')
        # print(i)
        _placed=i
        _walletd=_wallets[_uindex]
        dummy=[_named,_placed,_walletd,phonepe]
    else:
        dummy=['NA','NA','NA','NA']
    data.append(dummy)
    return (render_template('index.html',result=data,len=len(data)))

if __name__=="__main__":
    app.run(debug=True)