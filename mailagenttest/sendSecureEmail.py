# Python code to illustrate Sending mail with json-format attachments
# from your Gmail account

# libraries to be imported
import smtplib
import os
import asyncio
import time
import re
import json

from indy import crypto, did, wallet

from os.path import expanduser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class SecureMsg():
    async def encryptMsg(self, msg):
        # with open(decrypted, 'rb') as f:
        #     msg = f.read()
        encrypted = await crypto.auth_crypt(self.wallet_handle, self.my_vk, self.their_vk, msg)
        # encrypted = await crypto.anon_crypt(their_vk, msg)
        print('encrypted = %s' % repr(encrypted))
        with open('encrypted.dat', 'wb') as f:
            f.write(bytes(encrypted))
        print('prepping %s' % msg)
        print('encryp type is: ', type(encrypted))
        return encrypted

#     # Step 6 code goes here, replacing the read() stub.
    async def decryptMsg(self, encrypted):
        decrypted = await crypto.auth_decrypt(self.wallet_handle, self.my_vk, encrypted)
        # decrypted = await crypto.anon_decrypt(wallet_handle, my_vk, encrypted)
        return (decrypted)
#
    async def init(self, me):
        me = me.strip()
        self.wallet_config = '{"id": "%s-wallet"}' % me
        self.wallet_credentials = '{"key": "%s-wallet-key"}' % me

        # 1. Create Wallet and Get Wallet Handle
        try:
            await wallet.create_wallet(self.wallet_config, self.wallet_credentials)
        except:
            pass
        try:
            self.wallet_handle = await wallet.open_wallet(self.wallet_config, self.wallet_credentials)
            (self.my_did, self.my_vk) = await did.create_and_store_my_did(self.wallet_handle, "{}")
            print('wallet = %s' % self.wallet_handle)
            print('my_did and verkey = %s %s' % (self.my_did, self.my_vk))
        except:
            pass

    def __init__(self, me):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.init(me))
            time.sleep(1)  # waiting for libindy thread complete
        except KeyboardInterrupt:
            print('')

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
       if isinstance(obj, A):
          return { "foo" : obj.foo }
       return json.JSONEncoder.default(self, obj)

async def encryptMsg(decrypted, wallet_handle, my_vk, their_vk):
    with open(decrypted, 'rb') as f:
        msg = f.read()
    encrypted = await crypto.auth_crypt(wallet_handle, my_vk, their_vk, msg)
    # encrypted = await crypto.anon_crypt(their_vk, msg)
    print('encrypted = %s' % repr(encrypted))
    with open('encrypted.dat', 'wb') as f:
        f.write(bytes(encrypted))
    print('prepping %s' % msg)

def setUp(me):
    securemsg = SecureMsg(me)
    print ("securemsg")
    return securemsg
