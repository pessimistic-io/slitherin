pragma solidity ^0.8.0;

contract tx_gasprice_warning {
    uint256 toSet;

    function set_vulnurable(uint256 setter) external {
        uint256 a = 10;
        toSet = setter + a + tx.gasprice;
    }

    function set_ok(uint256 setter) external {
        uint256 a = 10;
        toSet = setter + a;
    }
}
