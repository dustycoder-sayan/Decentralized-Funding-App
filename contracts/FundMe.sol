// SPDX-License-Identifier: MIT 

pragma solidity ^0.8.0;

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public accountToAmount;
    address owner;
    uint256 public minimumAmountInUsd;
    address[] public funders;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeedAddress) {
        owner = msg.sender;
        minimumAmountInUsd = 50 * 10**18;
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function fund() public payable {
        require(getConversionRateFromEthInWeiToUsd(msg.value) >= minimumAmountInUsd, "Not enough funds");
        uint256 amount = msg.value;
        accountToAmount[msg.sender] += amount;
        funders.push(msg.sender);
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public onlyOwner payable {
        payable(msg.sender).transfer(address(this).balance);
        for(uint256 i=0;i<funders.length;i++) {
            accountToAmount[funders[i]] = 0;
        }
        funders = new address[](0);
    }

    function getEthToUsdPrice() public view returns (uint256) {
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * 10**10);
    }

    function getConversionRateFromEthInWeiToUsd(uint256 ethAmountInWei) public view returns (uint256) {
        uint256 ethToUsdPrice = getEthToUsdPrice();
        return (ethAmountInWei * ethToUsdPrice) / 10**18;
    }

    function getMinimumAmountToFundInEthWei() public view returns (uint256) {
        return (minimumAmountInUsd * 10**18) / getEthToUsdPrice();
    }
}