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


        # self.their = input("Other party's DID and verkey? ").strip().split(' ')
        # self.their_vk = self.their[1]
        # return self.wallet_handle, self.my_did, self.my_vk, self.their[0], self.their[1]

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

def send(senderEmail, senderPwd, server, port, dest, fileName, userInput):
    userInput = int(userInput)
    filename = fileName
    attachment = open(filename, "rb")

    # instance of MIMEMultipart
    m = MIMEMultipart()

    if userInput == 1:
        # attach the body with the msg instance
        m.attach(MIMEText('See attached file.', 'plain'))

        # instance of MIMEBase and named as p
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form
        p.set_payload((attachment).read())

        # encode into base64
        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename=msg.ap")

        # attach the instance 'p' to instance 'msg'
        m.attach(p)

    elif userInput == 2:
        # attach the body with the msg instance
        body = '{"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/tictactoe/1.0/move", "@id": "518be002-de8e-456e-b3d5-8fe472477a86", "ill_be": "X", "moves": ["X:B2"],"comment_ltxt": "Let\'s play tic-tac-to. I\'ll be X. I pick cell B2."}'
        m.attach(MIMEText(body, 'plain'))

    else:
        raise Exception("Wrong Input")

    # storing the senders email address.
    m['From'] = senderEmail  # TODO: get from config

    # storing the receivers email address
    m['To'] = dest

    # storing the subject
    m['Subject'] = 'temp'

    # creates SMTP session
    s = smtplib.SMTP(server, port)

    # start TLS for security
    s.starttls()

    # Authentication (If you use your personal email, use your personal password instread of 'I only talk via email!')
    s.login(senderEmail, senderPwd)

    # sending the mail
    s.sendmail(senderEmail, dest, m.as_string())

    # terminating the session
    s.quit()

def _get_config_from_cmdline():
    import argparse
    parser = argparse.ArgumentParser(description="Run a Hyperledger Indy agent that communicates by email.")
    parser.add_argument("--ll", metavar='LVL', default="DEBUG", help="log level (default=INFO)")
    args = parser.parse_args()
    return args

def get_config_from_file(home):
    import configparser
    cfg = configparser.ConfigParser()
    cfg_path = home+'/.mailagent/config.ini'
    if os.path.isfile(cfg_path):
        cfg.read(home+'/.mailagent/config.ini')
    return cfg

def apply_cfg(cfg, section, defaults):
    x = defaults
    if cfg and (cfg[section]):
        src = cfg[section]
        for key in src:
            x[key] = src[key]
    return x

def setUp(me):
    securemsg = SecureMsg(me)
    print ("securemsg")
    return securemsg
    # loop.run_until_complete(securemsg.encryptMsg('../mailagent/testFileToSend.json'))

async def demo(smtp, inputVal):
    while True:
        argv = input('> ').strip().split(' ')
        cmd = argv[0].lower()
        if re.match(cmd, 'send'):
            print("here is where I set userInput - init")
            # This is to send email to the agent.
            # You can use your personal email
            send(smtp['username'], smtp['password'], smtp['server'], smtp['port'], 'indyagent1@gmail.com', 'encrypted.dat', inputVal)
        # elif re.match(cmd, 'decrypt'):
        #     ##Code here
        elif re.match(cmd, 'quit'):
            break
        else:
            print('Huh?')


# while True:
#     argv = input('Enter 1 if you want to test sending msg via attached file.  Enter 2 if you want to send via email body: ').strip().split(' ')
#     cmd = argv[0].lower()
#     loop.run_until_complete(demo(smtp_cfg, cmd))
#     if re.match(cmd, 'quit'):
#         break
