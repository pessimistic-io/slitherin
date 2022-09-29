pragma solidity ^0.8.0;

contract StrangeSetter {
    uint256 toSet;
    bool isProtected = true;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    function set_vulnurable(uint256 setter) public onlyOwner {
        uint256 a = 10;
        a = setter;
    }

    function set_ok(uint256 setter) public onlyOwner {
        toSet = setter;
    }
}
