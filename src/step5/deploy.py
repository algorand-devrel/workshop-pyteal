import json
import os

from algosdk.future.transaction import *
from algosdk.v2client import algod
from pyteal import *
from ..utils.sandbox import  *

# user declared algod connection parameters. Node must have EnableDeveloperAPI set to true in its config
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    
# create new application
def create_app(client,  approval_program, clear_program, global_schema, local_schema):
    # define sender as creator
    sender, pk = get_accounts()[0]

    # declare on_complete as NoOp
    on_complete = OnComplete.NoOpOC.real

	# get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = ApplicationCreateTxn(sender, params, on_complete, \
                                            approval_program, clear_program, \
                                            global_schema, local_schema)

    # sign transaction
    signed_txn = txn.sign(pk)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    #wait_for_confirmation(client, tx_id, 20)
    # wait for confirmation 
    try:
        confirmed_txn = wait_for_confirmation(client, tx_id, 4)  
    except Exception as err:
        print(err)
        return
    
    # display results
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        
    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new app-id:", app_id)

    return app_id


# call application
def call_app(client, index, app_args) : 
    # declare sender
    sender, pk = get_accounts()[0]
    
    
	# get node suggested parameters
    params = client.suggested_params()

    # create unsigned transaction
    txn = ApplicationNoOpTxn(sender, params, index, app_args)

    # sign transaction
    signed_txn = txn.sign(pk)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    try:
        confirmed_txn = wait_for_confirmation(client, tx_id, 4)  
    except Exception as err:
        print(err)
        return
    # display results
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    
    print("Application called")

def main() :
    # initialize an algodClient
    algod_client = algod.AlgodClient(algod_token, algod_address)

    # declare application state storage (immutable)
    local_ints = 0
    local_bytes = 0
    global_ints = 1 
    global_bytes = 0
    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)

    path = os.path.dirname(os.path.abspath(__file__))

    # compile program to TEAL assembly
    with open(os.path.join(path, "./approval.teal"), "r") as f:
        approval_program_teal = f.read()


    # compile program to TEAL assembly
    with open(os.path.join(path, "./clear.teal"), "r") as f:
        clear_state_program_teal = f.read()

        
    # compile program to binary
    approval_program_compiled = compile_program(algod_client, approval_program_teal)
            
    # compile program to binary
    clear_state_program_compiled = compile_program(algod_client, clear_state_program_teal)

    print("--------------------------------------------")
    print("Deploying Counter application......")
    
    # create new application
    app_id = create_app(algod_client, approval_program_compiled, clear_state_program_compiled, global_schema, local_schema)

    sender, pk = get_accounts()[0]
    # read global state of application
    print("Global state:", read_global_state(algod_client, sender, app_id))

    print("--------------------------------------------")
    print("Calling Counter application......")
    app_args = ["Add"]
    call_app(algod_client, app_id, app_args)

    # read global state of application
    print("Global state:", read_global_state(algod_client, sender, app_id))
    
main()