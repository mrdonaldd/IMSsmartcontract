# pip install python-multipart
import hashlib
from ctypes import addressof
import json
from traceback import print_tb
from web3 import Web3
from web3.middleware import geth_poa_middleware

from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware

pk= '0x052392f7ff63575c99b2e17a547fc6e35974b5d19dc71b17b260d860bbb120b5'
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
abiContract = json.loads('[{"inputs":[{"internalType":"string","name":"_id","type":"string"},{"internalType":"string","name":"_value","type":"string"}],"name":"add","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_id","type":"string"}],"name":"_checkID","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_value","type":"string"}],"name":"_checkValue","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_id","type":"string"},{"internalType":"string","name":"_value","type":"string"}],"name":"checkmatch","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_value","type":"string"}],"name":"getID","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getSizeID","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_id","type":"string"}],"name":"getValue","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_id","type":"string"},{"internalType":"string","name":"_value","type":"string"}],"name":"isCreateInvoice","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')
addressContract = web3.toChecksumAddress('0xcb50EdE077e277378eCb1620ec1A596e0fE1D02d') # FILL ME IN
contract = web3.eth.contract(address=addressContract, abi=abiContract)

def getSizeID():
    _num = contract.functions.getSizeID().call()
    return(_num)

def add(_id,_value):
    store_contact = contract.functions.add(_id, _value).buildTransaction({"chainId": 1981, "from": '0xDb27962ef68be525Dbc3f0983d2Aa00332dCd926', "gasPrice": web3.eth.gas_price, "nonce": web3.eth.get_transaction_count('0xDb27962ef68be525Dbc3f0983d2Aa00332dCd926') })
    # Sign the transaction
    sign_store_contact = web3.eth.account.sign_transaction(store_contact, private_key=pk)
    # Send the transaction
    send_store_contact = web3.eth.send_raw_transaction(sign_store_contact.rawTransaction)
    transaction_receipt = web3.eth.wait_for_transaction_receipt(send_store_contact)
    return True

def checkIDInvoice(_id):
    isID = contract.functions._checkID(_id).call()
    return(isID)

def checkValueInvoicce(_value):
    isValue = contract.functions._checkValue(_value).call()
    return(isValue)

def ValidateData(_id,_value):
    validate = contract.functions.checkmatch(_id,_value).call()
    return(validate)

def getID(_value):
    id = contract.functions.getID(_value).call()
    return(id)

def getValue(_id):
    value = contract.functions.getValue(_id).call()
    return(value)

def isCreateInvoice(_id,_value):
    isCreate = contract.functions.isCreateInvoice(_id,_value).call()
    return(isCreate)

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://localhost:3502"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/totalinvoice")
def totalinvoice():
    return {'Total':getSizeID()}

@app.post("/createinvoice")
async def createInvoice(payload: dict = Body(...)):
    _id = payload['id']
    _value = payload['value']
    canCreate = isCreateInvoice(_id,_value)
    if (canCreate):
        add(_id,_value)
        return {'create':'Success'}
    else:
        return {'create':'Fail'}

@app.post("/uploadfile/")
async def create_upload_file(ID: str = Form(...),file: UploadFile = File(...)):
   data = file.file.read()
   hash = hashlib.sha256(data) 
   _id = ID
   _value = hash.hexdigest()
   canCreate = isCreateInvoice(_id,_value)
   if (canCreate):
        add(_id,_value)
        return {'create':'Success'}
   else:
       return {'create':'Fail'}

@app.post("/searchwithid")
async def searchWithID(payload: dict = Body(...)):
    _id = payload['id']
    isData = checkIDInvoice(_id)
    if (isData):
        return {'Data Hash of this InvoiceID ' : getValue(_id)}
    else :
        return False



@app.post("/checkid")
async def checkID(payload: dict = Body(...)):
    _id = payload['id']
    return { 'Is there an ID in the system? ':checkIDInvoice(_id)}


@app.post("/validatedata")
async def ValidateData_api(payload: dict = Body(...)):
    _id = payload['id']
    _value = payload['value']
    ValidateData(_id,_value)
    if (ValidateData(_id,_value)):
        return {'Does the information match? ':True}
    else:
        return {'Does the information match? ':False}

# @app.post("/getdatawithid")
# async def getDataWithID(payload: dict = Body(...)):
#     _id = payload['id']
#     return { 'Data Invoice is ':getValue(_id)}

@app.post("/getdidwithdata")
async def getIDWithData(payload: dict = Body(...)):
    _value = payload['value']
    isID = getID(_value)
    if (isID == 'null'):
        return False
    return { 'ID Invoice is ':isID}


if __name__ == "__main__":
#   # uvicorn.run(app, host="0.0.0.0", port=3502)
    uvicorn.run(app, port=3502)



# print(getSizeID())
# print(checkIDInvoice('im2022'))
# print(add('im2022','abc01'))
# print(web3.eth.get_transaction_count('0xDb27962ef68be525Dbc3f0983d2Aa00332dCd926'))
# print(ValidateData('im2022','abc01')) ## True
# print(ValidateData('im2022','abc02')) ## False
# print(ValidateData('im2023','abc02')) ## False
# print(ValidateData('im2023','abc01')) ## False
# print(getID('abc02')) ## null
# print(getID('abc01')) ## False
# print(getValue('im2022'))
# print(isCreateInvoice('im2022','abc01'))


