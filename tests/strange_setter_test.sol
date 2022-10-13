pragma solidity ^0.8.0;

contract StrangeSetter {
    uint256 toSet;
    bool isProtected = true;
    mapping(bytes32 => address) s_builders;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    function set_vulnurable(uint256 setter) public onlyOwner {
        uint256 a = 10;
        a = setter;
    }

    function setBuilder(bytes32 nameHash, address builder) public onlyOwner{
        uint256 x = 0;
        vulnurable_internal(x);
    }

    function set_ok(uint256 setter) public onlyOwner {
        toSet = setter;
    }

    function vulnurable_internal(uint256 setter) internal {
        toSet = setter;
    } 
}
