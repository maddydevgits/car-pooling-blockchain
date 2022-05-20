from flask import Flask,render_template,redirect,request,session
from web3 import Web3,HTTPProvider
from ca import *
import json

def connect_Blockchain_register(acc):
    blockchain_address="http://127.0.0.1:8545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/register.json'
    contract_address=registerContract
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']

    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    print('connected with blockchain')
    return (contract,web3)

app=Flask(__name__)
app.secret_key='makeskilled'

@app.route('/')
def indexPage():
    return render_template('index.html')

@app.route('/registerUser',methods=['GET','POST'])
def registerUser():
    walletaddr=request.form['walletaddr']
    name=request.form['name']
    mobile=request.form['mobile']
    password=request.form['password']
    email=request.form['email']
    print(walletaddr,name,mobile,password,email)
    contract,web3=connect_Blockchain_register(walletaddr)
    tx_hash=contract.functions.registerUser(walletaddr,name,email,mobile,password).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(redirect('/'))

@app.route('/loginUser',methods=['GET','POST'])
def loginUser():
    walletaddr=request.form['walletaddr1']
    password=request.form['password1']
    print(walletaddr,password)
    contract,web3=connect_Blockchain_register(walletaddr)
    state=contract.functions.loginUser(walletaddr,password).call()
    print(state)
    if(state==True):
        session['walletaddr']=walletaddr
        return(redirect('/dashboard'))
    else:
        return(redirect('/'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if(__name__=="__main__"):
    app.run(debug=True)