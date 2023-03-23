// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import './interfaces/IUniswapV2Router02.sol';

//TODO Finish good UniV2 integration
/// @notice Contract that uses Router contract of UniswapV2 instead of Pair
contract Good_UniswapV2_Integration_1 {
    IUniswapV2Router02 uniswap;

    constructor(address _uniswap){
        uniswap = IUniswapV2Router02(_uniswap);
    }
    
    function router_swap_call(uint amountOutMin, address[] calldata path, address to, uint deadline) external {
        uniswap.swapExactETHForTokensSupportingFeeOnTransferTokens(amountOutMin, path, to, deadline);
    }

}