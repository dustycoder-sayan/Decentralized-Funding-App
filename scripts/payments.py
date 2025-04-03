from brownie import FundMe
from scripts.helper_scripts import get_account, get_pricefeed_address
from scripts.deploy import deploy

if len(FundMe) > 0:
    fund_me = FundMe[-1]
else:
    fund_me = deploy()

def pay_to_contract(account, amount):
    txn = fund_me.fund(
        {
            "from": account,
            "value": amount
        }
    )
    txn.wait(1)

def withdraw_from_contract(account):
    txn = fund_me.withdraw(
        {
            "from": account
        }
    )
    txn.wait(1)

def main():
    minimum_funding_amount = fund_me.getMinimumAmountToFundInEthWei()
    pay_to_contract(get_account(), minimum_funding_amount)
    withdraw_from_contract(get_account())