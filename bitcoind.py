import requests
import json
import os
import db
from requests.auth import HTTPBasicAuth
import datetime

#url='localhost:8332'
url = 'http://5b478df5.ngrok.com'
username='barisser'
password='2bf763d2132a2ccf3ea38077f79196ebd600f4a29aa3b1afd96feec2e7d80beb3d9e13d02d56de0f'
chain_api_key = 'c68b1ae1f0e763bf7867409bba0474f7'

def connect(method,body):
  node_url='http://'+url#+':'+node_port
  headers={'content-type':'application/json'}
  payload=json.dumps({'method':method,'params':body})
  result=requests.get(node_url,headers=headers,data=payload, verify=False, auth=HTTPBasicAuth(username, password))

  response=json.loads(result.content)
  return response['result']

def get_address_info_blockchaininfo(public_address):
    api_url = 'https://blockchain.info/address/'+str(public_address)+'?format=json'
    addressdata = requests.get(api_url).content
    addressdata = json.loads(addressdata)
    return addressdata

def get_address_info_chain(public_address):
    #https://api.chain.com/v2/bitcoin/addresses/1C3nG7RpEGq5VzVWdygM4RY35qJji8fx2c/transactions?api-key-id=c68b1ae1f0e763bf7867409bba0474f7
    api_url = 'https://api.chain.com/v2/bitcoin/addresses/'+str(public_address)+"/transactions?api-key-id="+chain_api_key
    txdata = requests.get(api_url).content
    txd = json.loads(txdata)
    return txd

def get_address_info_local(public_address):
    dbstring = "select txhash from outputs where public_address='"+str(public_address)+"';"
    result = db.dbexecute(dbstring, True)


def download_block_chain(height):
    api_url = "https://api.chain.com/v2/bitcoin/blocks/"+str(height)+"?api-key-id="+chain_api_key
    blockdata = requests.get(api_url).content
    bd = json.loads(blockdata)
    return bd

def download_tx_chain(txhash):
    api_url = "https://api.chain.com/v2/bitcoin/transactions/"+str(txhash)+"?api-key-id="+chain_api_key
    txdata = requests.get(api_url).content
    txd = json.loads(txdata)
    return tx

def download_block_local_node(height):
    blockhash = connect("getblockhash", [height])
    blockdata = connect("getblock", [blockhash])
    print str(height)+ "    "+str(datetime.datetime.fromtimestamp(int(blockdata['time'])).strftime("%Y-%m-%d %H:%M:%S"))+"    "+str(len(blockdata['tx']))
    return blockdata

def download_tx_local_node(txhash):
    txdata = connect("getrawtransaction", [txhash, 1])
    return txdata

def get_input_address(inputline):
    if 'txid' in inputline:
        txid = inputline['txid']
        oldtx = download_tx_local_node(txid)
        try:
            a = oldtx['vout'][inputline['vout']]['scriptPubKey']['addresses'][0]
            b = oldtx['vout'][inputline['vout']]['value']*100000000
        except:
            a=""
            b=-1
    else:
        a=""
        b=-1
    return a, b

def save_txs_in_block(height):
    #txs = download_block_chain(height)['transaction_hashes']
    txs = download_block_local_node(height)['tx']
    txdata = []
    inputs = []
    outputs = []
    queued_input_checks = []
    for tx in txs:
        r = download_tx_local_node(tx)
        txdata.append(r)
        for inp in r['vin']:
            g= get_input_address(inp)
            if g[1]>-1:
                input_address =g[0]
                amt =g[1]
                db.add_input_tx(input_address, r['txid'], amt, height)
                queued_input_checks.append([inp['txid'], inp['vout'], r['txid']])

        for outp in r['vout']:
            if 'scriptPubKey' in outp:
                if 'addresses' in outp['scriptPubKey']:
                    if len(outp['scriptPubKey']['addresses'])>0:
                        output_address = outp['scriptPubKey']['addresses'][0]
                        amt = outp['value']*100000000
                        db.add_output_tx(output_address, r['txid'], amt, height)
                        db.add_tx_output(r['txid'], outp['n'], False, '', height, -1, amt)

    for a in queued_input_checks:
        db.spent_tx_output(a[0], a[1], a[2], height)

    dbstring="update meta set lastblockdone='"+str(height)+"';"
    db.dbexecute(dbstring, False)

def save_next_blocks(nblocks):
    last_block = connect("getblockcount", [])
    last_block_in_db = db.dbexecute("select * from meta;", True)[0][0]
    if last_block - last_block_in_db < nblocks:
        nblocks = last_block - last_block_in_db
    next = last_block_in_db + nblocks
    for i in range(last_block_in_db+1, next+1):
        save_txs_in_block(i)

def get_tx_outputs(txhash):
    txdata = download_tx_local_node(txhash)
    results = []
    for x in txdata['vout']:
        y= {}
        y['value'] = x['value'] * 100000000
        if 'scriptPubKey' in x:
            if 'addresses' in x['scriptPubKey']:
                if len(x['scriptPubKey']['addresses'])>0:
                    y['address'] = x['scriptPubKey']['addresses'][0]


def get_tx_inputs(txhash):
    download_tx_local_node(txhash)
