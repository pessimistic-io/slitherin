// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

contract EventSetter {
    uint256 toSet;
    bool isProtected;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    event Set_Ok(address indexed from, uint256 value);

    function setter_ok (uint256 _setter) external onlyOwner {
        toSet = _setter;
        emit Set_Ok(msg.sender, toSet);
    }

    function setter_vuln (uint256 _setter) external onlyOwner {
        toSet = _setter;
    }
}