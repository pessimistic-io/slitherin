//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import './interfaces/IUniswapV2Pair.sol';
import './interfaces/IUniswapV2ERC20.sol';

/// @notice Contract that uses Pair contract of UniswapV2 directly, uses reserve balance
contract Bad_UniswapV2_test {
    IUniswapV2Pair uniswap;
    IUniswapV2ERC20 token;
    uint112 private reserve0;
    uint112 private reserve1;
    uint32  private blockTimestampLast;

    constructor(address _uniswap, address _token){
        uniswap = IUniswapV2Pair(_uniswap); // Поиска использования интерфейса - достаточно?
        token = IUniswapV2ERC20(_token);

    }

    /// @notice Calls the swap function of the Pair contract
    function direct_pair_swap_call (uint _amount0Out, uint _amount1Out, address _to, bytes calldata _data) external {
        uniswap.swap(_amount0Out, _amount1Out, _to, _data);
    }

    /// @notice Checks reserve balance to return certain boolean
    function reserve_balance_used () external returns (bool) {
        (reserve0,reserve1,blockTimestampLast) = uniswap.getReserves(); // Поиска использования функции getReserves достаточно?
        if(reserve0 > 100){
            return false;
        }
        return true;
    }

    /// @notice Checks pair token balance to return certain boolea
    function pair_token_balance_used (address _owner) external returns (bool) {
        if (token.balanceOf(_owner) > 100){ // Често говоря хз, какую эвристику придумать
            return false;
        }
        return true;
    }
    
}

