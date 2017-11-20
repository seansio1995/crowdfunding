from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import Crypto
from ast import literal_eval


random_generator = Random.new().read
RSAkey=RSA.generate(1024,random_generator).exportKey()
pubkey=RSA.importKey(RSAkey).publickey().exportKey()
receiver_pubkey=RSA.importKey(pubkey)
src_data="hello world"
enc_data = str(receiver_pubkey.encrypt(src_data.encode(), 32)[0])
print(src_data)
print(enc_data)
print(pubkey.decode())
print(RSAkey.decode())
privkey = RSA.importKey(RSAkey)
dec_data = privkey.decrypt(eval(enc_data)).decode()
print(dec_data)
