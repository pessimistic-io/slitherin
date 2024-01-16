// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

contract Test {
    function vulnerableArbNumber() external view returns (uint256 number) {
        number = block.number;
    }

    function vulnerableArbTimestamp()
        external
        view
        returns (uint256 difficulty)
    {
        difficulty = block.timestamp;
    }

    function vulnerableArbNumberTimestamp()
        external
        view
        returns (uint256 number, uint256 timestamp)
    {
        number = block.number;
        timestamp = block.timestamp;
    }

    function vulnerableArbNumberTimestampYul()
        external
        view
        returns (uint256 bnumber, uint256 btimestamp)
    {
        assembly {
            bnumber := number()
            btimestamp := timestamp()
        }
    }
}
