## Overview
This is a simple repo that shows step by step how to create a smart contract on Algorand using python with the PyTeal library. The smart contract holds a global variable that is incremented or decremented when it is called. See the accompanying ppt

## Contents
    slides - finished workshop example
    src -
    clean - python used to cleanup created contracts for the sandbox account
    step1 - 4 - Build steps for the workshop
        Each step contains a contract and deploy python file
        Contract generates the TEAL and deploy creates annd the smart contract
        c_contract contains what the pyteal should look like after completing the exercise
    utils - contains sanbox.py that offers utility functions to all steps for deploying the contract    
    ppt - presentation for the workshop

## Get Started
# Get the project
First clone the project

CD into the workshop

```
cd pytealworkshop
```

# Setup and Activate Python Environment

```
python -m venv .venv
source .venv/bin/activate
# use the following install latest release of pyteal
# pip install pyteal  
# to install the latest from Github use
pip install git+https://github.com/algorand/pyteal
# install the Algorand python SDK - note this installed automatically with pyteal
# pip3 install py-algorand-sdk
```

# Install and Start Sandbox In Dev Mode

```
git clone https://github.com/algorand/sandbox.git
cd sandbox
./sandbox up dev
```

# Run Examples
first, generate the TEAL for the example you want to run

```
python3 -m src.complete.contract
```

Deploy and call the example

```
python3 -m src.complete.deploy
```

For each step, you will run both of these

```
python3 -m src.step1.contract
python3 -m src.step1.deploy
```

# Clean up
Clean up all created apps on the sandbox account

```
python3 -m src.clean.destroy
```

