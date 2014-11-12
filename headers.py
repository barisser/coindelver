import hashlib
import struct

def construct_header(version, hash_previous_block, merkle_root, time, bits, nonce):  #all inputs in hex
  ver = version
  prev_block = hash_previous_block
  mrkl_root = merkle_root

  exp = bits >> 24
  mant = bits & 0xffffff
  target_hexstr = '%064x' % (mant * (1<<(8*(exp - 3))))
  target_str = target_hexstr.decode('hex')

  header = ( struct.pack("<L", ver) + prev_block.decode('hex')[::-1] +
            mrkl_root.decode('hex')[::-1] + struct.pack("<LLL", time, bits, nonce))
  hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()

  verified=False
  if hash[::-1] < target_str:
    verified=True
  hash=hash[::-1].encode('hex')

  return hash, verified, header


a=construct_header(2, '000000000000000117c80378b8da0e33559b5997f2ad55e2f7d18ec1975b9717','871714dcbae6c8193a2bb9b2a69fe1c0440399f38d94b3a0f1b447275a29978a',0x53058b35,0x19015f53, 856192328)
