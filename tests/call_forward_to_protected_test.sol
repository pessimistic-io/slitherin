pragma solidity ^0.8.0;

import "../node_modules/@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../node_modules/@openzeppelin/contracts/utils/Address.sol";

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

contract OZCallForwardToProtectedTest {
    function safeERC20ShouldBeIgnored(IERC20 target, address to, uint256 value) external {
        SafeERC20.safeTransfer(target, to, value);
    }

    function transferHelperShouldBeIgnored(address payable to, uint256 value) external {
        Address.sendValue(to, value);
    }
}
