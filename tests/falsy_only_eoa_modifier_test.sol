pragma solidity ^0.8.0;

contract falsy_only_eoa_modifier_test {
    uint256 toSet;
    bool isProtected = true;

    modifier onlyOwner() {
        require(isProtected);
        _;
    }

    function set_vulnurable(uint256 setter) public onlyOwner {
        if(msg.sender == tx.origin){
            toSet = setter;
        }
    }

    function set_ok(uint256 setter) public onlyOwner {
        toSet = setter;
    }
}
