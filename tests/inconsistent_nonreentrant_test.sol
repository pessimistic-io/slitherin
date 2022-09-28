//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract inconsistent_nonreentrant_test {
    uint256 private _guardCounter;
    uint256 a;

    modifier nonReentrant() {
        _guardCounter += 1;
        uint256 localCounter = _guardCounter;
        _;
        require(localCounter == _guardCounter);
    }

    function nonReentrantFunc_ok(uint256 b) external nonReentrant {
        a = b;
    }

    function nonReentrantFunc_vulnerable(uint256 b) external {
        a = b;
    }

    function nonReentrantViewFunc_ok(uint256 b)
        external
        view
        returns (uint256)
    {
        return a + b;
    }
}
