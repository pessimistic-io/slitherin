//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import './interfaces/IUniswapV2Router02.sol';
import './interfaces/IUniswapV2Pair.sol';
import './interfaces/IUniswapV2ERC20.sol';


/// @notice Contract that uses Pair contract of UniswapV2 directly, uses reserve balance
contract Bad_UniswapV2_test {
    IUniswapV2Pair uniswap;
    IUniswapV2ERC20 token;
    IUniswapV2Router02 router2;
    uint112 private reserve0;
    uint112 private reserve1;
    uint32  private blockTimestampLast;

    constructor(address _uniswap, address _token, address _router2){
        uniswap = IUniswapV2Pair(_uniswap);
        token = IUniswapV2ERC20(_token);
        router2 = IUniswapV2Router02(_router2);
    }

    /// @notice Calls the swap function of the Pair contract
    function direct_pair_swap_call (uint _amount0Out, uint _amount1Out, address _to, bytes calldata _data) external {
        uniswap.swap(_amount0Out, _amount1Out, _to, _data);
    }

    /// @notice Checks reserve balance to return a certain boolean
    function reserve_balance_used () external returns (bool) {
        (reserve0,reserve1,blockTimestampLast) = uniswap.getReserves(); // TODO find usage of reserve0, reserve1
        if(reserve0 > 100){
            return false;
        }
        return true;
    }

    /// @notice Checks pair token balance to return a certain boolean
    function pair_token_balance_used (address _uniswap) external returns (bool) {
        if (token.balanceOf(address(IUniswapV2Pair(_uniswap))) > 100){
            return false;
        }
        return true;
    }

    /// @notice Checks pair token balance to return a certain boolean
    function pair_token_balance_used_2 () external returns (bool) {
        if (token.balanceOf(address(uniswap)) > 100){
            return false;
        }
        return true;
    }

    /// @notice Checks pair token balance to return a certain boolean
    function pair_token_balance_used_3 () external returns (bool) {
        address new_uni = address(uniswap);
        if (token.balanceOf(new_uni) > 100){
            return false;
        }
        return true;
    }
    
    /// @notice Uses functions where amountOutMin must be more than 0
    function amount_min_return_zero_router01 (uint amountIn, address[] calldata path, address to, uint deadline) external { // amountOutMin > 0
        uint amountOutMin = 0;
        uint256[] memory amounts_1 = router2.swapExactTokensForTokens(amountIn, amountOutMin, path, to, deadline);
        uint256[] memory amounts_2 = router2.swapExactETHForTokens(amountOutMin, path, to, deadline);
        uint256[] memory amounts_3 = router2.swapExactTokensForETH(amountIn, amountOutMin, path, to, deadline);
    }

    /// @notice Explain to an end user what this does
    function amount_max_not_infinite_router01_1 (uint amountOut, address[] calldata path, address to, uint deadline) external { // amountInMax != type(uint).max или type(uint256).max
        uint amountInMax_1 = type(uint).max; 
        uint256[] memory amounts_1 = router2.swapTokensForExactTokens(amountOut, amountInMax_1, path, to, deadline);
    }

    /// @notice Explain to an end user what this does
    function amount_max_not_infinite_router01_2 (uint amountOut, address[] calldata path, address to, uint deadline) external { // amountInMax != type(uint).max или type(uint256).max
        uint amountInMax_2 = type(uint256).max;
        uint256[] memory amounts_2 = router2.swapTokensForExactETH(amountOut, amountInMax_2, path, to, deadline);
    }

    function amount_min_return_zero_router02 (uint amountIn, address[] calldata path, address to, uint deadline) external {
        uint amountOutMin = 0;
        router2.swapExactTokensForTokensSupportingFeeOnTransferTokens(amountIn, amountOutMin, path, to, deadline);
        router2.swapExactETHForTokensSupportingFeeOnTransferTokens(amountOutMin, path, to, deadline);
        router2.swapExactTokensForETHSupportingFeeOnTransferTokens(amountIn, amountOutMin, path, to, deadline);
    }

    function uses_deflat_token () external view returns (address) {
        address deflat_token = 0x7db5af2B9624e1b3B4Bb69D6DeBd9aD1016A58Ac;
        return deflat_token; 
    }

    // function uses_rebase_token () external view returns (address){
    //     address rebase_token = 0xd46ba6d942050d489dbd938a2c909a5d5039a161;
    //     return rebase_token;
    // }
}

