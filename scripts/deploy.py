from brownie import FundMe, config
from scripts.helper_scripts import get_account, get_pricefeed_address, get_verify_value
from time import sleep

def deploy():
    account = get_account()
    fund_me = FundMe.deploy(
        get_pricefeed_address(),
        {
            "from": account
        },
        publish_source=get_verify_value()
    )
    sleep(1)

    return fund_me

def main():
    deploy()