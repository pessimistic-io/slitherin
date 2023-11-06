pragma solidity ^0.8.0;

contract falsy_only_eoa_modifier_test {
    uint256 toSet;
    address owner = msg.sender;

    modifier onlyOwner() {
        require(owner == msg.sender);
        _;
    }

    function set_vulnerable(uint256 setter) public onlyOwner {
        if(msg.sender == tx.origin){
            toSet = setter;
        }
    }

    function set_tx_origin(uint256 setter) public onlyOwner {
        if(owner == tx.origin){
            toSet = setter;
        }
    }

    function set_ok(uint256 setter) public onlyOwner {
        toSet = setter;
    }
}
