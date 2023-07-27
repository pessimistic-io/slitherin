// SPDX-License-Identifier: MIT

pragma solidity ^0.8.19;

interface IERC20 {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

contract Test
{
    IERC20 immutable TOKEN = IERC20(address(0));
    function test() internal {
        TOKEN.transferFrom(address(this), address(0), 0);
    }
}

