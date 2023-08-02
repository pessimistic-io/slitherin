pragma solidity ^0.8.0;

interface I {
    function initialize() external;
}

contract unprotected_initialize {
    uint256 toSet;
    bool isProtected = true;
    address owner = 0xFeebabE6b0418eC13b30aAdF129F5DcDd4f70CeA;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    function initialize_ok1(uint256 setter) external onlyOwner {
        uint256 a = 10;
        toSet = setter + a;
    }

    function initialize_ok2(uint256 setter) external {
        require(msg.sender == owner);
        uint256 a = 10;
        toSet = setter + a;
    }

    function initialize_vuln(uint256 setter) external {
        toSet = setter;
    }

    function init_ok1(uint256 setter) external onlyOwner {
        uint256 a = 10;
        toSet = setter + a;
    }

    function init_ok2(uint256 setter) external {
        require(msg.sender == owner);
        uint256 a = 10;
        toSet = setter + a;
    }

    function init_vuln(uint256 setter) external {
        toSet = setter;
    }
}
