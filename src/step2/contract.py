from pyteal import *

import os
 
"""Basic Counter Application"""
 
def approval_program():
   program = Approve()
   # Mode.Application specifies that this is a stateful smart contract
   # compileTeal compiles pyteal expression into TEAL
   return compileTeal(program, Mode.Application, version=5)
 
 
def clear_state_program():
   program = Approve()
   # Mode.Application specifies that this is a stateful smart contract
   # compileTeal compiles pyteal expression into TEAL
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