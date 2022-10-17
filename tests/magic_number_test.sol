pragma solidity ^0.8.0;

contract magic_number_test {
    uint256 toSet;

    function magic_num_vuln() public {
        uint256 x = 10;
        if(x != 100){
            toSet = x;
        }
    }

    function magic_num_ok() public{
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
