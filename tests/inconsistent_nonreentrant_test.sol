//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract inconsistent_nonreentrant_test {
    uint256 private _guardCounter;
    uint256 a;

    event OK();

    modifier nonReentrant() {
        _guardCounter += 1;
        uint256 localCounter = _guardCounter;
        _;
        require(localCounter == _guardCounter);
    }

    function nonReentrantFunc_vuln(uint256 b) external {
        a = b;
        _nonReentrantInternal();
    }

    function nonReentrantFunc_ok(uint256 b) nonReentrant external {
        a = b;
    }

    function _nonReentrantInternal() internal {
        emit OK();
    }

    function nonReentrantViewFunc_ok(uint256 b)
        external
        view
        returns (uint256)
    {
        return a + b;
    }
}

contract inconsistent_nonreentrant_false_test {

    mapping (address=>uint) a;

    address immutable self;

    constructor (){
        self=address(this);
    }

    function markMe(uint256 b) external {
        a[msg.sender] = b;
    }

    function markYou(uint256 b) external {
        a[self] = b;
    }

}
