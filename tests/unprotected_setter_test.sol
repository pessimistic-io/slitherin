pragma solidity ^0.8.0;

contract unprotected_setter_test {
    uint256 toSet;
    bool isProtected = true;
    address owner = 0xFeebabE6b0418eC13b30aAdF129F5DcDd4f70CeA;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    function setter_ok1(uint256 setter) external onlyOwner {
        uint256 a = 10;
        toSet = setter + a;
    }

    function setter_ok2(uint256 setter) external {
        require(msg.sender == owner);
        uint256 a = 10;
        toSet = setter + a;
    }

    function setter_vuln(uint256 setter) external {
        toSet = setter;
    }
}
