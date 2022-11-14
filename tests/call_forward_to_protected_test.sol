pragma solidity ^0.8.0;

contract call_forward_to_protected_test {

    function set_vulnurable(address customAddress) public returns (bool){
        (bool success, bytes memory data) = customAddress.call("");
        return success;
    }
    
    function set_vulnurable2(address customAddress) public returns (bool){
        (bool success, bytes memory data) = customAddress.staticcall("");
        return success;
    }
}
