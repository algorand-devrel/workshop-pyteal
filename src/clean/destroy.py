import base64
import json
import os

from algosdk.future import transaction
from algosdk import account, mnemonic, logic
from algosdk.v2client import algod
from pyteal import *
from ..utils.sandbox import  get_accounts
from ..utils.sandbox import  destroy_apps

# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def main() :
    # initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address)
    sender, pk = get_accounts()[0]
    destroy_apps(algod_client, sender, pk)
 
    
main()