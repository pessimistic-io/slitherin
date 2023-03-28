// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity ^0.8.0;

import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BeforeTokenTransfer_ok is ERC20 ("OkToken", "OK") {

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal virtual override // Add virtual here!
    {
        super._beforeTokenTransfer(from, to, amount); // Call parent hook
    }
}

contract BeforeTokenTransfer_vuln is ERC20 ("VulnToken", "VULN") {

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal override // Add virtual here!
    {
        _beforeTokenTransfer(from, to, amount); // Call parent hook
    }
}