from flask import Flask,render_template,redirect,request,session
from web3 import Web3,HTTPProvider
from ca import *
import json
import random

def createTripId():
    while True:
        k=random.randint(1,9999)
        f=open('rides.txt','r')
        a=f.readlines()
        f.close()
        a=[int(i) for i in a]
        f.close()
        if k not in a:
            f=open('rides.txt','a')
            f.write(str(k)+'\n')
            f.close()
            break
    return(k)


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

def connect_Blockchain_carpool(acc):
    blockchain_address="http://127.0.0.1:8545"
    web3=Web3(HTTPProvider(blockchain_address))
    if(acc==0):
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/carpool.json'
    contract_address=carContract
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
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(walletaddr)
    _usernames,_names,_emails,_mobiles,_passwords=contract.functions.viewUsers().call()

    contract,web3=connect_Blockchain_carpool(walletaddr)
    _drivers,_places,_cartype,_counts,_rideid,_minAmount,_from,_to,_dates=contract.functions.viewRides().call()
    data=[]
    for i in range(len(_rideid)):
        if _counts[i]!=0:
            dummy=[]
            userIndex=_usernames.index(_drivers[i])
            dummy.append(_names[userIndex])
            dummy.append(_places[i])
            dummy.append(_cartype[i])
            dummy.append(_counts[i])
            dummy.append(_rideid[i])
            dummy.append(_minAmount[i])
            dummy.append(_from[i])
            dummy.append(_to[i])
            dummy.append(_dates[i])
            data.append(dummy)
    l=len(data)
    return render_template('dashboard.html',len=l,dashboard_data=data)

@app.route('/book/<id>')
def bookingRide(id):
    print(id)
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(walletaddr)
    _usernames,_names,_emails,_mobiles,_passwords=contract.functions.viewUsers().call()

    contract,web3=connect_Blockchain_carpool(walletaddr)
    _drivers,_places,_cartype,_counts,_rideid,_minAmount,_from,_to,_dates=contract.functions.viewRides().call()
    
    data=[]
    for i in range(len(_rideid)):
        if int(id)==int(_rideid[i]):
            dummy=[]
            userIndex=_usernames.index(_drivers[i])
            dummy.append(_names[userIndex])
            dummy.append(_places[i])
            dummy.append(_cartype[i])
            dummy.append(_counts[i])
            dummy.append(id)
            dummy.append(_minAmount[i])
            dummy.append(_from[i])
            dummy.append(_to[i])
            dummy.append(_dates[i])
            data.append(dummy)
    l=len(data)
    print(data)
    session['tripid']=id
    return render_template('bidride.html',len=l,dashboard_data=data)

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/createride')
def createride():
    return render_template('createride.html')

@app.route('/createrideForm',methods=['POST','GET'])
def createrideForm():
    cartype=request.form['cartype']
    poolsize=request.form['poolsize']
    minamount=request.form['minamount']
    fromi=request.form['from']
    to=request.form['to']
    places=request.form['places']
    walletaddr=session['walletaddr']
    date=request.form['date']
    tripid=createTripId()
    print(cartype,poolsize,minamount,fromi,to,places,walletaddr,tripid,date)
    contract,web3=connect_Blockchain_carpool(walletaddr)
    tx_hash=contract.functions.createRide(walletaddr,places,cartype,int(poolsize),int(tripid),int(minamount),fromi,to,date).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return(redirect('/dashboard'))

@app.route('/bidrideForm',methods=['GET','POST'])
def bidrideForm():
    walletaddr=session['walletaddr']
    id=session['tripid']
    place=request.form['place']
    bidamount=int(request.form['bidamount'])
    print(place,bidamount)
    contract,web3=connect_Blockchain_carpool(walletaddr)
    tx_hash=contract.functions.bidRide(int(id),walletaddr,place,bidamount).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/mybids')

@app.route('/bidrequests')
def bidrequests():
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(walletaddr)
    _usernames,_names,_emails,_mobiles,_passwords=contract.functions.viewUsers().call()

    contract,web3=connect_Blockchain_carpool(walletaddr)
    _drivers,_places,_cartype,_counts,_rideid,_minAmount,_from,_to,_dates=contract.functions.viewRides().call()
    _tripids,_bidders,_bidplaces,_bidamounts,_bidstatus=contract.functions.viewBids().call()
    data=[]
    for i in range(len(_bidders)):
        tripIndex=_rideid.index(_tripids[i])
        if _drivers[tripIndex]==walletaddr and _bidstatus[i]==False:
            dummy=[]
            dummy.append(_tripids[i])
            dummy.append(_bidders[i])
            bidderIndex=_usernames.index(_bidders[i])
            dummy.append(_names[bidderIndex])
            dummy.append(_bidplaces[i])
            dummy.append(_bidamounts[i])
            data.append(dummy)
    l=len(data)
    return render_template('bidrequests.html',len=l,dashboard_data=data)

@app.route('/mybids')
def mybids():
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_carpool(walletaddr)
    _tripids,_bidders,_bidplaces,_bidamounts,_bidstatus=contract.functions.viewBids().call()
    data=[]
    for i in range(len(_bidders)):
        if(_bidders[i]==walletaddr):
            dummy=[]
            dummy.append(_tripids[i])
            dummy.append(_bidplaces[i])
            dummy.append(_bidamounts[i])
            if _bidstatus[i]==False:
                dummy.append('Not Accepted')
            else:
                dummy.append('Accepted')
            data.append(dummy)
    l=len(data)

    return render_template('bidstatus.html',len=l,dashboard_data=data)

@app.route('/bid/<id>/<id2>')
def acceptBid(id,id2):
    print(id)
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(walletaddr)
    _usernames,_names,_emails,_mobiles,_passwords=contract.functions.viewUsers().call()

    contract,web3=connect_Blockchain_carpool(walletaddr)
    tx_hash=contract.functions.acceptBid(int(id2),id).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/mybids')

@app.route('/myrides')
def myrides():
    walletaddr=session['walletaddr']
    contract,web3=connect_Blockchain_register(walletaddr)
    _usernames,_names,_emails,_mobiles,_passwords=contract.functions.viewUsers().call()

    contract,web3=connect_Blockchain_carpool(walletaddr)
    _drivers,_places,_cartype,_counts,_rideid,_minAmount,_from,_to,_dates=contract.functions.viewRides().call()

    _tripids,_bidders,_bidplaces,_bidamounts,_bidstatus=contract.functions.viewBids().call()
    data=[]
    for i in range(len(_rideid)):
        if _drivers[i]==walletaddr:
            dummy=[]
            dummy.append(_rideid[i])
            ownerIndex=_usernames.index(walletaddr)
            k=str(_names[ownerIndex])
            tripid=_tripids[i]
            for j in range(len(_bidders)):
                if tripid==_rideid[j] and _bidstatus[j]==True:
                    bidderIndex=_usernames.index(_bidders[j])
                    k+=','+str(_names[bidderIndex])
            dummy.append(k)
            dummy.append(_dates[i])
            data.append(dummy)
    l=len(data)
    return render_template('myrides.html',len=l,dashboard_data=data)

if(__name__=="__main__"):
    app.run(debug=True)