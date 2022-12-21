// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol"; //overflow checker just for Solidity <0.08

//import "@openzeppelin/contracts/access/Ownable.sol"; //get the only owner function

contract Lottery {
    using SafeMathChainlink for uint256; //checks for overflow in Solidity <0.8.0

    //public payabale address called players
    address payable[] public players;
    address payable recentWinner;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    address public owner;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        //OR lottery_state = 1;
    }

    function enter() public payable {
        //we can only enter if the lottery is open
        require(lottery_state == LOTTERY_STATE.OPEN);
        //$50 minimum entrance fee
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        //the price is given with 8 decimals, so we multiply by 10**10 to make it 18
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;

        return costToEnter;
    }

    function startLottery() public {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can't start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
    }

    function getRandomWinnerTransferAndReset() internal onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Not there yet"
        );
        //not working yet, just for test purposes
        uint256 randomNumber = 1;

        //get index of winner
        uint256 indexOfWinner = randomNumber % players.length;
        //get winner address
        recentWinner = players[indexOfWinner];
        //transfer to the winnner
        recentWinner.transfer(address(this).balance);
        //reset the players array
        players = new address payable[](0);
        //reset the lottery state
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }
}
