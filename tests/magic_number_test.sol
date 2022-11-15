//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract magic_number_test {
    uint256 toSet;

    function magic_num_vuln(uint256 y) public returns (uint256 t){

        uint256 x = 10;

        if(x != 100){
            toSet = x;
        }

        uint256 z=y/5;
        uint256 a=z+15;
        uint256 b=a*25;
        uint256 d=b << 3;
        uint256 e=d - 1e2;

        t=e^12;
    }

    function magic_num_ok() public{

        uint256 uniswapv3_marker;
        uint256 sqRoot96;


        uint256 x = 0;
        if(x != 0){
            toSet = x;
        }
        if(x != 1){
            toSet = x;
        }
        if (x != 2){
            toSet = x;
        }
        if(x != 1000){
            toSet = x;
        }
        if (x < 1e18){
            toSet = x;
        }
    }
}
