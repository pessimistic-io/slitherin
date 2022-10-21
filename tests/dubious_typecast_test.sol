pragma solidity ^0.8.0;

contract dubious_typecast_test {
    uint256 constant a = 1000;
    uint8 constant b = 10;

    function mul_vulnerable_uint () public view returns (uint8){
        uint8 res = uint8(a)*b;
    }

    function mul_ok () public view returns (uint256) {
        uint256 res = a*b;
    }
}
