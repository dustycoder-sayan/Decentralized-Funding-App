from scripts.deploy import deploy
from scripts.helper_scripts import get_account, DEVELOPMENT_ENVIRONMENTS
from brownie import accounts, exceptions, network
import pytest

def test_deployment():
    fund_me = deploy()
    minimumFund = fund_me.getMinimumAmountToFundInEthWei()
    account = get_account()

    txn1 = fund_me.fund(
        {
            "from": account,
            "value": minimumFund
        }
    )
    txn1.wait(1)

    assert fund_me.accountToAmount(account) == minimumFund

    txn2 = fund_me.withdraw(
        {
            "from": account
        }
    )
    txn2.wait(1)

    assert fund_me.accountToAmount(account) == 0

def test_withdraw_not_by_non_owner():
    if network.show_active() not in DEVELOPMENT_ENVIRONMENTS:
        pytest.skip("Test executed only in development chains")

    fund_me = deploy()
    bad_actor = accounts[-1]

    with pytest.raises(exceptions.VirtualMachineError):
        txn2 = fund_me.withdraw(
            {
                "from": bad_actor
            }
        )
        txn2.wait(1)