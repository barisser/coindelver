import requests
import json
import os
from requests.auth import HTTPBasicAuth

url='localhost:8332'
username='barisser'
password='dfjhidfjh903gk34g3jghfdplbkd2154215323'

def connect(method,body):
  node_url='http://'+url#+':'+node_port
  headers={'content-type':'application/json'}
  payload=json.dumps({'method':method,'params':body})
  result=requests.get(node_url,headers=headers,data=payload, verify=False, auth=HTTPBasicAuth(username, password))

  response=json.loads(result.content)
  return response['result']

def get_block_blockchaininfo(height):
  api_url = "http://blockchain.info/block-height/"+str(height)+"?format=json"
  blockdata = requests.get(api_url).content
  blockdata = json.loads(blockdata)

  for x in blockdata['blocks']:
    if x['main_chain']:
      return x
