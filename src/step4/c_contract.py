from pyteal import *

import os
 
"""Basic Counter Application"""
 
def approval_program():
   handle_creation = Seq(
       App.globalPut(Bytes("Count"), Int(0)),
       Approve()
   )
 
   handle_optin = Reject()
 
   handle_closeout = Reject()
 
   handle_updateapp = Reject()
 
   handle_deleteapp = Approve()
 
 
   add = Approve()
 
   deduct = Approve()
 
   handle_noop = Cond(
       [Txn.application_args[0] == Bytes("Add"), add],
       [Txn.application_args[0] == Bytes("Deduct"), deduct],
   )

 
   program = Cond(
       [Txn.application_id() == Int(0), handle_creation],
       [Txn.on_completion() == OnComplete.OptIn, handle_optin],
       [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
       [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
       [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
       [Txn.on_completion() == OnComplete.NoOp, handle_noop]
   )
   # Mode.Application specifies that this is a stateful smart contract
   return compileTeal(program, Mode.Application, version=5)
 
 
def clear_state_program():
   program = Approve()
   # Mode.Application specifies that this is a stateful smart contract
   return compileTeal(program, Mode.Application, version=5)

path = os.path.dirname(os.path.abspath(__file__))


# compile program to TEAL assembly
with open(os.path.join(path, "./approval.teal"), "w") as f:
    approval_program_teal = approval_program()
    f.write(approval_program_teal)


    # compile program to TEAL assembly
with open(os.path.join(path, "./clear.teal"), "w") as f:
    clear_state_program_teal = clear_state_program()
    f.write(clear_state_program_teal)
    
print(approval_program())
print(clear_state_program())