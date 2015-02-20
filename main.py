from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request
from flask import make_response
import json
import db
import addresses
import bitcoind
import process

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS']=True

@app.route('/')
def something():
  response=make_response("Hey there!", 200)
  response.headers['Access-Control-Allow-Origin']= '*'
  return response

@app.route('/status')
def status():
    jsonresponse={}
    try:
        jsonresponse['bitcoind_last_block']=bitcoind.connect("getblockcount", [])
    except:
        jsonresponse['bitcoind_last_block'] = "BITCOIND DOWN"
    jsonresponse['lastblock_processed'] = db.dbexecute("select * from meta;", True)
    jsonresponse=json.dumps(jsonresponse)
    response=make_response(str(jsonresponse), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin']= '*'
    return response

@app.route('/bitcoin/lastblock')
def last_block_bitcoin():
    lastblock = bitcoind.connect("getblockcount", [])
    response=make_response(str(lastblock), 200)
    response.headers['Access-Control-Allow-Origin']= '*'
    return response

@app.route('/meta')
def last_block_updated():
    lastblock = db.dbexecute("select * from meta;",True)
    d = {}
    d['last_block'] = str(lastblock[0][0])
    response=make_response(str(lastblock[0][0]), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin']= '*'
    return response

@app.route('/address/<public_address>/txs')
def txs_on_address(public_address = None):
    txs = addresses.txs_pertaining_to_address(public_address)
    jsonresponse={}
    jsonresponse['txs']=txs
    jsonresponse['public_address']=public_address
    jsonresponse=json.dumps(jsonresponse)
    response=make_response(str(jsonresponse), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin']= '*'
    return response

@app.route('/address/<public_address>/<depth>')
def correlations_on_address(public_address = None, depth = None):
    if depth == None:
        depth = 3
    else:
        depth = int(depth)
    a=process.get_temporary_address_correlations(public_address, depth)
    jsonresponse={}
    jsonresponse['correlations']=a
    jsonresponse['public_address']=public_address
    jsonresponse=json.dumps(jsonresponse)
    response=make_response(str(jsonresponse), 200)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin']= '*'
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
